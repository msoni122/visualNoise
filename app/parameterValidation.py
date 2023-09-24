from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from typing import Tuple, Optional

from app.noiseWindow import NoiseFrameWindow

class InputDialogApp(QWidget):
    """
    This class manages the UI for gathering and validating parameters for visual noise frames.
    """

    def __init__(self):
        super().__init__()
        self.noise_frame_window: Optional[NoiseFrameWindow] = None
        self.initUI()

    def initUI(self):
        """
        Sets up the UI to gather the parameters.
        """
        self.setWindowTitle('Parameter Collection')
        layout = QVBoxLayout()

        tldr = QLabel('<b>If inputs are invalid, it will run noise with default values: 5, 25, 500, 120000</b>')

        label1 = QLabel('Enter Length of M-Sequence [ between 2 and 32 ]:')
        self.input_sequence_length = QLineEdit()

        label2 = QLabel('Enter Image Size in Pixels [ between 2 and 1080 ]:')
        self.input_image_size = QLineEdit()

        label3 = QLabel('Enter Length of Time to Show Each Frame (in milliseconds) [ between 200 and 60000 ]:')
        self.input_frame_duration = QLineEdit()

        label4 = QLabel('Enter Length of Time for Frames to be Produced and Run (in milliseconds) [ between 500 and 120000 ]:')
        self.total_duration = QLineEdit()

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.showNoiseFrameWindow)

        layout.addWidget(tldr)
        layout.addWidget(label1)
        layout.addWidget(self.input_sequence_length)
        layout.addWidget(label2)
        layout.addWidget(self.input_image_size)
        layout.addWidget(label3)
        layout.addWidget(self.input_frame_duration)
        layout.addWidget(label4)
        layout.addWidget(self.total_duration)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def collectParameters(self) -> Tuple[int, int, int, int]:
        """
        Collects and validates user input parameters.

        Returns:
            A tuple containing sequence_length, image_size, frame_duration, and total_duration.
        """
        try:
            sequence_length = int(self.input_sequence_length.text())
            image_size = int(self.input_image_size.text())
            frame_duration = int(self.input_frame_duration.text())
            total_duration = int(self.total_duration.text())

            if sequence_length < 2 or sequence_length > 32:
                raise ValueError("Sequence length must be between 2 and 32")

            if image_size <= 0 or image_size > 1080:
                raise ValueError("Image size must be between 1 and 1080")

            if frame_duration < 200 or frame_duration > 60000:
                raise ValueError("Frame duration must be between 200 and 60000 milliseconds")

            if total_duration < 500 or total_duration > 120000 or total_duration < frame_duration // 2:
                raise ValueError("Total duration must be between 500 and 120000 milliseconds and at least twice as long as frame duration")

        except ValueError as e:
            QMessageBox.warning(self, 'Invalid Input', str(e))
            default_params = 5, 25, 500, 120000
            return default_params

        return sequence_length, image_size, frame_duration, total_duration

    def showNoiseFrameWindow(self):
        """
        Takes user input, performs basic validation, and displays the corresponding frames.
        """
        parameters = self.collectParameters()
        self.close()
        if self.noise_frame_window is None:
            self.noise_frame_window = NoiseFrameWindow(*parameters)
        self.noise_frame_window.show()