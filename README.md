# SAR-ALT Wikipedia Search Engine

This project implements an information retrieval system for Wikipedia articles. It allows for indexing JSON collections and performing boolean, positional, and semantic queries, including spelling correction features.

## Project Structure

The repository is organized into several key components:

* **SAR_Indexer.py**: The main program for indexing articles. It extracts content from a local collection, creates the index, and saves the object instance to disk.
* **ALT_Searcher.py / SAR_Searcher.py**: Programs for article retrieval. They load the index and respond to queries in interactive or batch modes.
* **SAR_lib.py**: The core library defining the SAR_Project class. It contains the logic for tokenization, index data structure management, and query resolution algorithms.
* **spellsuggester.py**: Implementation of the spelling corrector that suggests alternative terms based on edit distances.
* **distancias_parte2.py**: Contains the distance functions (Levenshtein and Damerau-Levenshtein) used by the spelling corrector.

## Main Features

### 1. Indexing
* Recursive processing of JSON files.
* Text tokenization by removing non-alphanumeric symbols and normalizing to lowercase.
* Creation of an inverted index accessible by term for multiple fields (title, summary, all).
* Support for positional indices to allow exact phrase searches.

### 2. Retrieval and Queries
* Boolean queries with AND and NOT operators, evaluated from left to right.
* Positional search using double quotes to find consecutive terms.
* Operational modes: Direct query (-Q), query list (-L), and test mode (-T) for result verification.

### 3. Spelling Correction (ALT Extension)
* Integration of a suggestion module based on edit distances.
* Configurable thresholds and distance types (Levenshtein, Restricted Damerau-Levenshtein, and Intermediate Damerau-Levenshtein) via the searcher.

### 4. Semantic Search (SAR Extension)
* Text embedding generation using models such as Spacy, BETO, or Sentence BERT.
* Use of KDTree structures for article retrieval by semantic similarity, even without exact term matches.

## Usage Requirements

### Indexing
To create an index from a directory of documents:
```bash
python SAR_Indexer.py <document_directory> <index_name>

```

Additional options:

* `-P`: Include positional information.
* `-S`: Include the semantic index.

### Searching

To perform queries on a created index:

```bash
python ALT_Searcher.py <index_name> -Q "query"

```

Spelling correction options:

* `-s`: Activate spelling correction.
* `-t <threshold>`: Define the distance threshold.
* `-d <distance>`: Select the algorithm (levenshtein, levenshtein_o, damerau_r, damerau_i).

```

```
