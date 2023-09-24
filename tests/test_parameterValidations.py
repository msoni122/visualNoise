import unittest
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication

from app.parameterValidation import InputDialogApp

class TestInputDialogApp(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.dialog = InputDialogApp()
        self.dialog.noise_frame_window = Mock()

    def tearDown(self):
        self.app.exit()

    def test_collectParameters_valid(self):
        self.dialog.input_sequence_length.setText("5")
        self.dialog.input_image_size.setText("100")
        self.dialog.input_frame_duration.setText("1000")
        self.dialog.total_duration.setText("2000")
        params = self.dialog.collectParameters()
        self.assertEqual(params, (5, 100, 1000, 2000))
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_collectParameters_invalid(self, mock_warning):
        self.dialog.input_sequence_length.setText("35")
        self.dialog.input_image_size.setText("-10")
        self.dialog.input_frame_duration.setText("300000")
        self.dialog.total_duration.setText("1000")
        params = self.dialog.collectParameters()
        self.assertEqual(params, (5, 25, 500, 120000))

    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_showNoiseFrameWindow(self, mock_warning):
        self.dialog.showNoiseFrameWindow()
        self.assertTrue(self.dialog.noise_frame_window.show.called)
