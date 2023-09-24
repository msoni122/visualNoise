import unittest
from unittest.mock import patch
import numpy as np

from app.fileOutputLog import RecreatableFrame, LoggedFrames

class TestRecreatableFrame(unittest.TestCase):
    def setUp(self):
        self.frame_states = [np.array([1, 0, 1]), np.array([0, 1, 0])]
        self.frame_states_python = [[1, 0, 1], [0, 1, 0]]

    def test_creation(self):
        frame = RecreatableFrame(self.frame_states)
        self.assertEqual(frame.frame_states, self.frame_states)

    def test_to_dict(self):
        frame = RecreatableFrame(self.frame_states)
        self.assertTrue(np.array_equal(frame.frame_states, self.frame_states))
        expected_dict = {
            'timestamp': frame.timestamp,
            'frame_states': self.frame_states_python
        }
        self.assertEqual(frame.to_dict(), expected_dict)

class TestLoggedFrames(unittest.TestCase):
    def setUp(self):
        frame1 = RecreatableFrame([np.array([1, 0, 1]), np.array([0, 1, 0])])
        frame2 = RecreatableFrame([np.array([0, 1, 0]), np.array([1, 0, 1])])
        self.logged_frames = LoggedFrames(sequence_length=3, image_size=2, frames=[frame1, frame2])

    def test_creation(self):
        self.assertEqual(self.logged_frames.sequence_length, 3)
        self.assertEqual(self.logged_frames.image_size, 2)
        self.assertEqual(len(self.logged_frames.frames), 2)

    def test_to_dict(self):
        expected_dict = {
            'sequence_length': 3,
            'image_size': 2,
            'frames': [
                {
                    'timestamp': self.logged_frames.frames[0].timestamp,
                    'frame_states': [ frame.tolist() for frame in self.logged_frames.frames[0].frame_states ]
                },
                {
                    'timestamp': self.logged_frames.frames[1].timestamp,
                    'frame_states': [ frame.tolist() for frame in self.logged_frames.frames[1].frame_states ]
                }
            ]
        }
        self.assertEqual(self.logged_frames.to_dict(), expected_dict)
