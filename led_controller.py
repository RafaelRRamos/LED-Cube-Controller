import tkinter as tk
import time
import math

# ----------------------------
# GLOBAL STATE
# ----------------------------
running = False
system_power = False
clock_running = False
boot_active = False

current_mode_id = 0

username = "USER"

modes_used = {
    "Static": False,
    "Blink": False,
    "Chase": False,
    "Burst": False
}

spin_unlocked = False
spin_active = False

rotation_angle = 0
flash_state = True
mystery_flash_state = True

# ----------------------------
# MAIN WINDOW
# ----------------------------
window = tk.Tk()

window.title("LED Cube Controller V3.5")

window.geometry("1400x850")

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

    canvas.delete("spin_cube")

    for row in cells:
        for cell in row:

            canvas.itemconfig(
                cell,
                fill=color,
                state="normal"
            )

def clear_all():

    canvas.delete("spin_cube")

    for row in cells:
        for cell in row:

            canvas.itemconfig(
                cell,
                fill="black",
                state="normal"
            )

# ----------------------------
# HIDE GRID DURING SPIN
# ----------------------------
def hide_grid():

    for row in cells:
        for cell in row:

            canvas.itemconfig(
                cell,
                state="hidden"
            )

# ----------------------------
# SHOW GRID AFTER SPIN
# ----------------------------
def show_grid():

    for row in cells:
        for cell in row:

            canvas.itemconfig(
                cell,
                state="normal"
            )

# ----------------------------
# FLASHING PROMPT
# ----------------------------
def flash_prompt():

    global flash_state

    if flash_state:

        prompt_label.config(
            fg="#00E5FF"
        )

    else:

        prompt_label.config(
            fg="#252526"
        )

    flash_state = not flash_state

    window.after(
        500,
        flash_prompt
    )

# ----------------------------
# FLASH MYSTERY BUTTON
# ----------------------------
def flash_mystery_button():

    global mystery_flash_state

    if not spin_unlocked:
        return

    if mystery_flash_state:

        mystery_button.config(
            bg="#8A2BE2",
            fg="white"
        )

    else:

        mystery_button.config(
            bg="#121212",
            fg="#8A2BE2"
        )

    mystery_flash_state = not mystery_flash_state

    window.after(
        500,
        flash_mystery_button
    )

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
            x1,
            y1,
            x2,
            y2,
            fill="#8A2BE2",
            width=3,
            tags="cube"
        )

    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = front[(i + 1) % 4]

        welcome_canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#00E5FF",
            width=3,
            tags="cube"
        )

    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = back[i]

        welcome_canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#39FF14",
            width=2,
            tags="cube"
        )

    rotation_angle += 0.02

    window.after(
        40,
        animate_welcome_cube
    )

# ----------------------------
# CLOCK DISPLAY
# ----------------------------
def update_clock():

    global clock_running

    if not clock_running or not system_power:
        return

    current_time = time.strftime("%I:%M:%S %p")

    current_date = time.strftime("%A %B %d %Y").upper()

    clock_name_label.config(
        text=f"{username} IT IS"
    )

    clock_time_label.config(
        text=current_time
    )

    clock_date_label.config(
        text=current_date
    )

    window.after(
        1000,
        update_clock
    )

# ----------------------------
# SPIN EFFECT
# ----------------------------
def spin_effect():

    global spin_active
    global rotation_angle

    if not spin_active:
        return

    canvas.delete("spin_cube")

    center_x = 250
    center_y = 250

    size = 120

    angle = rotation_angle

    depth_offset = 42

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
            center_x + rx * size * 0.7 + depth_offset,
            center_y + ry * size * 0.7 - depth_offset
        ))

    # BACK FACE
    for i in range(4):

        x1, y1 = back[i]
        x2, y2 = back[(i + 1) % 4]

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#8A2BE2",
            width=5,
            tags="spin_cube"
        )

    # FRONT FACE
    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = front[(i + 1) % 4]

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#00E5FF",
            width=5,
            tags="spin_cube"
        )

    # CONNECTORS
    for i in range(4):

        x1, y1 = front[i]
        x2, y2 = back[i]

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#39FF14",
            width=4,
            tags="spin_cube"
        )

    rotation_angle += 0.03

    window.after(
        40,
        spin_effect
    )

