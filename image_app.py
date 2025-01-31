import cv2
import tkinter as tk

from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from abc import abstractmethod

class ImageProcessingApp:
    """
    ImageProcessingApp is a GUI application for loading, displaying, processing, and saving images.
    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        btn_load (tk.Button): Button to load an image.
        btn_save (tk.Button): Button to save the processed image.
        image_label (tk.Label): Label to display the loaded or processed image.
        original_image (np.ndarray): The original loaded image.
        result_image (np.ndarray): The processed image.
        max_width (int): Maximum width for displaying the image.
        max_height (int): Maximum height for displaying the image.
    """

    def __init__(self, root):
        self.root = root

        self.btn_load = tk.Button(root, text="Wczytaj obraz", command=self.load_image)
        self.btn_load.pack()

        self.btn_save = tk.Button(root, text="Zapisz obraz", command=self.save_image)
        self.btn_save.pack()
        
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack()
        self.progress["value"] = 0  # Startowa wartość

        self.original_image = None
        self.result_image = None

        self.max_width = 1000
        self.max_height = 1000

    def load_image(self):
        """
        Prompts the user to select an image file and loads the selected image.

        This method opens a file dialog to allow the user to select an image file
        with extensions .jpg, .png, or .jpeg. If a file is selected, it reads the
        image using OpenCV and displays it using the display_image method.

        Attributes:
            file_path (str): The path to the selected image file.
            original_image (numpy.ndarray): The image read from the selected file.
        """
        self.file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png;*.jpeg")])
        if self.file_path:
            self.original_image = cv2.imread(self.file_path)
            self.display_image(self.original_image)

    def resize_to_fit(self, image):
        """
        Resize the given image to fit within the maximum width and height while maintaining the aspect ratio.

        Parameters:
        image (numpy.ndarray): The input image to be resized.

        Returns:
        numpy.ndarray: The resized image.
        """
        h, w = image.shape[:2]
        scale = min(self.max_width / w, self.max_height / h) 
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(image, (new_w, new_h))

    def display_image(self, image):
        """
        Displays the given image in the application window.

        This method resizes the image to fit the display area, converts it from BGR to RGB format,
        and then converts it to a format suitable for displaying in a Tkinter Label widget.

        Args:
            image (numpy.ndarray): The image to be displayed, represented as a NumPy array.
        """
        image = self.resize_to_fit(image) 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    @abstractmethod
    def process_image(self):
        """
        Processes the image by applying background replacement or other transformations.
        
        This method is a placeholder and should be implemented with the actual image processing logic.
        
        Returns:
            None
        """
        pass

    def save_image(self):
        """
        Saves the result image to a file selected by the user.

        This method opens a file dialog to allow the user to choose a location and filename
        for saving the result image. The image can be saved in either JPEG or PNG format.
        If the user selects a valid file path, the image is saved to that location.

        Returns:
            None
        """
        if self.result_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG files", "*.jpg"),
                                                                ("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.result_image)
                print("Zapisano:", file_path)

    def update_progress(self, value):
        """
        Updates the progress bar with the given value.

        Args:
            value (int): The new value to set for the progress bar.
        """
        self.progress["value"] = value
        self.root.update_idletasks()