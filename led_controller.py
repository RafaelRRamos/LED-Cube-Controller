import tkinter as tk
import serial
import time
import math

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
clock_running = False
boot_active = False
music_enabled = False

current_mode_id = 0

username = "USER"

modes_used = {
    "Static": False,
    "Blink": False,
    "Chase": False,
    "Burst": False
}

spin_unlocked = False

rotation_angle = 0
flash_state = True

# ----------------------------
# MAIN WINDOW
# ----------------------------
window = tk.Tk()
window.title("LED Cube Controller V2.9")
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
# MUSIC TOGGLE
# ----------------------------
def toggle_music():

    global music_enabled

    music_enabled = not music_enabled

    if music_enabled:

        music_status_label.config(
            text="MUSIC STATUS: ON",
            fg="#39FF14"
        )

        music_toggle_button.config(
            text="MUSIC: ON",
            bg="#39FF14",
            fg="black"
        )

    else:

        music_status_label.config(
            text="MUSIC STATUS: OFF",
            fg="#FF3B30"
        )

        music_toggle_button.config(
            text="MUSIC: OFF",
            bg="#FF3B30",
            fg="white"
        )

# ----------------------------
# FLASHING PROMPT
# ----------------------------
def flash_prompt():

    global flash_state

    if flash_state:
        prompt_label.config(fg="#00E5FF")
    else:
        prompt_label.config(fg="#252526")

    flash_state = not flash_state

    window.after(500, flash_prompt)

# ----------------------------
# WELCOME CUBE
# ----------------------------
def animate_welcome_cube():

    global rotation_angle

    welcome_canvas.delete("cube")

    center_x = 160
    center_y = 140

    size = 70

    angle = rotation_angle

    front = []
    back = []

    for x, y in [
        (-1, -1),
        (1, -1),
        (1, 1),
        (-1, 1)
    ]:

        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)

        front.append((
            center_x + rx * size,
            center_y + ry * size
        ))

    for x, y in [
        (-1, -1),
        (1, -1),
        (1, 1),
        (-1, 1)
    ]:

        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)

        back.append((
            center_x + rx * size * 0.7 + 40,
            center_y + ry * size * 0.7 - 40
        ))

    for i in range(4):

        x1, y1 = back[i]
        x2, y2 = back[(i + 1) % 4]

        welcome_canvas.create_line(
            x1, y1, x2, y2,
            fill="#8A2BE2",
            width=3,
            tags="cube"
        )

    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = front[(i + 1) % 4]

        welcome_canvas.create_line(
            x1, y1, x2, y2,
            fill="#00E5FF",
            width=3,
            tags="cube"
        )

    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = back[i]

        welcome_canvas.create_line(
            x1, y1, x2, y2,
            fill="#39FF14",
            width=2,
            tags="cube"
        )

    rotation_angle += 0.02

    window.after(40, animate_welcome_cube)

# ----------------------------
# CLOCK DISPLAY
# ----------------------------
def update_clock():

    global clock_running

    if not clock_running or not system_power:
        return

    current_time = time.strftime("%H:%M:%S")

    mode_value.config(text=f"CLOCK {current_time}")

    clear_all()

    colors = [
        "#00FFB3",
        "#00E5FF",
        "#39FF14",
        "#FFD700",
        "#8A2BE2"
    ]

    for row in range(grid_size):
        for col in range(grid_size):

            color_index = (row + col) % len(colors)

            canvas.itemconfig(
                cells[row][col],
                fill=colors[color_index]
            )

    window.after(1000, update_clock)

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
# CORE ANIMATIONS
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
# SPECIAL FEATURES
# ----------------------------
def pong_mode():

    global running
    global clock_running

    if not system_power:
        return

    running = False
    clock_running = False

    clear_all()

    mode_value.config(text="PONG")

    for i in range(grid_size):
        canvas.itemconfig(cells[2][i], fill="#FF00FF")

def music_mode():

    global running
    global clock_running

    if not system_power:
        return

    running = False
    clock_running = False

    clear_all()

    mode_value.config(text="MUSIC ACTIVE")

    status_value.config(text="AUDIO SYSTEM READY", fg="#CC7000")

    for row in range(grid_size):
        for col in range(grid_size):

            if (row + col) % 2 == 0:
                canvas.itemconfig(cells[row][col], fill="#CC7000")

def clock_mode():

    global running
    global clock_running

    if not system_power:
        return

    running = False
    clock_running = True

    status_value.config(text="CLOCK MODE ACTIVE", fg="#00FFB3")

    update_clock()

# ----------------------------
# SPIN UNLOCK
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
    global clock_running
    global current_mode_id

    system_power = False

    running = False
    clock_running = False

    current_mode_id += 1

    clear_all()

    status_value.config(text="SYSTEM OFFLINE", fg="#FF3B30")

    mode_value.config(text="NONE")

