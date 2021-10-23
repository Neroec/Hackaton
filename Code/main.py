import osmnx as ox


def generate_edges():
    G = ox.graph_from_place('Lipetsk, Russia', 'drive',
                            custom_filter='["highway"~"residential|tertiary|secondary|primary"]',
                            )
    _, edges = ox.graph_to_gdfs(G)
    f = open("edges.txt", 'w')
    for edge in edges.values:
        coords = edge[5].coords # 5 for custom | 6 for drive
        line = "["
        for coord in coords:
            line += "[{x}, {y}], ".format(x=coord[1], y=coord[0])
        line += "],\n"
        f.write('{l}'.format(l=line))


def generate_nodes():
    G = ox.graph_from_place('Lipetsk, Russia', 'drive',
                            custom_filter='["highway"~"residential|tertiary|secondary|primary"]')
    nodes, _ = ox.graph_to_gdfs(G)
    f = open("nodes.txt", 'w')
    for node in nodes.values:
        f.write('[{x}, {y}],\n'.format(x=node[0], y=node[1]))


generate_edges()