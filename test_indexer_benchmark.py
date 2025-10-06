# test_indexer_benchmark.py
import pytest
from indexer import tokenize, process_book
import random
import string

# Dummy text generator
def generate_dummy_text(word_count=1000):
    words = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(word_count)]
    return ' '.join(words)

def test_tokenize_benchmark(benchmark):
    dummy_text = generate_dummy_text()
    result = benchmark(tokenize, dummy_text)
    assert isinstance(result, list)

def test_process_book_benchmark(benchmark):
    dummy_text = generate_dummy_text()
    dummy_id = random.randint(100000, 999999)
    result = benchmark(process_book, dummy_id, dummy_text)
    assert result is None  # process_book returns nothing
