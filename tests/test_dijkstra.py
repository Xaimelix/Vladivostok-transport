"""
Тесты для алгоритма Дейкстры
"""
from app.modules.path import dijkstra


class TestDijkstra:
    """Тесты для функции dijkstra из модуля path."""

    def test_simple_path(self):
        """Простой тест с линейным графом."""
        # Граф: 0 -> 1 -> 2
        graph = {
            0: [(1, 1)],
            1: [(1, 2)],
            2: []
        }
        result = dijkstra(0, 2, graph)
        # Восстанавливаем путь
        path = []
        cur = 2
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0, 1, 2]

    def test_direct_connection(self):
        """Тест с прямым соединением между узлами."""
        # Граф: 0 напрямую соединён с 1 (вес 5)
        graph = {
            0: [(5, 1)],
            1: []
        }
        result = dijkstra(0, 1, graph)
        path = []
        cur = 1
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0, 1]

    def test_shortest_path_selection(self):
        """Тест выбора кратчайшего пути среди нескольких вариантов."""
        # Граф:
        # 0 -> 1 (вес 10)
        # 0 -> 2 (вес 1)
        # 2 -> 1 (вес 1)
        # Кратчайший путь: 0 -> 2 -> 1 (вес 2), а не 0 -> 1 (вес 10)
        graph = {
            0: [(10, 1), (1, 2)],
            1: [],
            2: [(1, 1)]
        }
        result = dijkstra(0, 1, graph)
        path = []
        cur = 1
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0, 2, 1]

    def test_same_start_end(self):
        """Тест когда начальная и конечная точки совпадают."""
        graph = {
            0: [(1, 1)],
            1: []
        }
        result = dijkstra(0, 0, graph)
        # Путь должен содержать только начальный узел
        path = []
        cur = 0
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0]

    def test_complex_graph(self):
        """Тест со сложным графом."""
        # Граф:
        #       2
        #     /   \
        # 0 -1- 1 -1- 3
        #     \     /
        #       4
        # Кратчайший путь от 0 до 3: 0 -> 1 -> 3 (вес 2)
        graph = {
            0: [(1, 1), (4, 4)],
            1: [(1, 0), (1, 3), (2, 2)],
            2: [(2, 1), (1, 3)],
            3: [(1, 1), (1, 2)],
            4: [(4, 0)]
        }
        result = dijkstra(0, 3, graph)
        path = []
        cur = 3
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0, 1, 3]

    def test_disconnected_graph(self):
        """Тест с несвязным графом (конечный узел недостижим)."""
        # Граф: 0 -> 1, но 2 изолирован
        graph = {
            0: [(1, 1)],
            1: [],
            2: []
        }
        result = dijkstra(0, 2, graph)
        # Путь не будет найден, 2 не будет в visited как достижимый
        assert 2 not in result or result.get(2) is None

    def test_multiple_edges_same_node(self):
        """Тест с несколькими рёбрами из одного узла."""
        # Граф: из 0 есть рёбра к 1, 2, 3
        graph = {
            0: [(5, 1), (3, 2), (7, 3)],
            1: [],
            2: [],
            3: []
        }
        result = dijkstra(0, 2, graph)
        path = []
        cur = 2
        while cur is not None:
            path.append(cur)
            cur = result.get(cur)
        path.reverse()
        assert path == [0, 2]
