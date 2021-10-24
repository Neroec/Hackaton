from flask import Flask
import osmnx as ox
from flask_cors import CORS, cross_origin
import json
import copy
from queue import PriorityQueue


G = ox.graph_from_place('Lipetsk, Russia', 'drive',
                            custom_filter='["highway"~"residential|tertiary|secondary|primary"]')

nodes, edges = ox.graph_to_gdfs(G)

def generate_edges_for_map(edges):
    res = []
    for edge in edges.values:
        coords = edge[5].coords # 5 for custom | 6 for drive
        if (isinstance(edge[1], str)):
            type = edge[1]
        else:
            type = edge[1][0]
        line = "['{type}', {length}, ".format(type=type, length=edge[3])
        curRes = [type, edge[3]]
        for coord in coords:
            curRes.append([coord[1], coord[0]])
            line += "[{x}, {y}], ".format(x=coord[1], y=coord[0])
        line += "],\n"
        res.append(curRes)
    return res

def generate_edges_for_algo(edges):
    res = []
    i = 0
    for edge in edges.values:
        coords = edge[5].coords # 5 for custom | 6 for drive
        line = "[{id}, {length}, 1, ".format(id=i, length=edge[3])
        i += 1
        ind = len(coords) - 1
        line += "[{x1}, {y1}], [{x2}, {y2}]],\n".format(x1=coords[0][1], y1=coords[0][0],
                                                        x2=coords[ind][1], y2=coords[ind][0])
        res.append([i - 1, edge[3], 1, [coords[0][1], coords[0][0]], [coords[ind][1], coords[ind][0]]])
    return res

def generate_nodes_for_algo(nodes):
    res = []
    i = 0;
    for node in nodes.values:
        # f.write('[{i}, [{x}, {y}]],\n'.format(i=i, x=node[0], y=node[1]))
        res.append([i, [node[0], node[1]]])
        i += 1
    return res

garage = 2745


def find_comps(nodes1, edges2, edges_imp):
    map_imp = {
        'primary': 2,
        'secondary': 1,
        'residential': 0
    }

    no2id = {tuple(i[1]): i[0] for i in nodes1}

    id2no = {i[0]: tuple(i[1]) for i in nodes1}
    id2edge = {i[0]: (i[1], i[2], tuple(i[3]), tuple(i[4])) for i in edges2}
    nodes2edge = {(tuple(i[3]), tuple(i[4])): i[0] for i in edges2}

    adj_list = {}
    inc_list = {}

    node_imp = []

    for edge in edges_imp:
        imp = edge[0]

        # nodes2edge[(tuple(edge[2]), tuple(edge[3]))]: edge[0]
        f, t = tuple(edge[2]), tuple(edge[3])
        if f not in no2id.keys():
            continue
        if t not in no2id.keys():
            continue
        f_id = no2id[f]
        t_id = no2id[t]
        if imp in map_imp.keys():
            node_imp.append((map_imp[imp], f_id))
            node_imp.append((map_imp[imp], t_id))
        else:
            node_imp.append((-1, t_id))
            node_imp.append((-1, f_id))

    # print(node_imp)
    node_imp.sort()
    for edge_id in id2edge.keys():
        edge = id2edge[edge_id]
        f, t = tuple(edge[2]), tuple(edge[3])
        f_id, t_id = no2id[f], no2id[t]
        if f_id not in adj_list.keys():
            adj_list[f_id] = [t_id]
        else:
            adj_list[f_id].append(t_id)

        if t_id not in adj_list.keys():
            adj_list[t_id] = [f_id]
        else:
            adj_list[t_id].append(f_id)

        if f_id not in inc_list.keys():
            inc_list[f_id] = [edge_id]
        else:
            inc_list[f_id].append(edge_id)

        if t_id not in inc_list.keys():
            inc_list[t_id] = [edge_id]
        else:
            inc_list[t_id].append(edge_id)

    leafs = []
    for node_id in adj_list.keys():
        if len(adj_list[node_id]) == 1:
            leafs.append(node_id)

    max_weight = 16000
    n_comp = 0
    max_comp = 103
    used_edges = set()
    node_queue = list(id2no.keys())
    all_comps = []
    components = []
    num_iter = 0
    nodes_used = set()
    while n_comp != max_comp and len(used_edges) != len(id2edge) and num_iter < 1000:
        # cur = leafs
        # start_node = node_queue.pop()
        start_node = -1
        while len(node_imp) != 0:
            start_node = node_imp.pop()
            start_node = start_node[1]
            if start_node not in nodes_used:
                break
        if start_node == -1:
            break

        dist_to = {start_node: 0}
        cur_weight = 0
        cur_nodes = [start_node]
        cur_edges = []
        while True:
            # print(1)
            mn = 10000
            mn_id = -1
            selected_node = -1
            to = -1
            for node in cur_nodes:
                # if dist_to[]
                for inc_edge in inc_list[node]:
                    if inc_edge not in used_edges:
                        if id2edge[inc_edge][0] + dist_to[node] < mn:
                            mn = id2edge[inc_edge][0] + dist_to[node]
                            mn_id = inc_edge
                            selected_node = node
                            edge = id2edge[inc_edge]
                            if edge[2] == selected_node:
                                to = no2id[edge[3]]
                            else:
                                to = no2id[edge[2]]
                    else:
                        continue
            if mn_id == -1:
                break
            if cur_weight + id2edge[mn_id][0] < max_weight:
                used_edges.add(mn_id)
                cur_weight += id2edge[mn_id][0]
                edge = id2edge[mn_id]
                cur_edges.append(mn_id)
                cur_nodes.append(to)
                nodes_used.add(to)
                nodes_used.add(selected_node)
                if to not in dist_to.keys():
                    dist_to[to] = dist_to[selected_node] + id2edge[mn_id][0]
                else:
                    dist_to[to] = min(dist_to[to], dist_to[selected_node] + id2edge[mn_id][0])
            else:
                break
        if len(cur_edges) == 0:
            pass
        else:
            n_comp += 1
            components.append([cur_weight, cur_edges])
        a = 1
        num_iter += 1

    # print(components)
    # with open('test.json', 'w') as f:
    #     json.dump(components, f)
    # print(id2edge)
    return components


