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
<img width="382" height="471" alt="Diagram drawio" src="https://github.com/user-attachments/assets/e42570cc-6439-435e-a538-4379f4e27154" />


## Execution
Run the crawler:
```bash
python crawler.py
python indexer.py
python search_engine.py
pytest --benchmark-only
```
Benchmark Metrics

The following metrics were collected:

- Tokenization speed
- Search performance
- Indexing speed

Credits
Project Group Members:

- Daniel Nosek
- Lennart Schega
- Domen Kac
- Nico Brockmeyer
- Anna Sowińska

Datasets & Tools Used

Project Gutenberg – source of book texts
Python 3.10+, pytest-benchmark, requests, pandas, sqlite3, pymongo
SQLite (relational backend)
MongoDB (NoSQL backend)

© 2025 Big Data ULPGC Project Group
