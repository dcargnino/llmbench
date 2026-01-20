# LLM Benchmark Tool

A comprehensive Python tool for benchmarking Large Language Model (LLM) APIs. This tool measures key performance metrics including generation speed, prompt throughput, time to first token (TTFT), and success rates across different concurrency levels.

## Features

- **Concurrent API Testing**: Test multiple concurrency levels simultaneously
- **Comprehensive Metrics**: Measure generation speed, prompt throughput, TTFT, and success rates
- **Multiple Output Formats**: Support for console tables, JSON, and YAML output
- **Flexible Configuration**: Custom prompts or auto-generated random prompts
- **Network Latency Measurement**: Built-in latency testing to API endpoints
- **Rich Console Output**: Beautiful tables and progress indicators

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install from Source

```bash
git clone <repository-url>
cd llmbench
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
llmbench --base-url https://api.openai.com/v1 --api-key sk-your-key-here
```

### Advanced Usage

```bash
llmbench \
  --base-url https://api.example.com/v1 \
  --api-key sk-your-key \
  --model gpt-4 \
  --concurrency 1,2,4,8 \
  --max-tokens 512 \
  --prompt "Write a short story about AI" \
  --format json
```

### Command Line Options

- `--base-url`: API endpoint base URL (required)
- `--api-key`: API authentication key
- `--model`: Model name (auto-discovered if not provided)
- `--concurrency`: Comma-separated concurrency levels (default: 1)
- `--max-tokens`: Maximum tokens to generate (default: 512)
- `--prompt`: Custom prompt text
- `--num-words`: Number of random words for prompt generation (default: 100)
- `--format`: Output format (json, yaml, or console table)

## Output Metrics

### Generation Speed
Tokens generated per second, calculated as total output tokens divided by response time minus network latency.

### Prompt Throughput
Tokens processed per second for input prompts, measured from request start to first token.

### Time to First Token (TTFT)
Time from request initiation to receiving the first token, in seconds.

### Success Rate
Percentage of successful API calls out of total attempts.

## Output Formats

### Console (Default)
Rich-formatted table with summary information and detailed metrics per concurrency level.

### JSON
Structured JSON output containing all benchmark data.

### YAML
Human-readable YAML format with complete results.

All formats automatically save a Markdown file (`benchmark_results.md`) with the results.

## Architecture

The tool is organized into the following modules:

- `cli/`: Command-line interface and output formatting
- `core/api/`: API client and prompt generation utilities
- `core/utils/`: Performance measurement utilities
- `core/`: Constants and exception definitions

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Project Structure

```
llmbench/
├── src/
│   ├── cli/
│   │   ├── main.py          # CLI entry point
│   │   ├── models.py        # Data models
│   │   ├── benchmark.py     # Benchmark orchestration
│   │   └── formatters.py    # Output formatting
│   └── core/
│       ├── api/
│       │   ├── client.py    # OpenAI API client
│       │   └── prompts.py   # Prompt generation
│       ├── utils/
│       │   ├── latency.py   # Network latency measurement
│       │   └── speed.py     # Performance metrics
│       ├── constants.py     # Application constants
│       └── exceptions.py    # Custom exceptions
├── tests/                   # Unit tests
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## API Compatibility

This tool is designed to work with OpenAI-compatible APIs. It has been tested with:

- OpenAI API
- Compatible local LLM servers (e.g., vLLM, Ollama with OpenAI compatibility)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.