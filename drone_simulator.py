import numpy as np
import cv2
import random

# Grid setup
GRID_SIZE = 10
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DRONE_COLOR = (0, 255, 0)
GOAL_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (50, 50, 50)

grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Random obstacles
for _ in range(15):
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    grid[y][x] = 1

def get_empty_cell():
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == 0:
            return x, y

drone_x, drone_y = get_empty_cell()
goal_x, goal_y = get_empty_cell()

# Movement keys
moves = {
    ord('w'): (0, -1),
    ord('s'): (0, 1),
    ord('a'): (-1, 0),
    ord('d'): (1, 0),
}

def draw_env():
    img = np.ones((WINDOW_SIZE, WINDOW_SIZE, 3), dtype=np.uint8) * 255
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 1:
                cv2.rectangle(img, (x*CELL_SIZE, y*CELL_SIZE), ((x+1)*CELL_SIZE, (y+1)*CELL_SIZE), OBSTACLE_COLOR, -1)
    cv2.rectangle(img, (goal_x*CELL_SIZE, goal_y*CELL_SIZE), ((goal_x+1)*CELL_SIZE, (goal_y+1)*CELL_SIZE), GOAL_COLOR, -1)
    cv2.rectangle(img, (drone_x*CELL_SIZE, drone_y*CELL_SIZE), ((drone_x+1)*CELL_SIZE, (drone_y+1)*CELL_SIZE), DRONE_COLOR, -1)
    return img

# Run
while True:
    img = draw_env()
    cv2.imshow("Drone Grid Navigation", img)
    key = cv2.waitKey(150)

    if key == 27: break
    if key in moves:
        dx, dy = moves[key]
        nx, ny = drone_x + dx, drone_y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] != 1:
            drone_x, drone_y = nx, ny

    if (drone_x, drone_y) == (goal_x, goal_y):
        print("🎯 Goal Reached!")
        break

cv2.destroyAllWindows()
