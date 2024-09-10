# WikiGraph Project 

The WikiGraph project consists of a set of Python scripts designed to crawl Wikipedia, analyze the connectivity between pages, and visualize the resulting graph. This project allows users to explore Wikipedia's structure and relationships between articles. 

## Overview

The project includes three main components:

- **wiki_crawler.py**: Crawls Wikipedia pages - starting from a specified article with specific depth of recursion - and constructs a directed graph of interconnected articles.

- **path_finder.py:** Finds the shortest path between two nodes in the graph (created by wiki_crawler.py), with support for both directed and undirected graphs. 

- **visualizer.py:** Visualizes the graph using pyvis, generating an interactive HTML representation of the graph.

## Usage

### wiki_crawler

```sh
python3 wiki_crawler.py -p <start_page> -d <depth>
```
- **-p <start_page>:** The starting Wikipedia page.
- **-d <depth>:** The maximum recursion depth.

Example: 
```sh
python3 wiki_crawler.py -p 'Python (programming_language)' -d 4

```

### shortest_path
```sh
python3 shortest_path.py --from <source> --to <dest> [-v] [--non-directed]
```
- **--from <source\>:** The starting article.
- **--to <dest\>:** The destination article.
- **-v:** Print the path instead of just the length.
- **--non-directed:** Treat the graph as undirected.

Example: 
```sh
python3 shortest_path.py --from 'Python (programming_language)' --to 'C++' -v
```

### render_graph

```sh
python3 render_graph.py
```
