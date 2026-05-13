import tkinter as tk
import serial
import time

# ----------------------------
# SERIAL SETUP
# ----------------------------
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    connection_status = "ONLINE"
except:
    arduino = None
    connection_status = "SIMULATION"

# ----------------------------
# GLOBAL STATE
# ----------------------------
running = False
system_power = False

current_mode_id = 0
current_mode_name = None
current_command_value = None

modes_used = {
    "Static": False,
    "Blink": False,
    "Chase": False,
    "Burst": False
}

spin_unlocked = False

# ----------------------------
# MAIN WINDOW
# ----------------------------
window = tk.Tk()
window.title("LED Cube Controller V2.1")
window.geometry("1200x800")
window.configure(bg="#121212")

# ----------------------------
# MATRIX SETTINGS
# ----------------------------
grid_size = 5
cell_size = 60
cells = []

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
# SPIN EFFECT
# ----------------------------
def spin_effect(step=0):

    global running

    if not running:
        return

    clear_all()

    for row in range(grid_size):
        for col in range(grid_size):

            if (row + col + step) % 2 == 0:
                canvas.itemconfig(cells[row][col], fill="#8A2BE2")

    window.after(180, lambda: spin_effect(step + 1))

# ----------------------------
# ANIMATIONS
# ----------------------------
def blink_loop(mode_id, state=False):

    global running, current_mode_id

    if not running or mode_id != current_mode_id:
        return

    if state:
        set_all("#00E5FF")
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

    if row % 2 == 1:
        col = grid_size - 1 - col

    canvas.itemconfig(cells[row][col], fill="#00E5FF")

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
                canvas.itemconfig(cells[r][c], fill="#FFD700")

    max_radius = grid_size // 2
    next_radius = radius + 1 if radius < max_radius else 0

    window.after(200, lambda: burst_loop(mode_id, next_radius))

# ----------------------------
# CLOCK PLACEHOLDER
# ----------------------------
def clock_mode():

    if not system_power:
        return

    clear_all()

    current_time = time.strftime("%H:%M:%S")

    mode_value.config(text=f"CLOCK {current_time}")

    set_all("#00FFB3")

# ----------------------------
# PONG PLACEHOLDER
# ----------------------------
def pong_mode():

    if not system_power:
        return

    clear_all()

    mode_value.config(text="PONG")

    for i in range(grid_size):
        canvas.itemconfig(cells[2][i], fill="#FF00FF")

# ----------------------------
# MUSIC PLACEHOLDER
# ----------------------------
def music_mode():

    if not system_power:
        return

    mode_value.config(text="MUSIC ACTIVE")

    status_value.config(text="AUDIO SYSTEM READY", fg="#CC7000")

# ----------------------------
# SPIN UNLOCK CHECK
# ----------------------------
def check_spin_unlock():

    global spin_unlocked
    global running

    if all(modes_used.values()) and not spin_unlocked:

        spin_unlocked = True

        status_value.config(text="SPIN ACTIVATED", fg="#8A2BE2")

        running = True

        spin_effect()

# ----------------------------
# SYSTEM POWER
# ----------------------------
def system_on():

    global system_power

    system_power = True

    status_value.config(text="SYSTEM ONLINE", fg="#39FF14")

def system_off():

    global system_power
    global running
    global current_mode_id

    system_power = False

    running = False

    current_mode_id += 1

    clear_all()

    status_value.config(text="SYSTEM OFFLINE", fg="#FF3B30")

    mode_value.config(text="NONE")

# ----------------------------
# COMMAND FUNCTION
# ----------------------------
def send_command(mode_name, command_value):

    global running
    global current_mode_id
    global current_mode_name
    global current_command_value

    if not system_power:
        status_value.config(text="SYSTEM OFFLINE", fg="#FF3B30")
        return

    current_mode_name = mode_name
    current_command_value = command_value

    running = False

    current_mode_id += 1

    my_id = current_mode_id

    mode_value.config(text=mode_name.upper())

    if arduino:
        arduino.write(command_value.encode())

    # ----------------------------
    # TRACK MODES
    # ----------------------------
    if mode_name in modes_used:
        modes_used[mode_name] = True
        check_spin_unlock()

    # ----------------------------
    # MODES
    # ----------------------------
    if mode_name == "Static":

        set_all("#39FF14")

    elif mode_name == "Blink":

        running = True
        blink_loop(my_id)

    elif mode_name == "Chase":

        running = True
        chase_loop(my_id)

    elif mode_name == "Burst":

        running = True
        burst_loop(my_id)