# ----------------------------
# END SPIN
# ----------------------------
def end_spin_reward():

    global spin_active
    global spin_unlocked

    spin_active = False
    spin_unlocked = False

    mystery_button.place_forget()

    canvas.delete("spin_cube")

    show_grid()

    clear_all()

    for key in modes_used:
        modes_used[key] = False

    status_value.config(
        text="SYSTEM ONLINE",
        fg="#39FF14"
    )

    mode_value.config(
        text="NONE"
    )

# ----------------------------
# START SPIN
# ----------------------------
def start_spin_reward():

    global spin_active
    global running
    global clock_running

    running = False
    clock_running = False

    mystery_button.place_forget()

    hide_grid()

    spin_active = True

    status_value.config(
        text="SPECIAL FEATURE ACTIVE",
        fg="#8A2BE2"
    )

    mode_value.config(
        text="MYSTERY"
    )

    spin_effect()

    window.after(
        10000,
        end_spin_reward
    )

# ----------------------------
# SPIN UNLOCK
# ----------------------------
def check_spin_unlock():

    global spin_unlocked

    if all(modes_used.values()) and not spin_unlocked:

        spin_unlocked = True

        status_value.config(
            text="SPECIAL FEATURE UNLOCKED",
            fg="#8A2BE2"
        )

        mystery_button.place(
            relx=0.5,
            rely=0.78,
            anchor="center"
        )

        flash_mystery_button()

# ----------------------------
# CORE ANIMATIONS
# ----------------------------
def blink_loop(mode_id, state=False):

    global running
    global current_mode_id

    if not running or mode_id != current_mode_id:
        return

    if state:
        set_all("#00E5FF")
    else:
        clear_all()

    window.after(
        300,
        lambda: blink_loop(mode_id, not state)
    )

def chase_loop(mode_id, step=0):

    global running
    global current_mode_id

    if not running or mode_id != current_mode_id:
        return

    clear_all()

    total_cells = grid_size * grid_size

    index = step % total_cells

    row = index // grid_size
    col = index % grid_size

    if row % 2 == 1:
        col = grid_size - 1 - col

    canvas.itemconfig(
        cells[row][col],
        fill="#00E5FF"
    )

    window.after(
        120,
        lambda: chase_loop(mode_id, step + 1)
    )

def burst_loop(mode_id, radius=0):

    global running
    global current_mode_id

    if not running or mode_id != current_mode_id:
        return

    clear_all()

    center = grid_size // 2

    for r in range(grid_size):
        for c in range(grid_size):

            if abs(r - center) == radius or abs(c - center) == radius:

                canvas.itemconfig(
                    cells[r][c],
                    fill="#FFD700"
                )

    max_radius = grid_size // 2

    next_radius = radius + 1 if radius < max_radius else 0

    window.after(
        200,
        lambda: burst_loop(mode_id, next_radius)
    )

# ----------------------------
# CLOCK MODE
# ----------------------------
def clock_mode():

    global running
    global clock_running

    if not system_power:
        return

    if clock_running:

        clock_running = False

        clear_all()

        clock_name_label.config(text="")
        clock_time_label.config(text="")
        clock_date_label.config(text="")

        status_value.config(
            text="CLOCK MODE OFF",
            fg="#FF3B30"
        )

        mode_value.config(
            text="NONE"
        )

        return

    running = False

    clock_running = True

    status_value.config(
        text="CLOCK MODE ACTIVE",
        fg="#00FFB3"
    )

    mode_value.config(
        text="CLOCK"
    )

    update_clock()

