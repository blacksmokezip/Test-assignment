import random
from collections import deque
import matplotlib.pyplot as plt

from test_assignment.constants import EMPTY, BLOCKED, SIGNAL, TOWER


class CityGrid:

    def __init__(self, n: int, m: int, block_coverage=0.3) -> None:
        """
        Инициализация сетки города.

        :param n: Количество строк в сетке.
        :param m: Количество столбцов в сетке.
        :param block_coverage: Доля заблокированных блоков в сетке.
        """
        self.n = n
        self.m = m
        self.grid = [[EMPTY for _ in range(m)] for _ in range(n)]
        self.populate_blocked_areas(block_coverage)

    def populate_blocked_areas(self, block_coverage) -> None:
        """
        Заполняет сетку заблокированными блоками.

        :param block_coverage: Доля заблокированных блоков в сетке.
        """
        total_blocks = self.n * self.m
        blocked_count = int(total_blocks * block_coverage)

        while blocked_count > 0:
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.m - 1)

            if self.grid[i][j] == EMPTY:
                self.grid[i][j] = BLOCKED
                blocked_count -= 1

    def display_grid(self) -> None:
        """
        Выводит сетку на экран.
        """
        print("_")
        for row in self.grid:
            print('|', ' '.join(map(str, row)), '|')
        print("_")

    def place_tower(self, x: int, y: int, R: int) -> None:
        """
        Размещает башню и визуализирует ее покрытие.

        :param x: Координата X башни.
        :param y: Координата Y башни.
        :param R: Радиус действия башни.
        """
        for i in range(max(0, x - R), min(self.n, x + R + 1)):
            for j in range(max(0, y - R), min(self.m, y + R + 1)):
                if i == x and j == y:
                    self.grid[x][y] = TOWER
                elif self.grid[i][j] != BLOCKED:  # Проверка, что блок не заблокирован
                    self.grid[i][j] = SIGNAL  # Пометка покрытия башней

    def optimize_towers(self, R: int) -> list:
        """
        Размещает башни для оптимального покрытия.

        :param R: Радиус действия каждой башни.
        """
        covered = [[False for _ in range(self.m)] for _ in range(self.n)]
        towers = []

        def can_place_tower(x, y):
            # Проверяет, можно ли разместить башню на данном блоке.
            return self.grid[x][y] == BLOCKED

        def update_coverage(x, y):
            # Обновляет покрытие после размещения башни.
            for i in range(max(0, x - R), min(self.n, x + R + 1)):
                for j in range(max(0, y - R), min(self.m, y + R + 1)):
                    covered[i][j] = True

        def get_coverage_count(x, y):
            # Считает количество покрываемых башней блоков.
            count = 0
            for i in range(max(0, x - R), min(self.n, x + R + 1)):
                for j in range(max(0, y - R), min(self.m, y + R + 1)):
                    if not covered[i][j]:
                        count += 1
            return count

        while True:
            max_coverage = 0
            best_location = None

            for x in range(self.n):
                for y in range(self.m):
                    if can_place_tower(x, y):
                        coverage = get_coverage_count(x, y)
                        if coverage > max_coverage:
                            max_coverage = coverage
                            best_location = (x, y)

            if best_location is None:
                break  # Все доступные блоки покрыты

            towers.append(best_location)
            update_coverage(*best_location)

        for x, y in towers:
            self.place_tower(x, y, R)

        return towers

    def find_most_reliable_path(self, R: int, towers: list, start: tuple, end: tuple) -> list:
        """
        Находит самый надежный путь между двумя башнями.
        :param R: радиус башен
        :param towers: все башни
        :param start: Координаты начальной башни (x, y).
        :param end: Координаты конечной башни (x, y).
        :return: Список координат башен, составляющих путь.
        """

        def in_range(x1, y1, x2, y2, R):
            return abs(x1 - x2) <= 2 * R + 1 and abs(y1 - y2) <= 2 * R + 1

        # Создание графа связей между башнями
        graph = {tower: [] for tower in towers}
        for tower in towers:
            for neighbour in towers:
                if tower != neighbour and in_range(*tower, *neighbour, R):
                    graph[tower].append(neighbour)
        # Алгоритм BFS для поиска пути
        queue = deque([start])
        visited = {tower: False for tower in towers}
        visited[start] = True
        parents = {tower: None for tower in towers}

        while queue:
            current = queue.popleft()
            if current == end:
                break
            for neighbour in graph[current]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    parents[neighbour] = current
                    queue.append(neighbour)

        # Восстановление пути
        path = []
        while end is not None:
            path.append(end)
            end = parents[end]
        path.reverse()

        return path if path[0] == start else []

    def visualize_city(self, towers=None, path=None) -> None:
        """
        Визуализирует заблокированные блоки,
        башни, области покрытия и пути передачи данных.
        :param towers: Все башни.
        :param path: Список координат башен, составляющих путь.
        """
        fig, ax = plt.subplots()

        # Визуализация заблокированных блоков
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == BLOCKED:
                    ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color="red"))

        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == SIGNAL:
                    ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color="green"))

        # Визуализация башен
        if towers:
            for tower in towers:
                row, col = tower
                ax.add_patch(plt.Rectangle((col, self.n - row - 1), 1, 1, color="blue"))

        # Визуализация пути передачи данных
        if path:
            for i in range(len(path) - 1):
                tower1 = path[i]
                tower2 = path[i + 1]
                row1, col1 = tower1
                row2, col2 = tower2
                plt.plot(
                    [col1 + 0.5, col2 + 0.5],
                    [self.n - row1 - 0.5, self.n - row2 - 0.5],
                    color="red",
                )

        ax.set_aspect("equal")
        ax.set_xlim(0, self.m)
        ax.set_ylim(0, self.n)
        plt.gca().invert_yaxis()

        ax.set_title("Сетка города с башнями, блоками, областью покрытия и путями передачи данных")
        ax.set_xlabel("Столбцы")
        ax.set_ylabel("Строки")

        plt.show()
