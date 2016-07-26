import networkx as nx
import dautil as dl


fb_file = dl.data.SPANFB().load()
G = nx.read_edgelist(fb_file,
                     create_using=nx.Graph(),
                     nodetype=int)

print('Graph Clique Number',
      nx.graph_clique_number(G.subgraph(list(range(2048)))))
