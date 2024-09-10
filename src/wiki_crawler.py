import argparse
import json

import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import logging
import networkx as nx
from networkx.readwrite import json_graph
from typing import Dict, Union, Any, List, Tuple, Set
logging.basicConfig(level=logging.INFO)


class WikiCrawler():
    def __init__(self, page: str = '', recursion: int = 3):
        self.max_depth: int = recursion
        self.first_page: str = 'https://en.wikipedia.org/wiki/' + page
        self.graph = nx.DiGraph()
        self.PAGE_LIMIT: int = 10000

    def __get_link(self, link: str) -> Union[bool, None]:
        try:
            answer = requests.get(link)

        except ConnectionError:
            return None

        if answer.status_code == 200:
            return answer
        else:
            return None

    def __get_link_name(self, link: str) -> str:
        return urllib.parse.unquote(link.split('/')[-1])

    def _traversing_pages(self) -> None:
        temp: List[Tuple[str, int]] = []
        visited: Set[int] = set()
        temp.append((self.first_page, 1))

        while temp:
            curr_link, depth = temp.pop()

            if curr_link not in visited:
                visited.add(curr_link)
                grab = self.__get_link(curr_link)

                if depth > self.max_depth or len(visited) >= 10000:
                    break

                if not grab:
                    continue

                page_name = self.__get_link_name(curr_link)

                logging.info(f"NEW START: {page_name.replace('_', ' ')}")
                soup = BeautifulSoup(grab.text, 'html.parser')
                curr_links = list(set([link.get('href') for link in soup.find("div", {"id": "bodyContent"}
                                                                              ).findAll("a", href=re.compile("(/wiki/)+[A-Za-z0-9_%]+$"))]))
                for link in curr_links:
                    full_link = 'https://en.wikipedia.org/' + link
                    if full_link not in visited:
                        temp.append((full_link, depth+1))
                        curr_name = self.__get_link_name(link)

                        self.graph.add_edge(page_name.replace(
                            '_', ' '), curr_name.replace('_', ' '))
                        logging.info(f"{curr_name.replace('_', ' ')}")

    def find_connected_pages(self) -> None:
        self._traversing_pages()

    def save(self) -> Dict[Any, Any]:
        return json_graph.node_link_data(self.graph)


parser = argparse.ArgumentParser()
parser.add_argument("-p", type=str,
                    dest='start_page',
                    help="wiki page")
parser.add_argument("-d", type=int,
                    default=3,
                    dest='depth',
                    help="recursion depth")

args = parser.parse_args()
graph = WikiCrawler(page=args.start_page, recursion=args.depth)
graph.find_connected_pages()

with open('graph.json', 'w') as file:
    json.dump(graph.save(), file)

with open('.env', 'w') as env_file:
    env_file.write(f"WIKI_FILE=./graph.json\n")
