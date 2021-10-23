import osmnx as ox


def generate_nodes_for_map(nodes):
    f = open("nodes.txt", 'w')
    for node in nodes.values:
        f.write('[{x}, {y}],\n'.format(x=node[0], y=node[1]))


def generate_edges_for_map(edges):
    f = open("edges.txt", 'w')
    for edge in edges.values:
        coords = edge[5].coords # 5 for custom | 6 for drive
        if (isinstance(edge[1], str)):
            type = edge[1]
        else:
            type = edge[1][0]
        line = "['{type}', {length}, ".format(type=type, length=edge[3])
        for coord in coords:
            line += "[{x}, {y}], ".format(x=coord[1], y=coord[0])
        line += "],\n"
        f.write('{l}'.format(l=line))


def generate_nodes_for_algo(nodes):
    f = open("nodes2.txt", 'w')
    i = 0;
    for node in nodes.values:
        f.write('[{i}, [{x}, {y}]],\n'.format(i=i, x=node[0], y=node[1]))
        i += 1


def generate_edges_for_algo(edges):
    f = open("edges2.txt", 'w')
    i = 0
    for edge in edges.values:
        coords = edge[5].coords # 5 for custom | 6 for drive
        line = "[{id}, {length}, 1, ".format(id=i, length=edge[3])
        i += 1
        ind = len(coords) - 1
        line += "[{x1}, {y1}], [{x2}, {y2}]],\n".format(x1=coords[0][1], y1=coords[0][0],
                                                        x2=coords[ind][1], y2=coords[ind][0])
        f.write('{l}'.format(l=line))


G = ox.graph_from_place('Lipetsk, Russia', 'drive',
                            custom_filter='["highway"~"residential|tertiary|secondary|primary"]')
nodes, edges = ox.graph_to_gdfs(G)
#generate_edges_for_map(edges)
generate_edges_for_algo(edges)
#generate_nodes(nodes)
#generate_nodes_for_algo(nodes)
