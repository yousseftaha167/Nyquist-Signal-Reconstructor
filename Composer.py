import os
import sys
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider)
from PyQt5.QtCore import Qt


class CustomMessageBox(QtWidgets.QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(400, 250, 300, 100)
        self.setStyleSheet("background-color: rgb(30,30,30); color: rgb(255, 255, 255);")

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button = QPushButton("OK")
        button.setStyleSheet("background-color: rgb(30, 30, 30); color: rgb(255, 255, 255);")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)


class SignalComposer(QMainWindow):
    def __init__(self, parent=None):
        super(SignalComposer, self).__init__(parent)
        self.setWindowTitle("Signal Composer")

        # Set initial geometry to start at minimum size
        self.setGeometry(850, 55, 315, 200)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:transparent;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color:rgb(50,50,50); border-radius: 10px;")
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        font = QFont("Times New Roman", 22)

        self.num_terms_label = QLabel("Frequencies Number In Signal")
        self.num_terms_label.setFont(font)
        self.num_terms_label.setStyleSheet("color:rgb(191, 191, 191);")
        self.layout.addWidget(self.num_terms_label)

        self.num_terms_input = QLineEdit()
        self.num_terms_input.setFixedHeight(30)
        self.num_terms_input.setStyleSheet("background-color: rgb(15, 15, 15); color: rgb(255, 255, 255);")
        self.layout.addWidget(self.num_terms_input)

        self.freq_amp_layout = QVBoxLayout()
        self.layout.addLayout(self.freq_amp_layout)

        self.generate_terms_button = QPushButton("Generate Terms")
        self.generate_terms_button.setStyleSheet(self.button_style())
        self.generate_terms_button.clicked.connect(self.generate_term_inputs)
        self.layout.addWidget(self.generate_terms_button)

        self.use_signal_button = QPushButton("Use Signal")
        self.use_signal_button.setStyleSheet(self.button_style())
        self.layout.addWidget(self.use_signal_button)

        self.action_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.action_buttons_layout)

        self.save_signal_button = QPushButton("Save Signal")
        self.save_signal_button.setStyleSheet(self.button_style())
        self.save_signal_button.clicked.connect(self.save_signal)
        self.action_buttons_layout.addWidget(self.save_signal_button)
        self.save_signal_button.hide()
        self.use_signal_button.hide()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(self.button_style())
        self.cancel_button.clicked.connect(self.reset_operation)
        self.action_buttons_layout.addWidget(self.cancel_button)

        self.freq_inputs = []
        self.amp_inputs = []
        self.phase_inputs = []
        self.clean_signal = None
        self.time = None

        self.hide()

    def reset_state(self):
        for i in reversed(range(self.freq_amp_layout.count())):
            layout_item = self.freq_amp_layout.itemAt(i)
            if layout_item is not None:
                layout = layout_item.layout()
                if layout is not None:
                    for j in reversed(range(layout.count())):
                        widget = layout.itemAt(j).widget()
                        if widget is not None:
                            widget.deleteLater()
                    layout_item.deleteLater()

        self.clean_signal = None
        self.time = None
        self.freq_inputs.clear()
        self.amp_inputs.clear()
        self.phase_inputs.clear()
        self.num_terms_input.clear()
        self.generate_terms_button.show()
        self.save_signal_button.hide()
        self.use_signal_button.hide()
        self.num_terms_input.setReadOnly(False)
        self.setGeometry(850, 55, 315, 200)

    def validate_inputs(self):
        for freq_input, amp_input, phase_input in zip(self.freq_inputs, self.amp_inputs, self.phase_inputs):
            freq_value = freq_input.text()
            amp_value = amp_input.text()
            phase_value = phase_input.text()

            if not freq_value or not amp_value:
                return False, "All Amplitudes and Frequency must be filled."
            try:
                float(freq_value)
                float(amp_value)
                if phase_value:  # Only validate phase if provided
                    float(phase_value)
            except ValueError:
                return False, "Please enter valid numbers for frequencies, amplitudes, and optional phases."

        return True, ""

    def generate_term_inputs(self):
        for i in reversed(range(self.freq_amp_layout.count())):
            layout_item = self.freq_amp_layout.itemAt(i)
            if layout_item is not None:
                layout = layout_item.layout()
                if layout is not None:
                    for j in reversed(range(layout.count())):
                        widget = layout.itemAt(j).widget()
                        if widget is not None:
                            widget.deleteLater()
                    layout_item.deleteLater()

        try:
            num_terms = int(self.num_terms_input.text())
            self.freq_inputs = []
            self.amp_inputs = []
            self.phase_inputs = []
            new_height = 200 + num_terms * 25
            self.setGeometry(850, 55, 315, new_height)

            for i in range(num_terms):
                term_layout = QHBoxLayout()

                line_label = QLineEdit(self)
                line_label.setText(f"Term {i + 1}")
                line_label.setFixedWidth(50)
                line_label.setStyleSheet("color: rgb(255, 255, 255);")
                term_layout.addWidget(line_label)

                amp_input = QLineEdit(self)
                amp_input.setPlaceholderText("Amplitude")
                amp_input.setStyleSheet("background-color: rgb(15, 15, 15); color: rgb(255, 255, 255);")
                term_layout.addWidget(amp_input)
                self.amp_inputs.append(amp_input)

                freq_input = QLineEdit(self)
                freq_input.setPlaceholderText("Frequency")
                freq_input.setStyleSheet("background-color: rgb(15, 15, 15); color: rgb(255, 255, 255);")
                term_layout.addWidget(freq_input)
                self.freq_inputs.append(freq_input)

                phase_input = QLineEdit(self)
                phase_input.setPlaceholderText("Phase")
                phase_input.setStyleSheet("background-color: rgb(15, 15, 15); color: rgb(255, 255, 255);")
                term_layout.addWidget(phase_input)
                self.phase_inputs.append(phase_input)

                self.freq_amp_layout.addLayout(term_layout)

            self.generate_terms_button.hide()
            self.num_terms_input.setReadOnly(True)
            self.save_signal_button.show()
            self.use_signal_button.show()
        except ValueError:
            self.show_error_message("Please enter a valid integer for the number of terms.")

    def generate_signal(self):
        valid, error_message = self.validate_inputs()
        if not valid:
            self.show_error_message(error_message)
            return np.array([]), np.array([])

        frequencies = [float(freq.text()) for freq in self.freq_inputs]
        amplitudes = [float(amp.text()) for amp in self.amp_inputs]

        # Convert phase from degrees to radians, with a default of 0 radians if left empty
        phases = [np.radians(float(phase.text())) if phase.text() else 0.0 for phase in self.phase_inputs]

        sample_rate = 1000
        duration = 1
        self.time, self.clean_signal = self.generate_clean_signal(frequencies, amplitudes, phases, sample_rate,
                                                                  duration)

        if len(self.clean_signal) == 0 or len(self.time) == 0:
            return np.array([]), np.array([])

        return self.time, self.clean_signal

    def save_signal(self):
        self.generate_signal()
        if self.time is None or self.clean_signal is None:
            return

        # Define the base folder path and make sure the folder exists
        generated_signal_folder = "Data/Generated_Signal"
        os.makedirs(generated_signal_folder, exist_ok=True)

        # Create the base filename and save path
        base_filename = "generated_signal_" + "_".join(
            [f"{freq}Hz" for freq in [float(freq.text()) for freq in self.freq_inputs]]
        )
        clean_path = os.path.join(generated_signal_folder, f"{base_filename}.csv")

        # Save the DataFrame as CSV
        clean_df = pd.DataFrame({'Time': self.time, 'Signal': self.clean_signal})
        clean_df.to_csv(clean_path, index=False)
        self.save_signal_button.setText("Saved")

    def generate_clean_signal(self, frequencies, amplitudes, phases, sample_rate, duration):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        signal = np.zeros_like(t)

        for freq, amp, phase in zip(frequencies, amplitudes, phases):
            signal += amp * np.sin(2 * np.pi * freq * t + phase)

        return t, signal

    def reset_operation(self):
        self.reset_state()
        self.hide()

    def show_error_message(self, message):
        error_dialog = CustomMessageBox(message)
        error_dialog.exec_()

    def button_style(self):
        return ("QPushButton { border: none; padding: 10px; color: rgb(255, 255, 255); "
                "background-color: rgb(15,15,15); border-bottom: 2px solid transparent; } "
                "QPushButton:hover { background-color:rgb(30, 30, 30); }")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalComposer()
    window.show()
    sys.exit(app.exec_())
