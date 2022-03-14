# imports
import threading
from tkinter import *
import cv2
from CoordinatesGetSendUI.coordinates_transfer_ui import CoordinatesTransferGUI
import imageio
from PIL import Image, ImageTk

# Constants & Variables
root = Tk()  # Parent Window
video_name = r"D:\Datasets\Computer Vision\Rizwan_Old_Drone_Recorded\TrimedVideos\Asad_Rizzwan_Traimmed.mp4"  # This is your video file path
video = imageio.get_reader(video_name)


# ==== Functions ===== #
# Video Streaming
def stream(label):
    for image in video.iter_data():
        img = Image.fromarray(image)
        img = img.resize((300, 300))
        frame_image = ImageTk.PhotoImage(img)
        label.config(image=frame_image)
        print(frame_image.width())
        label.image = frame_image


# main
if __name__ == "__main__":
    # Allow resize
    root.resizable(True, True)
    # set title
    root.title("Mission Planner")
    # Set minimum size for root window
    # root.geometry("650x400")
    root.geometry("")

    # Saved Video streaming to tkinter
    # my_label = Label(root)
    # my_label.pack()
    # thread = threading.Thread(target=stream, args=(my_label,))
    # thread.daemon = 1
    # thread.start()

    # MissionPlanner IInitialization
    CoordinatesTransferGUI(root, cv2.VideoCapture(0))
    # Main event loop of root window
    root.mainloop()
