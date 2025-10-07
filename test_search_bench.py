# test_search_bench.py
import pytest
from search_engine import bench_search, bench_search_multi

@pytest.mark.parametrize("term", ["love", "adventure", "island"])
def test_single_term(benchmark, term):
    benchmark(bench_search, term)

@pytest.mark.parametrize("terms", [["love", "adventure"], ["ship", "island"], ["sea", "journey", "storm"]])
def test_multi_term(benchmark, terms):
    benchmark(bench_search_multi, terms)