# ----------------------------
# RESET
# ----------------------------
def reset_system():

    global running
    global current_mode_id
    global spin_unlocked

    running = False

    current_mode_id += 1

    clear_all()

    spin_unlocked = False

    for key in modes_used:
        modes_used[key] = False

    mode_value.config(text="NONE")

    if system_power:
        status_value.config(text="SYSTEM ONLINE", fg="#39FF14")
    else:
        status_value.config(text="SYSTEM OFFLINE", fg="#FF3B30")

# ----------------------------
# SCREEN SWITCHING
# ----------------------------
def enter_system():

    welcome_frame.pack_forget()

    dashboard_frame.pack(fill="both", expand=True)

# ----------------------------
# WELCOME SCREEN
# ----------------------------
welcome_frame = tk.Frame(window, bg="#1E1E1E")

welcome_frame.pack(fill="both", expand=True)

title_label = tk.Label(
    welcome_frame,
    text="LED CUBE CONTROLLER",
    bg="#1E1E1E",
    fg="white",
    font=("Arial", 28, "bold")
)

title_label.pack(pady=30)

subtitle_label = tk.Label(
    welcome_frame,
    text="Interactive Visualization and Control System",
    bg="#1E1E1E",
    fg="#B0B0B0",
    font=("Arial", 14)
)

subtitle_label.pack(pady=10)

# ----------------------------
# WELCOME CUBE PLACEHOLDER
# ----------------------------
welcome_canvas = tk.Canvas(
    welcome_frame,
    width=240,
    height=240,
    bg="#1E1E1E",
    highlightthickness=0
)

welcome_canvas.pack(pady=20)

for row in range(5):
    for col in range(5):

        x = 40 + (col * 35)
        y = 40 + (row * 35)

        welcome_canvas.create_oval(
            x,
            y,
            x + 20,
            y + 20,
            fill="#00E5FF",
            outline=""
        )

username_entry = tk.Entry(
    welcome_frame,
    width=25,
    font=("Arial", 16),
    bg="#252526",
    fg="white",
    insertbackground="white"
)

username_entry.pack(pady=20)

enter_button = tk.Button(
    welcome_frame,
    text="ENTER SYSTEM",
    width=20,
    height=2,
    bg="#00E5FF",
    fg="black",
    font=("Arial", 14, "bold"),
    command=enter_system
)

enter_button.pack(pady=20)

footer_label = tk.Label(
    welcome_frame,
    text="SYSTEM READY V2.1.0",
    bg="#1E1E1E",
    fg="#B0B0B0",
    font=("Arial", 10)
)

footer_label.pack(side="bottom", pady=20)

# ----------------------------
# DASHBOARD
# ----------------------------
dashboard_frame = tk.Frame(window, bg="#121212")

header_label = tk.Label(
    dashboard_frame,
    text="LED CUBE CONTROL SYSTEM",
    bg="#121212",
    fg="white",
    font=("Arial", 22, "bold")
)

header_label.pack(pady=20)

main_frame = tk.Frame(dashboard_frame, bg="#121212")

main_frame.pack(fill="both", expand=True)

# ----------------------------
# VISUALIZATION PANEL
# ----------------------------
visual_frame = tk.Frame(
    main_frame,
    bg="#1B263B",
    highlightbackground="#00E5FF",
    highlightthickness=2
)

visual_frame.pack(side="left", padx=20, pady=20)

canvas = tk.Canvas(
    visual_frame,
    width=500,
    height=500,
    bg="black",
    highlightthickness=0
)

canvas.pack(padx=20, pady=20)

