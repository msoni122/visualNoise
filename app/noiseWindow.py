from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from scipy.signal import max_len_seq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from typing import List, Tuple

from app.fileOutputLog import LoggedFrames, RecreatableFrame, save_data_to_json

class NoiseFrameWindow(QWidget):
    """
    This is where the m-sequences are calculated and displayed to create the visual noise
    """
    def __init__(self, sequence_length: int, image_size: int, frame_duration: int, total_duration: int):
        super().__init__()
        self.sequence_length = sequence_length
        self.image_size = image_size
        self.frame_duration = frame_duration
        self.total_duration = total_duration
        self.initUI()

    def initUI(self):
        """
        Initialize the UI components and layout.
        """
        self.setWindowTitle("Visual Noise Frames")
        layout = QVBoxLayout()
        self.setGeometry(100, 100, 800, 600)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.figure.add_subplot()
        self.log = LoggedFrames(self.sequence_length, self.image_size, [])
        self.timer = self.start_timer(self.frame_duration, self.total_duration)

    def create_timer(self, slot, interval: int) -> QTimer:
        """
        Create a QTimer and connect it to the specified slot with the given interval.
        """
        timer = QTimer(self)
        timer.timeout.connect(slot)
        timer.start(interval)
        return timer
    
    def start_timer(self, interval: int, total_time: int) -> None:
        """
        Start two timers for updating the visualization and closing the window.
        """
        visualization_timer = self.create_timer(self.update_visualization, interval)
        close_timer = self.create_timer(self.close_visualization, total_time)

        return None

    def close_visualization(self) -> None:
        """
        Close the visualization window and save data to a JSON file.
        """
        self.close()
        data = self.log.to_dict()
        save_data_to_json(data)

    def update_visualization(self) -> None:
        """
        Update the visualization with a new frame.
        """
        self.ax.clear()
        random_states, m_sequences = self.generate_msequence_image()
        self.log.frames.append(RecreatableFrame(random_states))
        self.display_image(np.vstack(m_sequences))

    
    def generate_non_zero_state(self) -> np.ndarray:
        """
        Generate a random state with at least one non-zero element.
        """
        while True:
            state = np.random.randint(0, 2, self.sequence_length)
            if np.any(state):
                return state
            

    def generate_max_len_seq(self, state: np.ndarray) -> np.ndarray:
        """
        Generate a max-length sequence for the given state.
        """
        return max_len_seq(self.sequence_length, state=state)[0]

    
    def generate_msequence_image(self) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Generate random states and max-length sequences to create an m-sequence image.
        """
        random_states = [self.generate_non_zero_state() for _ in range(self.image_size)]
        m_sequences = [self.generate_max_len_seq(state) for state in random_states]
        return random_states, m_sequences


    def display_image(self, image: np.ndarray):
        """
        Display the binary sequence as a 2D image.
        """
        self.ax.imshow(image, cmap='gray', interpolation='nearest', aspect='auto')
        self.ax.axis('off')
        self.canvas.draw()
