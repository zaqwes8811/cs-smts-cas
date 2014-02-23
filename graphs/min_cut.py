# coding: utf-8

import copy
import random


def get_random_edge(source_graph):
    """
    Keys is positive integer.

    Как выбрать если схлопываем узлы?
    """

    keys = source_graph.keys()

    source_v = random.randint(1, len(keys))

    connections = source_graph[source_v]
    end_v = connections[random.randint(0, len(connections) - 1)]
    print end_v, connections, source_graph

    return source_v, end_v


def edge_contraction(graph, edge, super_vertices):
    begin = edge[0]
    end = edge[1]
    key_begin = begin.idx
    key_end = end.idx

    # Если нужно вставляем в набор супервершин исходного узла
    super_for_begin = begin.super_vertex
    super_for_end = end.super_vertex
    if not super_for_begin:
        begin.super_vertex = key_begin

    if key_begin not in super_vertices \
            and key_end not in super_vertices:
        super_vertices[key_begin] = []

        # Добавляем обе
        super_vertices[key_begin].append(key_begin)
        super_vertices[key_begin].append(key_end)

        # Удаляем ссылки друг на друга в пределах суперузла.
        # Здесь только для двух точек, вернее для суперузла.
    else:
        pass

    print super_vertices


    # Удаляем из вершир ребра ссылик на друг-друга

    # Вершина может стать пустой? Тогда может ее удалять? Из списка вершин и супер вершины

    # begin <- end
    #source_vs = graph[begin]
    #end_vs = graph[end]

    # Дублированные удалять нельзя, но нужно удалять петли
    #source_vs.extend(end_vs)

    #graph[begin] = filter(lambda a: a != begin, graph[begin])

    #del graph[end]  # Ссылки содержатся в списках


def main():
    """
    http://en.wikipedia.org/wiki/Karger%27s_algorithm

    Полагаем что доступ по ключу O(n)

    Как сохранить информацию о ребре, а не просто их схлопнуть?

    Использовать стопки, но это дополнительное место - O(n^2)!!

    Как хранить ссылки? Числа или сразу объекты?
    """

    class Vertex(object):
        def __init__(self, ends, source):
            self.end_points = ends
            self.super_vertex = None
            self.idx = source

    source_graph = {1: [2, 4], 2: [1, 4, 3], 3: [2, 4], 4: [1, 2, 3]}
    vertices = {}
    edges = []  # Копия со ссылками - по ней генерируем ребро - если вершина пустая
        # удаляем - это обеспечит попадание в ребро при случайном выборе.

    for k, v in source_graph.items():
        vertices[k] = Vertex(v, k)

    super_vertices = {}  # супервершины, когда будут появляться

    norm_v = len(source_graph)  # развязка появилась, но какие узлы остались?
    # Или может мы просто удаляем ребро, а ничего не схлопываем?
    # Не придется схлопнуть

    # One iteration
    #while norm_v > 2:
    edge = (vertices[1], vertices[2])#get_random_edge(source_graph)
    edge_contraction(vertices, edge, super_vertices)
    #    norm_v -= 1

    print source_graph


def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r



main()
#benchmark_delete_key()
