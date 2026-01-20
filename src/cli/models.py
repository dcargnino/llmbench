"""Data models for LLM benchmark configuration and results."""

from pydantic import BaseModel
from typing import List, Optional


class SpeedResult(BaseModel):
    """Result of a speed measurement for a specific concurrency level.

    Attributes:
        concurrency: Number of concurrent requests.
        generation_speed: Token generation speed in tokens/second.
        prompt_throughput: Prompt processing throughput in tokens/second.
        max_ttft: Maximum time to first token in seconds.
        min_ttft: Minimum time to first token in seconds.
        success_rate: Fraction of successful requests (0.0 to 1.0).
    """
    concurrency: int
    generation_speed: float  # tokens/s
    prompt_throughput: float  # tokens/s
    max_ttft: float  # seconds
    min_ttft: float  # seconds
    success_rate: float  # 0.0 to 1.0


class BenchmarkResult(BaseModel):
    """Complete benchmark result containing all measurements.

    Attributes:
        model_name: Name of the tested model.
        input_tokens: Number of input tokens used.
        output_tokens: Number of output tokens generated.
        latency: Network latency in milliseconds.
        results: List of speed results for different concurrency levels.
    """
    model_name: str
    input_tokens: int
    output_tokens: int
    latency: float  # ms
    results: List[SpeedResult]


class BenchmarkConfig(BaseModel):
    """Configuration for running a benchmark.

    Attributes:
        base_url: API endpoint base URL.
        api_key: Optional API authentication key.
        model: Optional model name (auto-discovered if not provided).
        concurrency: List of concurrency levels to test.
        max_tokens: Maximum tokens to generate per request.
        prompt: Optional custom prompt text.
        num_words: Optional number of random words for prompt generation.
        format: Optional output format (json, yaml, etc.).
    """
    base_url: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    concurrency: List[int]
    max_tokens: int = 512
    prompt: Optional[str] = None
    num_words: Optional[int] = None
    format: Optional[str] = None  # json, yaml, etc.