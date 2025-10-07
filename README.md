# Big-Data
Basic search engine for the Big Data class at ULPGC

# Prototype Search Engine for Project Gutenberg

This project implements a **prototype search engine** for Project Gutenberg texts, as part of the Big Data course at ULPGC.

## Main Goal

- Download books from **Project Gutenberg**.  
- Build inverted indexes using **two different backends**:  
  - SQLite (relational database, single file).  
  - MongoDB (NoSQL, document-based).  
- Implement a minimal **query engine** for metadata and full-text search.  
- Benchmark both solutions to compare performance.

## What It Means

In our case, the requirements were:

- (C1) The system must allow **full-text search** using an inverted index.  
- (C2) At least **two different data structures** for the index must be tested and compared.  
- (C3) A **minimal query engine** must exist for basic retrieval (metadata + full-text).  

## How It Works

The pipeline has three main steps:

1. **Crawler**  
   - Downloads raw `.txt` books from Project Gutenberg.  
   - Cleans metadata using `strip_headers` from `gutenbergpy`.  
   - Stores both text and metadata in MongoDB.  

2. **Indexer**  
   - Tokenizes book texts into lowercase terms.  
   - Builds an inverted index in:  
     - **SQLite**: terms + JSON posting lists.  
     - **MongoDB**: documents with `{ term, postings }`.  

3. **Query Engine**  
   - **Metadata search**: title, author, language.  
   - **Full-text search**: Boolean AND queries (intersection of posting lists).  

**Execution**
Run the crawler
python crawler.py

Run the indexer
python indexer.py

Run the query engine
python search_engine.py

Run benchmarks
pytest --benchmark-only

The following metrics were collected:
- Indexing time (s) the time required to build the index for the dataset.
- Index size (MB)  the storage footprint of the index.
- Query latency (ms) the average response time for a set of test queries.
- Memory usage (MB) approximate memory consumption during queries.
  
<img width="675" height="376" alt="image" src="https://github.com/user-attachments/assets/e9355ed1-570d-405f-bf3b-75d3dbf9b66c" />


