from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from scipy.signal import max_len_seq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import json
import numpy as np

from app.fileOutputLog import *

class NoiseFrameWindow(QWidget):
    def __init__(self, sequence_length, image_size, frame_duration, total_duration):
        super().__init__()
        self.sequence_length = sequence_length
        self.image_size = image_size
        self.frame_duration = frame_duration
        self.total_duration = total_duration
        self.initUI()

    def initUI(self):
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

    def start_timer(self, interval, total_time):
        timer = QTimer(self)
        timer_2 = QTimer(self)
        timer.timeout.connect(self.update_visualization)
        timer_2.timeout.connect(self.close_visualization)
        timer.start(interval)
        timer_2.start(total_time)
        return timer

    def close_visualization(self):
        self.close()
        data = self.log.to_dict()
        with open(f'../files/visualNoise_{currentTimestamp()}.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print("LoggedFrames instance dumped as JSON.")

    def update_visualization(self):

        # Clear the previous frame
        self.ax.clear()

        def generate_non_zero_state(sequence_length):
            while True:
                state = np.random.randint(0, 2, sequence_length)
                if np.any(state):
                    return state

        
        random_states = [ generate_non_zero_state(self.sequence_length) for _ in range(self.image_size) ]
        m_sequences = [max_len_seq(self.sequence_length, state=random_states[i])[0] for i in range(self.image_size)]
        image = np.vstack(m_sequences)
        
        self.log.frames.append(RecreatableFrame(random_states))

        # Display the binary sequence as a 2D image
        self.ax.imshow(image, cmap='gray', interpolation='nearest', aspect='auto')
        self.ax.axis('off')
        self.canvas.draw()