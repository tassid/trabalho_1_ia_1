import pygame
import time
import os

class Node:
    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0  # Custo para mover do nó inicial para o nó atual
        self.h = 0  # Custo para mover do nó atual para o nó final
        self.f = 0  # Custo total

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    # Cria nó inicial e final
    start_node = Node(start, None)
    end_node = Node(end, None)

    # Inicializa ambas listas aberta e fechada
    open_list = []
    closed_list = []

    # Adiciona o nó inicial
    open_list.append(start_node)

    # Loop até que a lista aberta esteja vazia
    while len(open_list) > 0:
        # Pega o nó atual
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Remove o nó atual da lista aberta e adiciona à lista fechada
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Verifica se chegamos ao fim, retorna o caminho
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Retorna o caminho invertido

        # Gera filhos
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacente quadrado (cima, baixo, esquerda, direita)

            # Pega a posição do nó
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Verifica se está dentro do labirinto
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Verifica se é uma parede
            if maze[node_position[0]][node_position[1]] != ' ':
                continue

            # Cria novo nó
            new_node = Node(node_position, current_node)

            # Adiciona
            children.append(new_node)

        # Loop através dos filhos
        for child in children:
            # Filho está na lista fechada
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Cria os valores f, g e h do filho
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Filho já está na lista aberta e o g é maior
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Adiciona o filho à lista aberta
            open_list.append(child)

def draw_maze(screen, maze):
    cell_size = 30
    wall_color = (0, 0, 0)
    path_color = (255, 255, 255)
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == '▓':
                pygame.draw.rect(screen, wall_color, (col_idx * cell_size, row_idx * cell_size, cell_size, cell_size))
            elif cell == ' ':
                pygame.draw.rect(screen, path_color, (col_idx * cell_size, row_idx * cell_size, cell_size, cell_size))

def main():
    pygame.init()

    maze = [['▓', '▓', '▓', '▓', '▓'],
            ['▓', ' ', ' ', '$', '▓'],
            ['▓', ' ', '▓', ' ', '▓'],
            ['▓', '☺', ' ', '$', '▓'],
            ['▓', '▓', '▓', '▓', '▓']]

    start = (3, 1)
    end = (1, 3)

    path = astar(maze, start, end)

    if path is None:
        print("Não foi encontrado um caminho válido.")
        return

    screen_width = len(maze[0]) * 30
    screen_height = len(maze) * 30

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("A* Maze Solver")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for step in path:
            maze[step[0]][step[1]] = "☺"
            draw_maze(screen, maze)
            pygame.display.update()
            time.sleep(0.5)

    pygame.quit()

if __name__ == '__main__':
    main()
