import pytest


def pytest_addoption(parser):
    parser.addoption("--model", action="store", default="ggml-gpt4all-j.bin")
    parser.addoption("--instructions",
                     action="store",
                     choices=("avx2", "avx", "basic"),
                     required=True)


@pytest.fixture
def model(request):
    return request.config.getoption("--model")


@pytest.fixture
def instructions(request):
    return request.config.getoption("--instructions")
