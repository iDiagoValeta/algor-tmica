# algor-tmica

**A Wikipedia search engine in Python whose queries tolerate misspelled words, built around hand-written edit-distance algorithms (Levenshtein and two Damerau variants) and a spell suggester.**

> **Context.** Built in November 2025 as a group coursework project for Algorítmica (ALT) at UPV, coordinated with the Sistemas de Almacenamiento y Recuperación de Información (SAR) project, when I was finishing my Computer Engineering degree and working at Grupo CEU. It is where I implemented dynamic-programming edit distances and plugged them into a retrieval engine; the retrieval ideas fed into the local RAG work of my final degree project, MonkeyGrab. It is kept as it was submitted; the code is not maintained.

The project was done in a group of four (the code headers list the team). It has two parts: the SAR engine (index and boolean queries over Wikipedia articles, per the SAR project PDF) and the ALT part (approximate string matching, per the course handout), joined so that a term missing from the index is replaced by its closest vocabulary words.

## What it does

- Indexes Wikipedia articles stored as JSON-lines files (one article per line) into an inverted index over the `all` field, saved to disk with `pickle`.
- Answers boolean queries with `AND`, `OR` and `NOT`, evaluated left to right, from a single query, a file of queries (`-L`) or an interactive prompt.
- Compares results against a file of expected counts (`-T`) and can show only counts (`-C`) or snippets (`-N`).
- Implements six edit-distance variants: Levenshtein (full matrix, two-row reduction, with threshold cut-off, with optimistic bound), restricted Damerau-Levenshtein and intermediate Damerau-Levenshtein.
- `SpellSuggester` returns the vocabulary words within a distance threshold of a term, grouped by distance.
- When spelling correction is on and a query term is not in the index, the term is replaced by the union of the postings of its suggestions.

## How it works

1. `SAR_Indexer.py` calls `SAR_Indexer.index_dir` (in `SAR_lib.py`), which tokenizes every article (lowercase, non-alphanumeric characters removed) and builds a term to sorted list of article ids index.
2. `solve_query` splits the query into terms and connectors and combines posting lists with `and_posting`, `or_posting` and `reverse_posting` (for `NOT`).
3. `get_posting` looks the term up. If it is missing and correction is on, `SpellSuggester.suggest` compares it with the whole vocabulary using the chosen distance and threshold, and the postings of all suggestions are merged.
4. `distancias_parte1.py` holds the textbook versions (full matrix, and recovery of the edit operations). `distancias_parte2.py` holds the optimised ones: they keep only the last columns of the matrix and stop as soon as the minimum of a column exceeds the threshold, returning `threshold + 1`. `opcionesSpell` maps names to functions: `levenshtein_m`, `levenshtein_r`, `levenshtein`, `levenshtein_o`, `damerau_r`, `damerau_i`.

Not implemented, although the template and attributes in `SAR_lib.py` leave room for it: positional (phrase) queries, a multi-field index and the semantic (embedding) index. The `-P` and `-S` flags of the indexer are accepted but not used by the indexing code, and `SAR_Searcher.py` from the template is not in the repository, only `ALT_Searcher.py`.

## Results

Numbers committed by the authors, not recomputed here.

Suggestions found on the vocabulary of `miniquijote.txt` (output of `test_spellsuggester.py`, saved in `resultado_test_spellsuggester.txt`), counts at distance 0 to 4 and total:

| Term | Levenshtein | Damerau restricted | Damerau intermediate |
|---|---|---|---|
| `casa` | [1, 17, 81, 344, 847], 1290 | [1, 17, 81, 345, 846], 1290 | [1, 17, 81, 346, 845], 1290 |
| `ancho` | [0, 2, 13, 75, 511], 601 | [0, 2, 13, 78, 510], 603 | [0, 2, 13, 81, 527], 623 |
| `ecrvantse` | [0, 0, 0, 0, 7], 7 | [0, 0, 1, 0, 6], 7 | [0, 0, 1, 0, 6], 7 |
| `uqijoext` | 0 | 2 | 2 |

The Levenshtein variants (`levenshtein_r`, `levenshtein`, `levenshtein_o`) give identical counts. In `resultados/test_suggester_damerau_i.txt`, `ecrvantse` at distance 2 yields `cervantes`.

`queries.txt` holds 35 queries with deliberate typos. `result_100_original.txt` lists the number of results per query without correction (for example `capitla` 0, `virneg` 0) and `result_100_levenshtein_3.txt`, `result_100_damerau_r_3.txt` and `result_100_damerau_i_3.txt` the counts with correction (for example `capitla` 171, `virneg` 255 with Levenshtein). The file names suggest threshold 3 on the 100-article collection; the exact commands used were not recorded in the repo.

## Run it

Not run again while writing this README; the commands follow the argument parsers in the code. Needs Python 3 and `numpy`.

```bash
pip install numpy
unzip 100.zip                      # 100/ already exists in the repo; 500.zip is the larger collection (about 37 MB)
python SAR_Indexer.py 100 mi_indice
python ALT_Searcher.py mi_indice -Q "capital AND NOT secuela"
python ALT_Searcher.py mi_indice -Q "capitla" -s -d levenshtein -t 3
python ALT_Searcher.py mi_indice -L queries.txt -d damerau_r -t 3
python test_distancias_parte2.py   # compares the distance functions on sample pairs with several bounds
python test_spellsuggester.py      # writes resultados/test_suggester_<distance>.txt
```

Searcher options: `-Q` query, `-L` file of queries, `-T` file of queries with expected results, `-C` count only, `-N` snippets, `-A` show all results (otherwise 10), `-s` enable correction, `-d` distance (`levenshtein`, `levenshtein_o`, `damerau_r`, `damerau_i`), `-t` threshold. With no query option it opens an interactive prompt.

## Repository layout

```
SAR_Indexer.py            indexing entry point
ALT_Searcher.py           search entry point (query, list, test, interactive)
SAR_lib.py                SAR_Indexer class: tokenizer, index, boolean query solving, spelling hook
spellsuggester.py         SpellSuggester: vocabulary and suggest()
distancias_parte1.py      distances as a full matrix, plus edit operations
distancias_parte2.py      optimised distances with threshold and opcionesSpell
test_distancias_parte2.py, test_spellsuggester.py   test scripts
miniquijote.txt           vocabulary text for the suggester tests
100/, 100.zip, 500.zip    Wikipedia article collections (JSON lines)
queries.txt, result_100_*.txt, resultados/, resultado_test_spellsuggester.txt   saved outputs
mi_indice, index_100.bin  prebuilt indexes
boletin.pdf               ALT handout: approximate string matching
SAR_Proyecto_practicas.pdf   SAR project statement
```

## Stack

Python, NumPy, pickle, argparse, regular expressions.
