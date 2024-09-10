import networkx as nx
from dotenv import load_dotenv
import argparse
import json
import os
from typing import Union, Set, List, Tuple


class Path:
    def __init__(self, source: str, dest: str, db: nx.classes.digraph.DiGraph, non_dir: bool = False, path: bool = False):
        self.source = source
        self.dest = dest
        self.non_dir = non_dir
        self.path = path
        self.graph = nx.Graph(db) if non_dir else nx.DiGraph(db)

    def _bfs(self) -> Union[List[str], bool]:
        if self.graph.has_node(self.source) and self.graph.has_node(self.dest):
            visited: Set[str] = set()
            Q: List[Tuple[str, List[str]]] = [(self.source, [self.source])]
            while Q:
                node, path = Q.pop(0)
                visited.add(node)

                if node == self.dest:
                    return path

                for child in self.graph[node]:
                    if child not in visited:
                        Q.append((child, path + [child]))
                        visited.add(child)
            return False
        else:
            return False

    def calculate_path(self) -> Union[List[str], int]:
        answer: List[str] | bool = self._bfs()
        if not answer:
            print('path not found')
            return
        if self.path:
            return answer
        else:
            return len(answer) - 1


load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("--from", type=str,
                    dest='source')
parser.add_argument("--to", type=str,
                    dest='dest')
parser.add_argument("-v", action='store_true',
                    dest='path')
parser.add_argument("--non-directed", action='store_true',
                    dest='non_dir')
args = parser.parse_args()


path_to_db = os.environ.get('WIKI_FILE')
if not path_to_db:
    print('database not found')
else:
    with open(path_to_db) as json_data:
        graph = nx.node_link_graph(json.loads(json_data.read()))
        path = Path(args.source, args.dest, graph,
                    args.non_dir, args.path).calculate_path()
        if path:
            print(path)
