import pandas as pd
from copy import deepcopy

def find_all_paths(graph, start_vertex, end_vertex, path=[]):
    """ find all paths from start_vertex to
        end_vertex in graph """
    path = path + [start_vertex]
    if start_vertex == end_vertex:
        return [path]
    if start_vertex not in graph:
        return []
    paths = []
    for vertex in graph[start_vertex]:
        if vertex not in path:
            extended_paths = find_all_paths(graph, vertex, end_vertex, path)
            for p in extended_paths:
                paths.append(p)
    return paths

def diameter(graph):
    """ calculates the diameter of the graph """
    v = list(graph.keys())
    pairs = [(v[i], v[j]) for i in range(len(v)) for j in range(i+1, len(v)-1)]
    smallest_paths = []
    for (start, end) in pairs:
        paths = find_all_paths(graph, start, end)
        try:
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)
        except:
            pass

    # longest path is at the end of list,
    # i.e. diameter corresponds to the length of this path
    dia = len(smallest_paths[-1])
    return dia

def prepare_dict(graphs):
    """ cleans our dict from
        {
            "Germany": {"out_links": ["Netherland"]}
        }
        to
        {
            "Germany": ["Netherland"]
        }
    """
    new_dict = dict()
    for key, values in graphs.items():
        new_dict[key] = values['out_links']
    return new_dict


def add_empty_node(dict_of_link):
    pure_dict = deepcopy(dict_of_link)
    all_links = set()
    for key, values in pure_dict.items():
        all_links.add(key)
        all_links |= set(values)
    for key in all_links:
        if key not in pure_dict:
            pure_dict[key] = []
    return pure_dict


def read_file(file_name):
    """ read given file and returns the content"""
    return pd.HDFStore(file_name)

if __name__ == "__main__":
    """ entry point of the application"""

    store = read_file("store.h5")
    df = store['df2']
    # Dictionary of article names and its associated article text in list form
    name_assoctext_dict = df.set_index('name').T.to_dict()
    new_dict = prepare_dict(name_assoctext_dict)
    graph = add_empty_node(new_dict)
    print("The diameter of our outlinks is: " , diameter(graph))