# ----------------------------
# SYSTEM POWER
# ----------------------------
def system_on():

    global system_power

    system_power = True

    status_value.config(
        text="SYSTEM ONLINE",
        fg="#39FF14"
    )

def system_off():

    global system_power
    global running
    global clock_running
    global current_mode_id
    global spin_active
    global spin_unlocked

    system_power = False

    running = False
    clock_running = False
    spin_active = False
    spin_unlocked = False

    current_mode_id += 1

    mystery_button.place_forget()

    canvas.delete("spin_cube")

    show_grid()

    clear_all()

    clock_name_label.config(text="")
    clock_time_label.config(text="")
    clock_date_label.config(text="")

    status_value.config(
        text="SYSTEM OFFLINE",
        fg="#FF3B30"
    )

    mode_value.config(
        text="NONE"
    )

# ----------------------------
# COMMAND FUNCTION
# ----------------------------
def send_command(mode_name):

    global running
    global clock_running
    global current_mode_id

    if not system_power:

        status_value.config(
            text="SYSTEM OFFLINE",
            fg="#FF3B30"
        )

        return

    show_grid()

    canvas.delete("spin_cube")

    clock_running = False

    running = False

    current_mode_id += 1

    my_id = current_mode_id

    mode_value.config(
        text=mode_name.upper()
    )

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
    global spin_active

    running = False
    clock_running = False
    spin_active = False
    spin_unlocked = False

    current_mode_id += 1

    mystery_button.place_forget()

    canvas.delete("spin_cube")

    show_grid()

    clear_all()

    for key in modes_used:
        modes_used[key] = False

    clock_name_label.config(text="")
    clock_time_label.config(text="")
    clock_date_label.config(text="")

    mode_value.config(
        text="NONE"
    )

    if system_power:

        status_value.config(
            text="SYSTEM ONLINE",
            fg="#39FF14"
        )

    else:

        status_value.config(
            text="SYSTEM OFFLINE",
            fg="#FF3B30"
        )

# ----------------------------
# RETURN TO WELCOME
# ----------------------------
def return_to_welcome():

    global username
    global boot_active
    global running
    global system_power
    global clock_running
    global spin_active
    global spin_unlocked

    username = "USER"

    boot_active = False

    running = False
    system_power = False
    clock_running = False
    spin_active = False
    spin_unlocked = False

    mystery_button.place_forget()

    canvas.delete("spin_cube")

    show_grid()

    clear_all()

    dashboard_frame.pack_forget()

    welcome_title.config(
        text="LED CUBE CONTROLLER",
        fg="#00E5FF",
        font=("Arial", 24, "bold")
    )

    username_entry.delete(0, tk.END)

    countdown_label.config(text="")

    clock_name_label.config(text="")
    clock_time_label.config(text="")
    clock_date_label.config(text="")

    status_value.config(
        text="SYSTEM OFFLINE",
        fg="#FF3B30"
    )

    mode_value.config(
        text="NONE"
    )

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
# EXTENDED COUNTDOWN
# ----------------------------
boot_messages = [
    "INITIALIZING",
    "LOADING VISUAL SYSTEM",
    "PREPARING INTERFACE",
    "ENTERING SYSTEM"
]

def countdown_sequence(index):

    global boot_active

    if not boot_active:
        return

    if index < len(boot_messages):

        countdown_label.config(
            text=boot_messages[index]
        )

        window.after(
            1200,
            lambda: countdown_sequence(index + 1)
        )

    else:

        flash_enter_effect()

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

    countdown_sequence(0)

# ----------------------------
# ENTER SYSTEM
# ----------------------------
def enter_system():

    welcome_frame.pack_forget()

    dashboard_frame.pack(fill="both", expand=True)

# ----------------------------
# WELCOME SCREEN
# ----------------------------
welcome_frame = tk.Frame(
    window,
    bg="#1E1E1E"
)

