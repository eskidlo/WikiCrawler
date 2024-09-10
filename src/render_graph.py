import json
import os
from pyvis.network import Network
import networkx as nx
from dotenv import load_dotenv


load_dotenv()
with open(os.environ.get('WIKI_FILE'), 'r') as file:
    graph = nx.node_link_graph(json.load(file), directed=True)


nt = Network('1000px', '1000px')
nt.from_nx(graph)

for node in nt.nodes:
    node['label'] = node['label']
    node['size'] = node['size'] + (graph.in_degree(node['id']) * 10)

nt.show('wiki_graph.html', notebook=False)
