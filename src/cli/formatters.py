import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console
from rich.table import Table

from src.cli.models import BenchmarkResult
from src.core.constants import DEFAULT_MARKDOWN_FILENAME


def format_console(result: BenchmarkResult) -> str:
    """Format benchmark results for console display using Rich tables.

    Displays results in a formatted table with summary information.

    Args:
        result: BenchmarkResult containing all measurement data.

    Returns:
        Empty string (output is printed directly to console).
    """
    console = Console()
    table = Table(title="Benchmark Results")

    table.add_column("Concurrency", justify="right")
    table.add_column("Generation Throughput (tokens/s)", justify="right")
    table.add_column("Prompt Throughput (tokens/s)", justify="right")
    table.add_column("Min TTFT (s)", justify="right")
    table.add_column("Max TTFT (s)", justify="right")
    table.add_column("Success Rate", justify="right")

    for r in result.results:
        table.add_row(
            str(r.concurrency),
            f"{r.generation_speed:.2f}",
            f"{r.prompt_throughput:.2f}",
            f"{r.min_ttft:.2f}",
            f"{r.max_ttft:.2f}",
            f"{r.success_rate:.2%}",
        )

    console.print(f"Input Tokens: {result.input_tokens}")
    console.print(f"Output Tokens: {result.output_tokens}")
    console.print(f"Test Model: {result.model_name}")
    console.print(f"Latency: {result.latency:.2f} ms")
    console.print()
    console.print(table)

    return ""  # Console output doesn't return string


def format_json(result: BenchmarkResult) -> str:
    """Format benchmark results as JSON string.

    Args:
        result: BenchmarkResult to serialize.

    Returns:
        JSON formatted string with indentation.
    """
    return json.dumps(result.model_dump(), indent=2)


def format_yaml(result: BenchmarkResult) -> str:
    """Format benchmark results as YAML string.

    Args:
        result: BenchmarkResult to serialize.

    Returns:
        YAML formatted string.
    """
    return yaml.dump(result.model_dump())


def format_markdown(result: BenchmarkResult) -> str:
    """Format benchmark results as Markdown table.

    Args:
        result: BenchmarkResult to format.

    Returns:
        Markdown string with summary and table.
    """
    lines = []
    lines.append(f"Input Tokens: {result.input_tokens}")
    lines.append(f"Output Tokens: {result.output_tokens}")
    lines.append(f"Test Model: {result.model_name}")
    lines.append(f"Latency: {result.latency:.2f} ms")
    lines.append("")
headers = ["Concurrency", "Generation Throughput (tokens/s)", "Prompt Throughput (tokens/s)", "Min TTFT (s)", "Max TTFT (s)", "Success Rate"]

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")

    for r in result.results:
        row = [
            str(r.concurrency),
            f"{r.generation_speed:.2f}",
            f"{r.prompt_throughput:.2f}",
            f"{r.min_ttft:.2f}",
            f"{r.max_ttft:.2f}",
            f"{r.success_rate:.2%}",
        ]
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def save_markdown(result: BenchmarkResult, filename: str = DEFAULT_MARKDOWN_FILENAME):
    """Save benchmark results to a Markdown file.

    Args:
        result: BenchmarkResult to save.
        filename: Output filename (default: DEFAULT_MARKDOWN_FILENAME).
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"
    content = format_markdown(result)
    Path(filename).write_text(content)


def output_result(result: BenchmarkResult, output_format: Optional[str] = None):
    """Output benchmark results in the specified format.

    Displays results to console and always saves a Markdown file.

    Args:
        result: BenchmarkResult to output.
        output_format: Format type ("json", "yaml", or None for console).
    """
    if output_format == "json":
        print(format_json(result))
    elif output_format == "yaml":
        print(format_yaml(result))
    else:
        format_console(result)

    # Always save markdown
    save_markdown(result)