# ----------------------------
# COMMAND FUNCTION
# ----------------------------
def send_command(mode_name, command_value):

    global running
    global clock_running
    global current_mode_id

    if not system_power:

        status_value.config(text="SYSTEM OFFLINE", fg="#FF3B30")

        return

    clock_running = False

    running = False

    current_mode_id += 1

    my_id = current_mode_id

    mode_value.config(text=mode_name.upper())

    if arduino:
        arduino.write(command_value.encode())

    if mode_name in modes_used:
        modes_used[mode_name] = True
        check_spin_unlock()

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
# RESET SYSTEM
# ----------------------------
def reset_system():

    global running
    global clock_running
    global current_mode_id
    global spin_unlocked

    running = False
    clock_running = False

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
# RETURN TO WELCOME
# ----------------------------
def return_to_welcome():

    global username
    global boot_active

    username = "USER"

    boot_active = False

    dashboard_frame.pack_forget()

    welcome_title.config(
        text="LED CUBE CONTROLLER",
        fg="#00E5FF",
        font=("Arial", 24, "bold")
    )

    username_entry.delete(0, tk.END)

    countdown_label.config(text="")

    prompt_label.pack(pady=10)

    username_entry.pack(pady=20)

    enter_button.pack(pady=10)

    welcome_frame.pack(fill="both", expand=True)

# ----------------------------
# FLASH ENTRY EFFECT
# ----------------------------
def flash_enter_effect(count=0):

    colors = [
        "#00E5FF",
        "#8A2BE2",
        "#39FF14",
        "#FFD700"
    ]

    color = colors[count % len(colors)]

    welcome_canvas.configure(bg=color)

    if count < 8:

        window.after(
            120,
            lambda: flash_enter_effect(count + 1)
        )

    else:

        welcome_canvas.configure(bg="#1E1E1E")

        enter_system()

# ----------------------------
# START BOOT
# ----------------------------
def start_boot_sequence():

    global username
    global boot_active

    boot_active = True

    entered_name = username_entry.get().strip()

    if entered_name != "":
        username = entered_name.upper()

    welcome_title.config(
        text=f"WELCOME TO THE CUBE\n\nA RETRO VISUALIZATION EXPERIENCE\n\nUSER: {username}",
        fg="#00E5FF",
        font=("Arial", 20, "bold")
    )

    username_entry.pack_forget()

    enter_button.pack_forget()

    prompt_label.pack_forget()

    countdown_sequence(3)

# ----------------------------
# COUNTDOWN
# ----------------------------
def countdown_sequence(value):

    global boot_active

    if not boot_active:
        return

    if value > 0:

        countdown_label.config(text=str(value))

        window.after(
            1000,
            lambda: countdown_sequence(value - 1)
        )

    else:

        countdown_label.config(text="ENTERING SYSTEM")

        window.after(1000, flash_enter_effect)

# ----------------------------
# ENTER SYSTEM
# ----------------------------
def enter_system():

    welcome_frame.pack_forget()

    dashboard_frame.pack(fill="both", expand=True)

# ----------------------------
# WELCOME SCREEN
# ----------------------------
welcome_frame = tk.Frame(window, bg="#1E1E1E")

welcome_frame.pack(fill="both", expand=True)

welcome_title = tk.Label(
    welcome_frame,
    text="LED CUBE CONTROLLER",
    bg="#1E1E1E",
    fg="#00E5FF",
    font=("Arial", 24, "bold"),
    justify="center"
)

welcome_title.pack(pady=20)

welcome_canvas = tk.Canvas(
    welcome_frame,
    width=320,
    height=280,
    bg="#1E1E1E",
    highlightthickness=0
)

welcome_canvas.pack(pady=10)

prompt_label = tk.Label(
    welcome_frame,
    text="ENTER USER NAME",
    bg="#1E1E1E",
    fg="#00E5FF",
    font=("Arial", 14, "bold")
)

prompt_label.pack(pady=10)

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
    command=start_boot_sequence
)

enter_button.pack(pady=10)

countdown_label = tk.Label(
    welcome_frame,
    text="",
    bg="#1E1E1E",
    fg="#00E5FF",
    font=("Arial", 28, "bold")
)

countdown_label.pack(pady=20)

footer_label = tk.Label(
    welcome_frame,
    text="SYSTEM READY V2.9.0",
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
# LEFT CONTROL AREA
# ----------------------------
left_control_frame = tk.Frame(
    visual_frame,
    bg="#1B263B"
)

left_control_frame.pack(pady=10)

music_status_label = tk.Label(
    left_control_frame,
    text="MUSIC STATUS: OFF",
    bg="#1B263B",
    fg="#FF3B30",
    font=("Arial", 12, "bold")
)

music_status_label.pack(pady=5)

music_toggle_button = tk.Button(
    left_control_frame,
    text="MUSIC: OFF",
    width=20,
    bg="#FF3B30",
    fg="white",
    font=("Arial", 12, "bold"),
    command=toggle_music
)

music_toggle_button.pack(pady=5)

back_to_welcome_button = tk.Button(
    left_control_frame,
    text="BACK TO WELCOME",
    width=20,
    bg="#00E5FF",
    fg="black",
    font=("Arial", 12, "bold"),
    command=return_to_welcome
)

back_to_welcome_button.pack(pady=5)

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
# CORE MODES
# ----------------------------
mode_label = tk.Label(
    control_frame,
    text="CORE MODES",
    bg="#252526",
    fg="#00E5FF",
    font=("Arial", 14, "bold")
)

mode_label.pack(pady=(30, 10))

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
# SPECIAL FEATURES
# ----------------------------
special_label = tk.Label(
    control_frame,
    text="SPECIAL FEATURES",
    bg="#252526",
    fg="#FF00FF",
    font=("Arial", 14, "bold")
)

special_label.pack(pady=(30, 10))

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
# START ANIMATIONS
# ----------------------------
animate_welcome_cube()
flash_prompt()

# ----------------------------
# RUN APP
# ----------------------------
window.mainloop()