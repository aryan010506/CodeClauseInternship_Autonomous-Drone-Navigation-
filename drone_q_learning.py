import numpy as np
import cv2
import random

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
EPISODES = 2000

# Rewards
REWARD_GOAL = 10
REWARD_OBSTACLE = -10
REWARD_MOVE = -1

# Actions: [Up, Down, Left, Right]
actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Q-table: [y][x][action]
q_table = np.zeros((GRID_SIZE, GRID_SIZE, 4))

# Draw the environment
def draw_env(grid, drone_pos, goal_pos):
    img = np.ones((WINDOW_SIZE, WINDOW_SIZE, 3), dtype=np.uint8) * 255
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = (255, 255, 255)
            if grid[y][x] == 1:
                color = (50, 50, 50)  # Obstacle
            cv2.rectangle(img, (x * CELL_SIZE, y * CELL_SIZE),
                          ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), color, -1)

    dx, dy = drone_pos
    gx, gy = goal_pos
    cv2.rectangle(img, (gx * CELL_SIZE, gy * CELL_SIZE),
                  ((gx + 1) * CELL_SIZE, (gy + 1) * CELL_SIZE), (0, 0, 255), -1)  # Goal
    cv2.rectangle(img, (dx * CELL_SIZE, dy * CELL_SIZE),
                  ((dx + 1) * CELL_SIZE, (dy + 1) * CELL_SIZE), (0, 255, 0), -1)  # Drone

    # Grid lines
    for i in range(0, WINDOW_SIZE, CELL_SIZE):
        cv2.line(img, (i, 0), (i, WINDOW_SIZE), (0, 0, 0), 1)
        cv2.line(img, (0, i), (WINDOW_SIZE, i), (0, 0, 0), 1)

    return img

# Get a random empty cell
def get_empty_cell(grid):
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == 0:
            return (x, y)

# Create grid with obstacles
def create_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for _ in range(15):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[y][x] = 1  # obstacle
    return grid

# Training
print("📚 Training AI agent...")
for ep in range(EPISODES):
    grid = create_grid()
    drone_pos = get_empty_cell(grid)
    goal_pos = get_empty_cell(grid)

    for _ in range(100):  # Steps per episode
        x, y = drone_pos
        gx, gy = goal_pos

        # Epsilon-greedy action selection
        if random.uniform(0, 1) < 0.1:
            action = random.randint(0, 3)
        else:
            action = np.argmax(q_table[y][x])

        dx, dy = actions[action]
        new_x, new_y = x + dx, y + dy

        # Bounds check
        if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            reward = REWARD_OBSTACLE
            new_x, new_y = x, y
        elif grid[new_y][new_x] == 1:
            reward = REWARD_OBSTACLE
            new_x, new_y = x, y
        elif (new_x, new_y) == goal_pos:
            reward = REWARD_GOAL
        else:
            reward = REWARD_MOVE

        # Update Q-table
        old_q = q_table[y][x][action]
        future_q = np.max(q_table[new_y][new_x])
        q_table[y][x][action] = old_q + 0.1 * (reward + 0.9 * future_q - old_q)

        drone_pos = (new_x, new_y)
        if drone_pos == goal_pos:
            break

    if ep % 500 == 0:
        print(f"Episode {ep} done")

print("✅ Training complete.")

# Save Q-table
np.save("q_table.npy", q_table)

# Test trained agent
print("🧠 Running trained agent...")
grid = create_grid()
drone_pos = get_empty_cell(grid)
goal_pos = get_empty_cell(grid)

while True:
    img = draw_env(grid, drone_pos, goal_pos)
    cv2.imshow("Drone AI Navigation", img)
    cv2.waitKey(200)

    x, y = drone_pos
    action = np.argmax(q_table[y][x])
    dx, dy = actions[action]
    new_x, new_y = x + dx, y + dy

    # Stop if hit wall or obstacle
    if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
        break
    elif grid[new_y][new_x] == 1:
        break
    elif (new_x, new_y) == goal_pos:
        p