def build_graph(nodes1, edges2):
    no2id = {tuple(i[1]): i[0] for i in nodes1}

    id2edge = {i[0]: (i[1], i[2], tuple(i[3]), tuple(i[4])) for i in edges2}

    graph = {}

    for edge_id in id2edge.keys():
        edge = id2edge[edge_id]
        f, t = tuple(edge[2]), tuple(edge[3])
        f_id, t_id = no2id[f], no2id[t]
        if f_id not in graph.keys():
            graph[f_id] = {t_id: edge[0]}
        else:
            graph[f_id][t_id] = edge[0]
    return graph


def djikstra(source, graph):
    parents = {}
    costs = {}
    costs[source] = 0
    used = set()
    q = PriorityQueue()
    q.put((0, source))
    while not q.empty():
        cur = q.get()
        cost, v = cur
        if v in used:
            continue
        if v not in graph.keys():
            continue
        for to in graph[v]:
            if to in costs.keys():
                if costs[to] > costs[v] + cost:
                    parents[to] = v
                    costs[to] = costs[v] + cost
                    q.put((costs[to], to))
            else:
                costs[to] = costs[v] + cost
                q.put((costs[to], to))
                parents[to] = v
    return parents, costs


def get_path(start, end, parents):
    cur = end
    path = []
    while cur != start:
        path.append(cur)
        cur = parents[cur]
    path.append(start)
    return path


def find_paths_to_comp(components, nodes1, edges2, garage=2745):
    g = build_graph(nodes1, edges2)
    # print(g)
    id2edge = {i[0]: (i[1], i[2], tuple(i[3]), tuple(i[4])) for i in edges2}
    no2id = {tuple(i[1]): i[0] for i in nodes1}
    id2node = {i[0]: tuple(i[1]) for i in nodes1}
    parents, costs = djikstra(garage, g)
    nodes2edge = {(tuple(i[3]), tuple(i[4])): i[0] for i in edges2}

    paths = []
    for comp in components:
        edges = comp[1]
        mn = 10000000
        mn_id = -1
        for edge_id in edges:
            edge = id2edge[edge_id]
            f, t = tuple(edge[2]), tuple(edge[3])
            f_id, t_id = no2id[f], no2id[t]
            if f_id in costs.keys():
                if costs[f_id] < mn:
                    mn = costs[f_id]
                    mn_id = f_id
            if t_id in costs.keys():
                if costs[t_id] < mn:
                    mn = costs[t_id]
                    mn_id = t_id
        if mn_id == -1:
            paths.append([])
            continue

        min_path = get_path(garage, mn_id, parents)[::-1]
        edges_path = get_edges_path(min_path, nodes2edge, id2edge, id2node)
        # print(edges_path)
        paths.append(edges_path)
    return paths


def get_edges_path(min_path, nodes2edge, id2edge, id2node):
    start = min_path[0]
    ret = []
    for i in range(1, len(min_path)):
        cur = min_path[i]
        try:
            f = id2node[start]
            t = id2node[cur]

            # print(f, t)
            node_id = nodes2edge[(t, f)]
            ret.append(node_id)
        except:
            pass
        start = cur

    return ret


# print(json.dump(components))

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/roads")
def get_roads():
    return json.dumps(generate_edges_for_map(edges))

@app.route("/routes")
def get_routes():
    nodes1 = generate_nodes_for_algo(nodes)
    edges2 = generate_edges_for_algo(edges)
    edges_imp = generate_edges_for_map(edges)

    return json.dumps(find_comps(nodes1, edges2, edges_imp))

@app.route("/edges")
def get_edges():
    edges2 = generate_edges_for_algo(edges)

    return json.dumps(edges2)