# ----------------------------
# MATRIX CREATION
# ----------------------------
for row in range(grid_size):

    row_cells = []

    for col in range(grid_size):

        x1 = col * cell_size + 20
        y1 = row * cell_size + 20

        x2 = x1 + cell_size
        y2 = y1 + cell_size

        rect = canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="black",
            outline="gray"
        )

        row_cells.append(rect)

    cells.append(row_cells)

# ----------------------------
# CONTROL PANEL
# ----------------------------
control_frame = tk.Frame(
    main_frame,
    bg="#252526",
    highlightbackground="#D4AF37",
    highlightthickness=2
)

control_frame.pack(side="right", padx=20, pady=20, fill="y")

# ----------------------------
# STATUS
# ----------------------------
status_title = tk.Label(
    control_frame,
    text="SYSTEM STATUS",
    bg="#252526",
    fg="#D4AF37",
    font=("Arial", 14, "bold")
)

status_title.pack(pady=(20, 5))

status_value = tk.Label(
    control_frame,
    text="SYSTEM OFFLINE",
    bg="#252526",
    fg="#FF3B30",
    font=("Arial", 12)
)

status_value.pack(pady=(0, 20))

# ----------------------------
# MODE DISPLAY
# ----------------------------
mode_title = tk.Label(
    control_frame,
    text="CURRENT MODE",
    bg="#252526",
    fg="#00E5FF",
    font=("Arial", 14, "bold")
)

mode_title.pack(pady=(0, 5))

mode_value = tk.Label(
    control_frame,
    text="NONE",
    bg="#252526",
    fg="white",
    font=("Arial", 12)
)

mode_value.pack(pady=(0, 20))

# ----------------------------
# SYSTEM LABEL
# ----------------------------
system_label = tk.Label(
    control_frame,
    text="SYSTEM",
    bg="#252526",
    fg="#FFD700",
    font=("Arial", 14, "bold")
)

system_label.pack(pady=(10, 10))

# ----------------------------
# SYSTEM BUTTONS
# ----------------------------
tk.Button(
    control_frame,
    text="SYSTEM ON",
    width=20,
    bg="#39FF14",
    fg="black",
    command=system_on
).pack(pady=5)

tk.Button(
    control_frame,
    text="SYSTEM OFF",
    width=20,
    bg="#FF3B30",
    fg="white",
    command=system_off
).pack(pady=5)

tk.Button(
    control_frame,
    text="RESET",
    width=20,
    bg="#FFD700",
    fg="black",
    command=reset_system
).pack(pady=5)

# ----------------------------
# CORE MODES LABEL
# ----------------------------
mode_label = tk.Label(
    control_frame,
    text="CORE MODES",
    bg="#252526",
    fg="#00E5FF",
    font=("Arial", 14, "bold")
)

mode_label.pack(pady=(30, 10))

# ----------------------------
# CORE MODE BUTTONS
# ----------------------------
tk.Button(
    control_frame,
    text="STATIC",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Static", "1")
).pack(pady=5)

tk.Button(
    control_frame,
    text="BLINK",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Blink", "2")
).pack(pady=5)

tk.Button(
    control_frame,
    text="CHASE",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Chase", "3")
).pack(pady=5)

tk.Button(
    control_frame,
    text="BURST",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Burst", "4")
).pack(pady=5)

# ----------------------------
# SPECIAL FEATURES LABEL
# ----------------------------
special_label = tk.Label(
    control_frame,
    text="SPECIAL FEATURES",
    bg="#252526",
    fg="#FF00FF",
    font=("Arial", 14, "bold")
)

special_label.pack(pady=(30, 10))

# ----------------------------
# SPECIAL FEATURE BUTTONS
# ----------------------------
tk.Button(
    control_frame,
    text="CLOCK",
    width=20,
    bg="#00FFB3",
    fg="black",
    command=clock_mode
).pack(pady=5)

tk.Button(
    control_frame,
    text="PONG",
    width=20,
    bg="#FF00FF",
    fg="white",
    command=pong_mode
).pack(pady=5)

tk.Button(
    control_frame,
    text="MUSIC",
    width=20,
    bg="#CC7000",
    fg="white",
    command=music_mode
).pack(pady=5)

# ----------------------------
# RUN APP
# ----------------------------
window.mainloop()