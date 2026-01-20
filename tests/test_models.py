import pytest
from src.cli.models import BenchmarkConfig, BenchmarkResult, SpeedResult


def test_speed_result():
    result = SpeedResult(
        concurrency=1,
        generation_speed=58.49,
        prompt_throughput=846.81,
        max_ttft=0.05,
        min_ttft=0.05,
        success_rate=1.0,
    )
    assert result.concurrency == 1
    assert result.generation_speed == 58.49


def test_benchmark_result():
    speed_results = [
        SpeedResult(
            concurrency=1,
            generation_speed=58.49,
            prompt_throughput=846.81,
            max_ttft=0.05,
            min_ttft=0.05,
            success_rate=1.0,
        )
    ]
    result = BenchmarkResult(
        model_name="gpt-4",
        input_tokens=45,
        output_tokens=512,
        latency=2.2,
        results=speed_results,
    )
    assert result.model_name == "gpt-4"
    assert len(result.results) == 1


def test_benchmark_config():
    config = BenchmarkConfig(
        base_url="https://api.example.com/v1",
        api_key="sk-123",
        model="gpt-4",
        concurrency=[1, 2, 4],
        max_tokens=512,
        prompt="Test prompt",
        num_words=100,
        format="json",
    )
    assert config.base_url == "https://api.example.com/v1"
    assert config.concurrency == [1, 2, 4]