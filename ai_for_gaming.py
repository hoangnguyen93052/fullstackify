import numpy as np
import random
import heapq

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width))

    def place_obstacle(self, x, y):
        if self.is_within_bounds(x, y):
            self.board[y][x] = 1

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def display(self):
        print(self.board)

class Agent:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def get_position(self):
        return self.position

class AStar:
    def __init__(self, start, goal, gameboard):
        self.start = start
        self.goal = goal
        self.gameboard = gameboard

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar_search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == self.goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)

                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if self.gameboard.is_within_bounds(*neighbor) and self.gameboard.board[neighbor[1]][neighbor[0]] == 0:
                neighbors.append(neighbor)
        
        return neighbors

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

class Game:
    def __init__(self, board_width, board_height):
        self.board = GameBoard(board_width, board_height)
        self.agents = {}
        self.game_over = False

    def add_agent(self, name, position):
        agent = Agent(name, position)
        self.agents[name] = agent

    def move_agent(self, name, new_position):
        if name in self.agents:
            agent = self.agents[name]
            if self.board.is_within_bounds(*new_position) and self.board.board[new_position[1]][new_position[0]] == 0:
                agent.move(new_position)

    def place_obstacle(self, x, y):
        self.board.place_obstacle(x, y)

    def display_board(self):
        for agent in self.agents.values():
            pos_x, pos_y = agent.get_position()
            self.board.board[pos_y][pos_x] = 2  # Mark agent's position with 2
        self.board.display()

    def find_path(self, agent_name, goal):
        if agent_name in self.agents:
            start = self.agents[agent_name].get_position()
            astar = AStar(start, goal, self.board)
            path = astar.astar_search()
            return path
        return None

    def play_game(self):
        while not self.game_over:
            self.display_board()
            # Here we would have game logic to continue the game

def main():
    game = Game(10, 10)
    game.place_obstacle(3, 3)
    game.place_obstacle(3, 4)
    game.place_obstacle(3, 5)
    game.add_agent("Player1", (0, 0))
    game.add_agent("Player2", (5, 5))
    
    path = game.find_path("Player1", (7, 8))
    print(f"Path for Player1 to (7, 8): {path}")

    game.move_agent("Player1", (1, 1))
    game.move_agent("Player2", (4, 4))

main()