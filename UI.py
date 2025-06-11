import tkinter as tk

# Show a transparent and movable capture box on the screen
def show_capture_window(region):
    root = tk.Tk()
    root.attributes('-topmost', True)     # Keep the window on top
    root.attributes('-alpha', 0.3)        # Set transparency
    root.overrideredirect(True)           # Remove window borders and title
    root.geometry(f"{region[2]}x{region[3]}+{region[0]}+{region[1]}")  # Set size and position

    # Create a canvas with a red border rectangle
    canvas = tk.Canvas(root, width=region[2], height=region[3], bg='white', highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, region[2], region[3], outline='red', width=3)

    # Event handler: when mouse is clicked, remember initial position
    def start_move(event):
        root.start_x = event.x
        root.start_y = event.y

    # Event handler: move the window according to mouse drag
    def do_move(event):
        dx = event.x - root.start_x
        dy = event.y - root.start_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"{region[2]}x{region[3]}+{x}+{y}")
        region[0] = x
        region[1] = y  # Update the region with new position

    # Bind mouse events to canvas
    canvas.bind("<Button-1>", start_move)
    canvas.bind("<B1-Motion>", do_move)

    # Start the Tkinter main loop
    root.mainloop()