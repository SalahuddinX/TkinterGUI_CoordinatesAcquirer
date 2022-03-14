import tkinter as tk
from tkinter import CENTER
from PIL import Image, ImageTk, ImageDraw
import cv2


class CoordinatesTransferGUI:
    def __init__(self, window, cap):
        self.image = None
        self.window = window
        self.main_frame = tk.Frame(self.window, width=650, height=450, pady=3, padx=2)
        self.main_frame.pack()
        self.cap = cap
        self.width = 600  # self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = 380  # self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20  # Interval in ms to get the latest frame

        # Main Frame Configuration
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Top Frame Creation & Configurations
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, sticky="nswe")

        # Create canvas for image
        self.canvas_title = tk.Label(self.top_frame, text='Live Stream', font='Helvetica 18 bold')
        self.canvas_title.grid(row=0, columnspan=2)
        self.canvas = tk.Canvas(self.top_frame, width=self.width, height=self.height)
        self.canvas.grid(row=1, columnspan=2)

        # Bottom Frame Creation & Configuration
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=1, column=0, sticky="nswe")
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # Left Section in Bottom Fame
        self.bf_left_section = tk.Frame(self.bottom_frame)
        self.bf_left_section.grid(row=0, column=0)

        # Contents of left Section
        self.stream_info = tk.Text(self.bf_left_section, height=6, width=40, bg='lightblue')
        text_to_insert = f'''Frame Width:   {self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}\nFrame Height:  {self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}'''
        self.stream_info.insert(tk.INSERT, text_to_insert)
        self.stream_info.config(state=tk.DISABLED)
        self.stream_info.grid(row=0, column=0)
        self.send_coord_btn = tk.Button(self.bf_left_section, text='Send Coordinates', width=44, pady=5, padx=3,
                                        bg='yellow')
        self.send_coord_btn.grid(row=1, column=0)

        # Right Section in Bottom Fame
        self.bf_right_section = tk.Frame(self.bottom_frame)
        self.bf_right_section.grid(row=0, column=1)

        # Button Creation
        self.captured_coord = tk.Text(self.bf_right_section, height=8, width=30, bg='light green')
        text_to_insert2 = f'Click at an object in the video to get its Longitude and Latitude'
        self.captured_coord.insert(tk.INSERT, text_to_insert2)
        self.captured_coord.config(state=tk.DISABLED)
        self.captured_coord.grid(row=0, column=0)

        # Update image on canvas
        self.update_image()

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)  # to RGB
        self.image = Image.fromarray(self.image)  # to PIL format
        self.image = self.image.resize((self.width, self.height))
        self.image = self.add_corners(self.image, 50)
        self.image = ImageTk.PhotoImage(self.image)  # to ImageTk format

        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)