welcome_frame.pack(
    fill="both",
    expand=True
)

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
    font=("Arial", 24, "bold")
)

countdown_label.pack(pady=20)

footer_label = tk.Label(
    welcome_frame,
    text="SYSTEM READY V3.5",
    bg="#1E1E1E",
    fg="#B0B0B0",
    font=("Arial", 10)
)

footer_label.pack(
    side="bottom",
    pady=20
)

# ----------------------------
# DASHBOARD
# ----------------------------
dashboard_frame = tk.Frame(
    window,
    bg="#121212"
)

header_label = tk.Label(
    dashboard_frame,
    text="LED CUBE CONTROL SYSTEM",
    bg="#121212",
    fg="white",
    font=("Arial", 22, "bold")
)

header_label.pack(pady=20)

main_frame = tk.Frame(
    dashboard_frame,
    bg="#121212"
)

main_frame.pack(
    fill="both",
    expand=True
)

# ----------------------------
# VISUALIZATION PANEL
# ----------------------------
visual_frame = tk.Frame(
    main_frame,
    bg="#1B263B",
    highlightbackground="#00E5FF",
    highlightthickness=2
)

visual_frame.pack(
    side="left",
    padx=20,
    pady=20
)

canvas = tk.Canvas(
    visual_frame,
    width=500,
    height=500,
    bg="black",
    highlightthickness=0
)

canvas.pack(
    padx=20,
    pady=20
)

# ----------------------------
# BACK BUTTON
# ----------------------------
tk.Button(
    visual_frame,
    text="BACK TO WELCOME",
    width=22,
    bg="#00E5FF",
    fg="black",
    font=("Arial", 12, "bold"),
    command=return_to_welcome
).pack(
    pady=(10, 20)
)

# ----------------------------
# CENTER CLOCK DISPLAY
# ----------------------------
center_display_frame = tk.Frame(
    main_frame,
    bg="#121212",
    width=320
)

center_display_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=20
)

center_display_frame.pack_propagate(False)

clock_content_frame = tk.Frame(
    center_display_frame,
    bg="#121212"
)

clock_content_frame.place(
    relx=0.5,
    rely=0.32,
    anchor="center"
)

clock_name_label = tk.Label(
    clock_content_frame,
    text="",
    bg="#121212",
    fg="#00E5FF",
    font=("Arial", 20, "bold")
)

clock_name_label.pack(
    pady=(0, 20)
)

clock_time_label = tk.Label(
    clock_content_frame,
    text="",
    bg="#121212",
    fg="white",
    font=("Arial", 32, "bold")
)

clock_time_label.pack(
    pady=10
)

clock_date_label = tk.Label(
    clock_content_frame,
    text="",
    bg="#121212",
    fg="#B0B0B0",
    font=("Arial", 14)
)

clock_date_label.pack(
    pady=10
)

# ----------------------------
# MYSTERY BUTTON
# ----------------------------
mystery_button = tk.Button(
    center_display_frame,
    text="???",
    width=18,
    height=2,
    bg="#8A2BE2",
    fg="white",
    font=("Arial", 14, "bold"),
    command=start_spin_reward
)

# ----------------------------
# CONTROL PANEL
# ----------------------------
control_frame = tk.Frame(
    main_frame,
    bg="#252526",
    highlightbackground="#D4AF37",
    highlightthickness=2
)

control_frame.pack(
    side="right",
    padx=20,
    pady=20,
    fill="y"
)

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
    command=lambda: send_command("Static")
).pack(pady=5)

tk.Button(
    control_frame,
    text="BLINK",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Blink")
).pack(pady=5)

tk.Button(
    control_frame,
    text="CHASE",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Chase")
).pack(pady=5)

tk.Button(
    control_frame,
    text="BURST",
    width=20,
    bg="#252526",
    fg="white",
    command=lambda: send_command("Burst")
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
# RUN APPLICATION
# ----------------------------
window.mainloop()