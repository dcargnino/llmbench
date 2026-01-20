import asyncio
import logging
import typer
from typing import List, Optional
from src.cli.models import BenchmarkConfig
from src.cli.benchmark import run_benchmark
from src.cli.formatters import output_result

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = typer.Typer()


def parse_concurrency(value: str) -> List[int]:
    """Parse comma-separated concurrency levels into a list of integers.

    Args:
        value: Comma-separated string of concurrency levels (e.g., "1,2,4").

    Returns:
        List of integer concurrency levels.

    Raises:
        ValueError: If any value cannot be converted to int.
    """
    return [int(x.strip()) for x in value.split(",")]


@app.command()
def benchmark(
    base_url: str = typer.Option(..., "--base-url", help="API endpoint URL"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API authentication key"),
    model: Optional[str] = typer.Option(None, "--model", help="Model name (auto-discovered if not provided)"),
    concurrency: str = typer.Option("1", "--concurrency", help="Comma-separated concurrency levels", callback=parse_concurrency),
    max_tokens: int = typer.Option(512, "--max-tokens", help="Maximum output tokens"),
    prompt: Optional[str] = typer.Option(None, "--prompt", help="Custom prompt text"),
    num_words: Optional[int] = typer.Option(None, "--num-words", help="Number of random words for prompt"),
    format: Optional[str] = typer.Option(None, "--format", help="Output format (json/yaml)"),
):
    """Run LLM API benchmark with specified configuration.

    This command performs concurrent API calls to measure performance metrics
    including generation speed, prompt throughput, time to first token, and success rate.

    Args:
        base_url: The base URL of the LLM API endpoint.
        api_key: Optional API key for authentication.
        model: Model name to test (auto-discovered if not provided).
        concurrency: Comma-separated list of concurrency levels to test.
        max_tokens: Maximum number of tokens to generate per request.
        prompt: Custom prompt text (randomly generated if not provided).
        num_words: Number of words for random prompt generation.
        format: Output format for results (json, yaml, or console table).
    """
    config = BenchmarkConfig(
        base_url=base_url,
        api_key=api_key,
        model=model,
        concurrency=concurrency,
        max_tokens=max_tokens,
        prompt=prompt,
        num_words=num_words,
        format=format,
    )

    async def main():
        try:
            result = await run_benchmark(config)
            output_result(result, config.format)
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)

    asyncio.run(main())


if __name__ == "__main__":
    app()