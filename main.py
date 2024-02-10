import pyautogui
from PIL import Image, ImageTk
import tkinter as tk
from pynput import keyboard

leftButtonPressed = False
coord = []

# Function to close the window
def close():
    global root
    try:
        root.destroy()
    except:
        print("Window already closed")
        pass

# Function to handle mouse motion
def on_mouse_move(event):
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor="nw")
    # Draw a vertical line
    canvas.create_line(event.x, 0, event.x, event.widget.winfo_height(), fill="red")
    # Draw a horizontal line
    canvas.create_line(0, event.y, event.widget.winfo_width(), event.y, fill="red")
    if leftButtonPressed:
        canvas.create_rectangle(coord[0], coord[1], event.x, event.y, outline="green", width=2)

        # Draw under the rectangle the size of the rectangle in pixels, the rectangle has a black background and the text is white
        text = f"{event.x - coord[0]} x {event.y - coord[1]}"
        canvas.create_rectangle(coord[0] - 30, coord[1] - 30, coord[0] - 30 + len(text) * 8, coord[1] - 30 + 20, fill="black", outline="black")
        canvas.create_text(coord[0] - 30, coord[1] - 30, text=text, fill="white", font="Arial 10", anchor="nw")
 

def on_mouse_click(event):
    global leftButtonPressed
    leftButtonPressed = True
    global coord
    coord = [event.x, event.y]

def on_mouse_release(event):
    global leftButtonPressed
    leftButtonPressed = False

# Function to capture screenshot
def capture_screenshot():
    # Capture screenshot
    screenshot = pyautogui.screenshot()

    # Save the image
    screenshot.save("screenshot.png")

    # Open the image file
    img = Image.open("screenshot.png")

    # Create a tkinter window
    global root
    root = tk.Tk()

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Set the frameless window but showed in the taskbar
    root.overrideredirect(True)

    # Create a PhotoImage object from the Image object
    global photo
    photo = ImageTk.PhotoImage(img)

    global canvas
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack()

    # Display the image on the canvas
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Bind the mouse motion event to the on_mouse_move function
    canvas.bind('<Motion>', on_mouse_move)

    # Bind the middle mouse button click event to the close function
    canvas.bind('<Button-3>', lambda event: close())

    # Bind the left mouse button click down event to the on_mouse_click function
    canvas.bind('<ButtonPress-1>', on_mouse_click)

    # Bind the left mouse release event to the close function
    canvas.bind('<ButtonRelease-1>', on_mouse_release)

    # Run the tkinter main loop
    root.mainloop()

# Define the key combination for screenshot
COMBINATION = {keyboard.Key.shift, keyboard.Key.cmd, keyboard.KeyCode.from_char('M')}

# The currently active modifiers
current_keys = set()

def on_press(key):
    if key in COMBINATION:
        current_keys.add(key)
        if COMBINATION.issubset(current_keys):
            capture_screenshot()

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

# Start listening for keypresses
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()