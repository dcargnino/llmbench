import asyncio
from typing import Optional

from openai import AsyncOpenAI

from src.cli.models import BenchmarkConfig, BenchmarkResult, SpeedResult
from src.core.api.client import get_first_available_model, estimate_tokens
from src.core.api.prompts import generate_random_phrase
from src.core.constants import DEFAULT_NUM_WORDS
from src.core.utils.latency import measure_latency
from src.core.utils.speed import run_speed_measurement


async def run_benchmark(config: BenchmarkConfig) -> BenchmarkResult:
    """Execute the complete benchmark suite based on configuration.

    This function orchestrates the benchmark process including model discovery,
    latency measurement, and speed testing across different concurrency levels.

    Args:
        config: Benchmark configuration containing API settings and test parameters.

    Returns:
        Complete benchmark results with all measured metrics.

    Raises:
        ValueError: If configuration is invalid or API calls fail.
        RuntimeError: If network or API errors occur during measurement.
    """
    # Initialize client
    client = AsyncOpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
    )

    # Get model if not provided
    model = config.model
    if not model:
        model = await get_first_available_model(client)

    # Determine prompt and input tokens
    use_random_input = config.prompt is None
    if use_random_input:
        if config.num_words is None:
            config.num_words = DEFAULT_NUM_WORDS
        prompt = generate_random_phrase(config.num_words)
    else:
        prompt = config.prompt

    input_tokens = estimate_tokens(prompt)

    # Measure latency
    latency = await measure_latency(config.base_url)

    # Run benchmarks for each concurrency level
    results = []
    for concurrency in config.concurrency:
        speed_result = await run_speed_measurement(
            client=client,
            model_name=model,
            prompt=prompt if not use_random_input else None,
            use_random_input=use_random_input,
            num_words=config.num_words or 100,
            max_tokens=config.max_tokens,
            latency=latency,
            concurrency=concurrency,
        )
        results.append(SpeedResult(**speed_result))

    return BenchmarkResult(
        model_name=model,
        input_tokens=input_tokens,
        output_tokens=config.max_tokens,
        latency=latency,
        results=results,
    )