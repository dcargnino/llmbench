import asyncio
import math
import time
from typing import Dict, List, Optional

from openai import AsyncOpenAI

from src.core.api.client import ask_openai, ask_openai_random_input


def round_to_two_decimals(f: float) -> float:
    """Round a float to two decimal places.

    Args:
        f: Float value to round.

    Returns:
        Rounded float with 2 decimal places.
    """
    return round(f, 2)


async def run_speed_measurement(
    client: AsyncOpenAI,
    model_name: str,
    prompt: Optional[str],
    use_random_input: bool,
    num_words: int,
    max_tokens: int,
    latency: float,  # in ms
    concurrency: int,
    progress_callback: Optional[callable] = None,
) -> Dict:
    """Run concurrent API calls and measure comprehensive performance metrics.

    Executes multiple concurrent requests to the LLM API and calculates
    generation speed, prompt throughput, time to first token, and success rate.

    Args:
        client: Configured AsyncOpenAI client instance.
        model_name: Name of the model to test.
        prompt: Custom prompt text (ignored if use_random_input is True).
        use_random_input: Whether to generate random prompts for each request.
        num_words: Number of words in random prompts.
        max_tokens: Maximum tokens to generate per request.
        latency: Network latency in milliseconds.
        concurrency: Number of concurrent requests to make.
        progress_callback: Optional callback for progress updates.

    Returns:
        Dictionary containing measured metrics compatible with SpeedResult model.
    """
    start_time = time.time()

    tasks = []
    for i in range(concurrency):
        if use_random_input:
            task = asyncio.create_task(
                ask_openai_random_input(client, model_name, num_words, max_tokens, progress_callback)
            )
        else:
            task = asyncio.create_task(
                ask_openai(client, model_name, prompt, max_tokens, progress_callback)
            )
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    duration = time.time() - start_time

    # Process results
    ttfts = []
    response_tokens = []
    prompt_tokens_list = []
    successful_requests = 0
    failed_requests = 0

    for result in results:
        if isinstance(result, Exception):
            failed_requests += 1
            continue
        ttft, completion_tokens, input_tokens = result
        successful_requests += 1
        ttfts.append(ttft)
        response_tokens.append(completion_tokens)
        prompt_tokens_list.append(input_tokens)

    total_response_tokens = sum(response_tokens)
    total_prompt_tokens = sum(prompt_tokens_list)

    success_rate = successful_requests / concurrency if concurrency > 0 else 0

    min_ttft = min(ttfts) if ttfts else 0
    max_ttft = max(ttfts) if ttfts else 0

    # Calculate speeds
    latency_sec = latency / 1000
    generation_speed = total_response_tokens / (duration - latency_sec) if duration > latency_sec else 0
    prompt_throughput = total_prompt_tokens / (max_ttft - latency_sec) if max_ttft > latency_sec else 0

    return {
        "concurrency": concurrency,
        "generation_speed": round_to_two_decimals(generation_speed),
        "prompt_throughput": round_to_two_decimals(prompt_throughput),
        "max_ttft": round_to_two_decimals(max_ttft),
        "min_ttft": round_to_two_decimals(min_ttft),
        "success_rate": success_rate,
    }