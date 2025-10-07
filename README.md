# Big-Data
Prototype search engine for the Big Data course at ULPGC

## Overview
This project implements a **prototype search engine** for Project Gutenberg texts, as part of the Big Data course at ULPGC.

## Main Goals
- Download books from **Project Gutenberg**  
- Build inverted indexes using **two different backends**:  
  - SQLite (relational database, single file)  
  - MongoDB (NoSQL, document-based)  
- Implement a minimal **query engine** for metadata and full-text search  
- Benchmark both solutions to compare performance  

## Requirements
- (C1) The system must allow **full-text search** using an inverted index  
- (C2) At least **two different data structures** for the index must be tested and compared  
- (C3) A **minimal query engine** must exist for basic retrieval (metadata + full-text)  

## System Architecture
The pipeline has three main steps:

1. **Crawler**  
   - Downloads raw `.txt` books from Project Gutenberg  
   - Cleans metadata using `strip_headers` from `gutenbergpy`  
   - Stores both text and metadata in MongoDB  

2. **Indexer**  
   - Tokenizes book texts into lowercase terms  
   - Builds an inverted index in:  
     - **SQLite**: terms + JSON posting lists  
     - **MongoDB**: documents with `{ term, postings }`  

3. **Query Engine**  
   - **Metadata search**: title, author, language  
   - **Full-text search**: Boolean AND queries (intersection of posting lists)  

**Figure 1. System architecture of the prototype search engine.**  
<img width="384" height="456" alt="image" src="https://github.com/user-attachments/assets/38a0308c-b7d9-4d16-992c-f32f0981d952" />

## Execution

Run the crawler:
```bash

python crawler.py
python indexer.py
python search_engine.py
pytest --benchmark-only
```

The following metrics were collected:
- Indexing time (s) the time required to build the index for the dataset.
- Index size (MB)  the storage footprint of the index.
- Query latency (ms) the average response time for a set of test queries.
- Memory usage (MB) approximate memory consumption during queries.

## Credits
**Project Group Members**:
- Daniel Nosek,
- Lennart Schega,
- Domen Kac,
- Nico Brockmeyer,
- Anna Sowińska
  
**Datasets & Tools Used**:  
- [Project Gutenberg](https://www.gutenberg.org/) – source of book texts  
- Python 3.10+, pytest-benchmark, requests, pandas, sqlite3, pymongo  
- SQLite (relational backend)  
- MongoDB (NoSQL backend)  

© 2025 Big Data ULPGC Project Group
