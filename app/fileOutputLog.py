from PyQt5.QtCore import QDateTime

from typing import List
import numpy as np

import json

class RecreatableFrame:
    """
    Represents a frame that can be recreated from its states.
    """
    def __init__(self, frame_states: List[np.ndarray]) -> None:
        """
        Initializes a RecreatableFrame instance.

        Args:
            frame_states: Is a list of np arrays: List[ndarray[int]])
        """
        self.timestamp = current_timestamp()
        self.frame_states = frame_states
    
    def to_dict(self) -> dict:
        """
        Converts the RecreatableFrame to a dictionary.

        Returns:
            dict: A dictionary representation of the RecreatableFrame.
        """
        return {
            'timestamp': self.timestamp,
            'frame_states': [nparr.tolist() for nparr in self.frame_states]
        }

class LoggedFrames:
    """
    Represents a collection of logged frames.
    """
    def __init__(self, sequence_length: int, image_size: int, frames: List[RecreatableFrame]) -> None:
        """
        Initializes a LoggedFrames instance.

        Args:
            sequence_length (int): The length of the sequence.
            image_size (int): The size of the image.
            frames (List[RecreatableFrame]): A list of RecreatableFrame instances.
        """
        self.sequence_length = sequence_length
        self.image_size = image_size
        self.frames = frames

    def to_dict(self) -> dict:
        """
        Converts the LoggedFrames to a dictionary.

        Returns:
            dict: A dictionary representation of the LoggedFrames.
        """
        return {
            'sequence_length': self.sequence_length,
            'image_size': self.image_size,
            'frames': [frame.to_dict() for frame in self.frames]
        }

def current_timestamp() -> str:
    """
    Get the current timestamp in the format "yyyy-MM-dd hh:mm:ss.zzz".

    Returns:
        str: The current timestamp.
    """
    current_time = QDateTime.currentDateTime()
    timestamp = current_time.toString("yyyy-MM-dd hh:mm:ss.zzz")
    return timestamp

def save_data_to_json(data: dict) -> None:
    """
    Save the data to a JSON file.

    OutputFile:
        {
        "sequence_length": 5,
        "image_size": 50,
        "frames": [
            {
            "timestamp": "2023-09-23 21:25:45.814",
            "frame_states": [...]
            }
        ]}
    """
    file_name = f'files/visualNoise_{current_timestamp()}.json'
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print("LoggedFrames instance dumped as JSON.")
