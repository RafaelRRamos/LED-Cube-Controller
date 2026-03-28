import tkinter as tk
import serial
import time

# ----------------------------
# SERIAL SETUP
# ----------------------------
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    connection_status = "Connected to COM3"
except:
    arduino = None
    connection_status = "No hardware detected (Simulation Mode)"

# ----------------------------
# GLOBAL STATE
# ----------------------------
running = False
current_mode_id = 0
current_mode_name = None
current_command_value = None

# ----------------------------
# MATRIX FUNCTIONS
# ----------------------------
def set_all(color):
    for row in cells:
        for cell in row:
            canvas.itemconfig(cell, fill=color)

def clear_all():
    set_all("black")

# ----------------------------
# ANIMATIONS
# ----------------------------

def blink_loop(mode_id, state=False):
    global running, current_mode_id
    if not running or mode_id != current_mode_id:
        return

    if state:
        set_all("red")
    else:
        clear_all()

    window.after(300, lambda: blink_loop(mode_id, not state))


def chase_loop(mode_id, step=0):
    global running, current_mode_id
    if not running or mode_id != current_mode_id:
        return

    clear_all()

    total_cells = grid_size * grid_size
    index = step % total_cells

    row = index // grid_size
    col = index % grid_size

    # Snake pattern
    if row % 2 == 1:
        col = grid_size - 1 - col

    canvas.itemconfig(cells[row][col], fill="blue")

    window.after(120, lambda: chase_loop(mode_id, step + 1))


def burst_loop(mode_id, radius=0):
    global running, current_mode_id
    if not running or mode_id != current_mode_id:
        return

    clear_all()
    center = grid_size // 2

    for r in range(grid_size):
        for c in range(grid_size):
            if abs(r - center) == radius or abs(c - center) == radius:
                canvas.itemconfig(cells[r][c], fill="yellow")

    max_radius = grid_size // 2
    next_radius = radius + 1 if radius < max_radius else 0

    window.after(200, lambda: burst_loop(mode_id, next_radius))


# ----------------------------
# COMMAND FUNCTION
# ----------------------------
def send_command(mode_name, command_value):
    global running, current_mode_id
    global current_mode_name, current_command_value

    # Store current mode
    current_mode_name = mode_name
    current_command_value = command_value

    # Stop previous mode
    running = False
    current_mode_id += 1
    my_id = current_mode_id

    status_label.config(text=f"Current Mode: {mode_name}")
    command_label.config(text=f"Last Command: {command_value}")

    if arduino:
        arduino.write(command_value.encode())
    else:
        print(f"[SIMULATION] {mode_name}")

    # Start new mode
    if mode_name == "Static":
        set_all("green")

    elif mode_name == "Blink":
        running = True
        blink_loop(my_id)

    elif mode_name == "Chase":
        running = True
        chase_loop(my_id)

    elif mode_name == "Burst":
        running = True
        burst_loop(my_id)

    elif mode_name == "Off":
        clear_all()


# ----------------------------
# RESET FUNCTION (FIXED)
# ----------------------------
def reset_system():
    global running, current_mode_id
    global current_mode_name, current_command_value

    if current_mode_name is None:
        print("Nothing to reset")
        return

    print(f"Resetting: {current_mode_name}")

    running = False
    current_mode_id += 1

    send_command(current_mode_name, current_command_value)


# ----------------------------
# UI SETUP
# ----------------------------
window = tk.Tk()
window.title("LED Cube Controller")
window.geometry("420x580")

title_label = tk.Label(window, text="LED Cube Controller", font=("Arial", 18))
title_label.pack(pady=10)

status_label = tk.Label(window, text="Current Mode: None", font=("Arial", 12))
status_label.pack(pady=5)

command_label = tk.Label(window, text="Last Command: None", font=("Arial", 10))
command_label.pack(pady=5)

connection_label = tk.Label(window, text=connection_status, font=("Arial", 10))
connection_label.pack(pady=5)

# ----------------------------
# MATRIX DISPLAY
# ----------------------------
canvas = tk.Canvas(window, width=200, height=200, bg="black")
canvas.pack(pady=10)

grid_size = 5
cell_size = 40
cells = []

for row in range(grid_size):
    row_cells = []
    for col in range(grid_size):
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        rect = canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
        row_cells.append(rect)
    cells.append(row_cells)

# ----------------------------
# BUTTONS
# ----------------------------
tk.Button(window, text="Static", width=20, command=lambda: send_command("Static", "1")).pack(pady=5)
tk.Button(window, text="Blink", width=20, command=lambda: send_command("Blink", "2")).pack(pady=5)
tk.Button(window, text="Chase", width=20, command=lambda: send_command("Chase", "3")).pack(pady=5)
tk.Button(window, text="Burst", width=20, command=lambda: send_command("Burst", "4")).pack(pady=5)
tk.Button(window, text="Off", width=20, command=lambda: send_command("Off", "0")).pack(pady=5)

tk.Button(window, text="Reset", width=20, bg="red", fg="white", command=reset_system).pack(pady=10)

# ----------------------------
# RUN APP
# ----------------------------
window.mainloop()