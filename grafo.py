from no import No
from networkx import Graph, draw
from pylab import show


def format_string(string):
    string = string.split(" ")
    neighbors = [int(no) for no in string[1:]]
    return (int(string[0]), neighbors)


def print_no(no):
    print("\n")
    print("---------------------------------------------")
    print("- {}: {}                                     ".format("No",
                                                                 no.id))
    print("- {}: {}                                     ".format("Visited",
                                                                 no.visited))
    print("- {}: {}                                     ".format("Neighbors",
                                                                 no.neighbors))
    print("---------------------------------------------")


def BFS(graph):
    for no in graph:
        if no.visited is False:
            no.visited = True
            stack = no.neighbors
            for id in stack:
                if graph[id-1].visited is False:
                    graph[id-1].visited = True
                    stack.extend(graph[id-1].neighbors)
                else:
                    continue
        else:
            continue


def verify_no(no):
    if no.visited is True:
        return True
    else:
        return False


def draw_graph(graph):
    list_edges = []
    for no in graph:
        for nei in no.neighbors:
            tup = (no.id, nei)
            list_edges.append(tup)

    g_draw = Graph()
    g_draw.add_edges_from(list_edges, color='red')
    draw(g_draw, with_labels=True, font_weight='bold')
    show()


def main():
    inputs = []
    graph = []
    length = int(input("Write the graph's length: "))
    for count in range(length):
        line = str(input("Write graph with 'id' + 'list of neighbors': "))
        formated_input = format_string(line)
        inputs.append(formated_input)

    for id, neighbors in inputs:
        no = No(id)
        no.neighbors = neighbors
        graph.append(no)

    BFS(graph)
    results = [verify_no(no) for no in graph]
    if all(results):
        print("All connected")
    else:
        print("Not connected")

    draw_graph(graph)
    # TODO make BFS and DFS algorithm in graph
    # for no in graph:
    #     print_no(no)


if __name__ == "__main__":
    main()
