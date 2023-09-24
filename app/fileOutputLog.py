from PyQt5.QtCore import QDateTime

from typing import List

class RecreatableFrame:
    def __init__(self, frame_states):
        self.timestamp = currentTimestamp()
        self.frame_states = frame_states
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'frame_states': [nparr.tolist() for nparr in self.frame_states ]
        }

class LoggedFrames:
    def __init__(self, sequence_length: int, image_size: int, frames: List[RecreatableFrame]):
        self.sequence_length = sequence_length
        self.image_size = image_size
        self.frames = frames

    def to_dict(self):
        return {
            'sequence_length': self.sequence_length,
            'image_size': self.image_size,
            'frames': [frame.to_dict() for frame in self.frames]
        }
    

def currentTimestamp():
        current_time = QDateTime.currentDateTime()
        timestamp = current_time.toString("yyyy-MM-dd hh:mm:ss.zzz")
        return timestamp