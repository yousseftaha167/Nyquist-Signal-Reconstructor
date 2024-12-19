import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from pyqtgraph import PlotWidget
import numpy as np
from Design import Ui_MainWindow
import Composer
from Composer import SignalComposer, CustomMessageBox
from scipy.signal import find_peaks


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up UI from the design file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plot_difference_mode = True
        self.toggle_plot_mode_button_name()
        self.is_reconstructed = False  # Flag to indicate if signal is reconstructed
        self.frequency_ratio_mode = False

        self.composer = Composer.SignalComposer(self)
        self.error_object = CustomMessageBox(self)

        # Set up plot widgets
        self.setup_plot_widgets()

        # Add items to the combo box
        self.ui.reconstruction_method.addItems([
            "Sinc Interpolation",
            "Zero-Order Hold",
            "Lanczos Resampling"
        ])
        self.ui.reconstruction_method.setCurrentIndex(0)

        # Connect the "Upload Signal" button to the upload_signal function
        self.ui.upload_signal.clicked.connect(self.upload_signal)
        self.ui.sampling_frequency.valueChanged.connect(self.update_sampling_frequency)
        self.ui.frequency_value_label_button.clicked.connect(self.toggle_frequency_mode)
        self.ui.SNR_level.valueChanged.connect(self.update_snr)
        self.composer.use_signal_button.clicked.connect(self.use_signal)

        # Connect combo box to method
        self.ui.reconstruction_method.currentIndexChanged.connect(self.update_reconstruction_method)
        self.ui.signal_composer.clicked.connect(self.open_signal_composer)
        self.ui.toggle_plot_button.clicked.connect(self.toggle_plot_mode)
        self.ui.set_min_valid_frequency.clicked.connect(self.set_min_valid_frequency)

        self.load_signal_data("Data/signal_5Hz_20Hz_50Hz.csv")

        # Run initial reconstruction with the selected method
        self.update_reconstruction_method

    def open_signal_composer(self):
        self.composer.show()  # Use show() instead of exec_()

    def setup_plot_widgets(self):
        """
        Initializes PlotWidgets for displaying different signal plots in designated group boxes.
        """
        self.plot_widget_1 = PlotWidget(self.ui.groupBox)
        self.plot_widget_1.setGeometry(QRect(3, 30, 615, 280))

        self.plot_widget_2 = PlotWidget(self.ui.groupBox_2)
        self.plot_widget_2.setGeometry(QRect(3, 30, 615, 280))

        self.plot_widget_3 = PlotWidget(self.ui.groupBox_3)
        self.plot_widget_3.setGeometry(QRect(3, 30, 615, 280))

        self.plot_widget_4 = PlotWidget(self.ui.groupBox_4)
        self.plot_widget_4.setGeometry(QRect(3, 30, 615, 280))

    def upload_signal(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Signal File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_name:
            try:
                self.load_signal_data(file_name)
            except ValueError:
                self.show_error_message("Error loading file. Ensure it's formatted correctly.")

    def load_signal_data(self, file_name):
        try:

            # Load the signal data from the file
            data = np.loadtxt(file_name, delimiter=',', skiprows=1)
            if data.shape[1] != 2:
                raise ValueError("File must contain exactly two columns: Time and Signal.")

            time = data[:, 0]
            amplitude = data[:, 1]

            # Pass the time and amplitude to the processing function
            self.process_signal_data(time, amplitude)

        except IOError:
            self.show_error_message("Error opening the file. Please check the file path.")
        except ValueError as ve:
            self.show_error_message(str(ve))

    def process_signal_data(self, time, amplitude):
        try:
            # Assign the time and amplitude data
            self.time = time
            self.amplitude = amplitude

            # Call print_frequencies to analyze and print frequencies
            self.print_frequencies()

            # Plot the signal data
            self.plot_signal()

            # Automatically set initial sampling frequency
            initial_sampling_frequency = self.ui.sampling_frequency.minimum()
            self.ui.sampling_frequency.setValue(initial_sampling_frequency)
            self.update_sampling_frequency(initial_sampling_frequency)

            # Set the SNR slider to its minimum value
            max_snr_value = self.ui.SNR_level.maximum()
            self.ui.SNR_level.setValue(max_snr_value)
            self.update_snr(max_snr_value)

            # Automatically reconstruct after signal upload
            self.sample_and_reconstruct_signal()

        except ValueError:
            self.show_error_message(
                "Error processing signal data. Please ensure it is formatted correctly with 'Time,Signal' values."
            )

    def use_signal(self):
        time_data, amplitude_data = self.composer.generate_signal()
        # Check if the returned arrays are empty or too short
        if time_data.size == 0 or amplitude_data.size == 0:
            self.show_error_message("No valid signal generated to use.")
            return
        if time_data.size < 10:
            self.show_error_message("Generated signal is too short for processing.")
            return

        self.process_signal_data(time_data, amplitude_data)
        self.composer.reset_operation()

    def plot_signal(self):
        # Clear and plot the signal data
        self.plot_widget_1.clear()
        self.plot_widget_1.plot(self.time, self.amplitude, pen='b')
        # frequency domain
        time_step = np.mean(np.diff(self.time))

        n = len(self.amplitude)
        amplitude_fft = np.fft.fft(self.amplitude)
        frequencies = np.fft.fftfreq(n, d=time_step)

        # positive_freqs = frequencies[:n // 2]
        # magnitude = np.abs(amplitude_fft[:n // 2])

        self.plot_widget_4.clear()
        self.plot_widget_4.plot(frequencies, np.abs(amplitude_fft) / n, pen='r')

        self.plot_widget_4.setXRange(-300, 300)

    def add_noise(self, snr_db):
        """
        Adds noise to the signal based on the specified SNR (dB).
        """
        # Calculate signal power and noise power based on SNR
        signal_power = np.mean(self.amplitude ** 2)
        snr_linear = 10 ** (snr_db / 20)
        noise_power = signal_power / snr_linear

        # Generate white Gaussian noise
        noise = np.random.normal(0, np.sqrt(noise_power), self.amplitude.shape)

        # Add noise to the signal
        self.noisy_signal = self.amplitude + noise

        # Clear plot and show noisy signal
        self.plot_widget_1.clear()
        self.plot_widget_1.plot(self.time, self.noisy_signal, pen='b', name='Noisy Signal')

    def update_snr(self, value):
        """
        Updates the SNR based on the UI slider and re-generates the noisy signal.
        """
        self.snr = value
        print("Current SNR (dB):", self.snr)

        # Re-generate the noisy signal with updated SNR
        if hasattr(self, 'time') and hasattr(self, 'amplitude'):
            self.add_noise(self.snr)
            self.sample_and_reconstruct_signal()  # Trigger signal sampling and reconstruction
        # Update the SNR value label to show the current SNR as a percentage
        self.ui.SNR_value_label.setText(f"{self.snr}%")  # Update the label with the current value

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("File Load Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    def print_frequencies(self, threshold=0.1, max_frequencies=None):
        """
        Calculates and prints the dominant frequencies in the uploaded signal.
        Parameters:
            - threshold: Minimum magnitude to consider a frequency as dominant.
            - max_frequencies: Maximum number of dominant frequencies to print (set to None for all).
        """
        if hasattr(self, 'time') and hasattr(self, 'amplitude'):
            time_step = np.mean(np.diff(self.time))
            sampling_rate = 1 / time_step

            n = len(self.amplitude)
            amplitude_fft = np.fft.fft(self.amplitude)
            frequencies = np.fft.fftfreq(n, d=time_step)

            positive_freqs = frequencies[:n // 2]
            magnitude = np.abs(amplitude_fft[:n // 2])

            # Identify peaks and filter by threshold
            peaks, _ = find_peaks(magnitude, height=threshold)
            peak_freqs = positive_freqs[peaks]
            peak_magnitudes = magnitude[peaks]

            # Sort frequencies by magnitude in descending order
            sorted_indices = np.argsort(peak_magnitudes)[::-1]

            # Select top frequencies based on max_frequencies or print all above threshold
            if max_frequencies:
                dominant_frequencies = peak_freqs[sorted_indices][:max_frequencies]
            else:
                dominant_frequencies = peak_freqs[sorted_indices]
            # Print the dominant frequencies
            self.max_signal_frequeny = max(dominant_frequencies)
            self.max_slide_frequency = int(4 * max(dominant_frequencies))
            self.ui.sampling_frequency.setRange(1, self.max_slide_frequency)

    def update_sampling_frequency(self, value):
        """
        Update the sampling frequency from the slider or programmatically.
        """
        self.current_sample_frequency = value
        print(f"Updating Sampling Frequency (Hz): {self.current_sample_frequency}")

        # Update button display
        self.update_frequency_mode()

        # Process the signal based on the updated sampling frequency
        self.sample_and_reconstruct_signal()

        # Explicitly synchronize the slider if necessary
        if self.ui.sampling_frequency.value() != self.current_sample_frequency:
            self.ui.sampling_frequency.blockSignals(True)
            self.ui.sampling_frequency.setValue(self.current_sample_frequency)
            self.ui.sampling_frequency.blockSignals(False)

    def set_min_valid_frequency(self):
        """
        Set the slider to the minimum valid frequency using the button.
        """
        f_sample = round((2 * self.max_signal_frequeny) + 1)
        print(f"Setting minimum valid frequency: {f_sample}")

        # Update the slider programmatically
        self.ui.sampling_frequency.blockSignals(True)
        self.ui.sampling_frequency.setValue(f_sample)
        self.ui.sampling_frequency.blockSignals(False)

        # Trigger update_sampling_frequency explicitly to update other components
        self.update_sampling_frequency(f_sample)

    def toggle_frequency_mode(self):
        """
        Toggle between frequency value (Hz) and ratio (%) display on the button.
        """
        self.frequency_ratio_mode = not self.frequency_ratio_mode
        self.update_frequency_mode()

    def update_frequency_mode(self):
        """
        Update the button's display based on the current frequency mode.
        """
        if not self.frequency_ratio_mode:
            self.ui.frequency_value_label_button.setText(f"{self.current_sample_frequency} Hz")
        else:
            percentage = round(self.current_sample_frequency / self.max_signal_frequeny * 100)
            self.ui.frequency_value_label_button.setText(f"{percentage}%")

    def sample_and_reconstruct_signal(self):
        # Ensure that original data exists
        if not hasattr(self, 'time') or not hasattr(self, 'amplitude') or not hasattr(self, 'noisy_signal'):
            return  # No data to process

        # Step 1: Calculate Sampling Interval from Frequency
        time_step = np.mean(np.diff(self.time))  # Time step of original data
        sampling_interval = max(1, int(1 / (self.current_sample_frequency * time_step)))  # Interval in terms of indices

        # Step 2: Downsample the Signal
        self.t_sampled = self.time[::sampling_interval]  # Take samples at intervals
        self.amplitude_sampled = self.amplitude[::sampling_interval]

        # Step 3: Determine reconstruction method based on combo box selection
        t_interp = self.time  # High-resolution time array for reconstruction
        selected_method = self.ui.reconstruction_method.currentText()  # Get selected text from combo box

        if selected_method == "Sinc Interpolation":
            self.reconstructed_signal = self.sinc_interpolation(self.t_sampled, self.amplitude_sampled, t_interp)
        elif selected_method == "Zero-Order Hold":
            self.reconstructed_signal = self.zero_order_hold_interpolation(self.t_sampled, self.amplitude_sampled,
                                                                           t_interp)
        elif selected_method == "Lanczos Resampling":
            self.reconstructed_signal = self.lanczos_resampling(self.t_sampled, self.amplitude_sampled, t_interp)
        else:
            print(f"Reconstruction method '{selected_method}' not recognized.")
            self.reconstructed_signal = np.zeros_like(t_interp)  # Fallback if no method matches

        # Step 4: Calculate the Original SNR
        # self.noisy_signal contains the original signal with noise
        signal_power = np.mean(self.amplitude ** 2)  # Power of the clean signal
        noise_power = np.mean(
            (self.noisy_signal - self.amplitude) ** 2)  # Power of the noise in the original noisy signal
        original_snr_linear = signal_power / noise_power  # Original SNR in linear scale
        original_noise_power = signal_power / original_snr_linear

        noise_scale = 1 - (self.current_sample_frequency / self.max_slide_frequency)
        print(f"Noise Scale is {noise_scale * 100}%")

        # Step 5: Add noise to the reconstructed signal based on original SNR
        noise = np.random.normal(0, np.sqrt(original_noise_power * noise_scale), self.reconstructed_signal.shape)
        self.reconstructed_signal_noisy = self.reconstructed_signal + noise

        # Step 6: Plot Original, Sampled, and Noisy Reconstructed Signals
        self.plot_widget_1.clear()  # Clear original signal plot
        self.plot_widget_1.plot(self.time, self.noisy_signal, pen='b', name='Noisy Signal')
        self.plot_widget_1.plot(
            self.t_sampled,
            self.amplitude_sampled,
            pen=None,
            symbol='o',
            symbolBrush='r',
            symbolSize=2.5,
            name='Sampled Points'
        )
        self.plot_widget_3.clear()

        # if self.current_sample_frequency <= 2 * self.max_signal_frequeny:
        #     self.current_reconstructed_signal = self.reconstructed_signal_noisy
        # else:
        #     self.current_reconstructed_signal = self.reconstructed_signal

        self.plot_widget_3.plot(t_interp, self.reconstructed_signal_noisy, pen='g',
                                name='Reconstructed Signal')

        self.update_difference_plot()

        # Define the number of repetitions and the bandwidth
        time_step = np.mean(np.diff(self.time))

        n = len(self.amplitude)
        amplitude_fft = np.fft.fft(self.amplitude)
        frequencies = np.fft.fftfreq(n, d=time_step)
        self.plot_widget_4.clear()

        num_repeats = 10  # Number of bandwidth repetitions
        bandwidth = np.max(self.current_sample_frequency)  # Adjust this value to control the spacing between bands

        # Plot the repeated bands
        for i in range(1, num_repeats + 1):
            # Create a band centered around the original frequencies
            band_shift = i * bandwidth
            self.plot_widget_4.plot(frequencies + band_shift, np.abs(amplitude_fft) / n, pen='b',
                                    name=f'Band {i}')
            self.plot_widget_4.plot(frequencies - band_shift, np.abs(amplitude_fft) / n, pen='b',
                                    name=f'Band -{i}')  # Include negative offsets for symmetry

        self.plot_widget_4.plot(frequencies, np.abs(amplitude_fft) / n, pen='r')

    def update_difference_plot(self):
        # Clear the plot
        self.plot_widget_2.clear()

        # Synchronize x and y axis limits with plot_widget_1
        view_box_1 = self.plot_widget_1.getViewBox()  # Correct way to access the ViewBox
        x_range_1, y_range_1 = view_box_1.viewRange()  # Get the x and y ranges of plot_widget_1

        if self.plot_difference_mode:
            # Plot the difference between the original and reconstructed signals in plot_widget_2
            difference_signal = self.noisy_signal - self.reconstructed_signal_noisy
            self.plot_widget_2.plot(self.time, difference_signal, pen='m', name='Difference (Error)')
        else:
            # Plot both original and reconstructed noisy signals for comparison in plot_widget_2
            self.plot_widget_2.plot(self.time, self.noisy_signal, pen='b', name='Original Signal')
            self.plot_widget_2.plot(self.time, self.reconstructed_signal_noisy, pen='g',
                                    name='Noisy Reconstructed Signal')

        # Set the x and y ranges to match those of plot_widget_1 for plot_widget_2
        self.plot_widget_2.setXRange(*x_range_1, padding=0)
        self.plot_widget_2.setYRange(*y_range_1, padding=0)

        # Plot the reconstructed signal in plot_widget_3 and synchronize ranges
        self.plot_widget_3.setXRange(*x_range_1, padding=0)
        self.plot_widget_3.setYRange(*y_range_1, padding=0)

    def update_reconstruction_method(self):
        """Update the reconstruction method based on the selected combo box item."""
        # Check if the signal data is loaded
        if not hasattr(self, 'time') or not hasattr(self, 'amplitude'):
            print("No signal data loaded. Please upload a signal first.")
            return  # Exit if there's no data to process

        method = self.ui.reconstruction_method.currentText()  # Get selected text from combo box

        t_interp = self.time  # High-resolution time array for reconstruction

        if method == "Sinc Interpolation":
            self.reconstructed_signal = self.sinc_interpolation(self.t_sampled, self.amplitude_sampled, t_interp)
        elif method == "Zero-Order Hold":
            self.reconstructed_signal = self.zero_order_hold_interpolation(self.t_sampled, self.amplitude_sampled,
                                                                           t_interp)
        elif method == "Lanczos Resampling":
            self.reconstructed_signal = self.lanczos_resampling(self.t_sampled, self.amplitude_sampled, t_interp)

        # Update the plot with the new reconstructed signal
        self.plot_widget_1.clear()
        self.plot_signal()
        self.plot_widget_1.plot(
            self.t_sampled,
            self.amplitude_sampled,
            pen=None,
            symbol='o',
            symbolBrush='r',
            symbolSize=4,
            name='Sampled Points'
        )
        self.plot_widget_3.clear()  # Clear reconstructed signal plot
        self.plot_widget_3.plot(t_interp, self.reconstructed_signal, pen='g', name='Reconstructed Signal')
        # Update the difference plot
        self.plot_widget_2.clear()
        difference_signal = self.amplitude - self.reconstructed_signal_noisy
        self.plot_widget_2.plot(self.time, difference_signal, pen='m', name='Difference (Error)')

    def toggle_plot_mode(self):
        self.toggle_plot_mode_button_name()

        # Toggle the plot mode
        self.plot_difference_mode = not self.plot_difference_mode

        # Update the plot based on the current mode
        self.update_difference_plot()

    def toggle_plot_mode_button_name(self):
        if self.plot_difference_mode:
            self.ui.toggle_plot_button.setText("Compared Graphs")
        else:
            self.ui.toggle_plot_button.setText("Sampling Difference")

    def sinc_interpolation(self, t_sampled, amplitude_sampled, t_interp):
        """Reconstruct the signal using sinc interpolation at the specified times."""
        if len(t_sampled) < 2:
            print("Sampling interval too high for interpolation.")
            return np.zeros_like(t_interp)  # Return an array of zeros to avoid errors in reconstruction plot
        T = t_sampled[1] - t_sampled[0]  # Sampling period from sampled data
        reconstructed_signal = np.zeros_like(t_interp)
        for i in range(len(t_sampled)):
            reconstructed_signal += amplitude_sampled[i] * np.sinc((t_interp - t_sampled[i]) / T)
        return reconstructed_signal

    def lanczos_resampling(self, t_sampled, amplitude_sampled, t_interp, a=3):
        """Reconstruct the signal using Lanczos resampling at the specified times."""

        def lanczos_kernel(x, a):
            """Calculate the Lanczos kernel for a given distance and window parameter"""
            if abs(x) < 1e-10:
                return 1
            elif abs(x) > a:
                return 0
            else:
                return np.sinc(x) * np.sinc(x / a)

        if len(t_sampled) < 2:  # Check if we have enough points for interpolation
            print("Not enough points for Lanczos resampling.")
            return np.zeros_like(t_interp)

        reconstructed_signal = np.zeros_like(t_interp)

        for i in range(len(t_interp)):
            for j in range(len(t_sampled)):
                distance = (t_interp[i] - t_sampled[j]) / (t_sampled[1] - t_sampled[0])
                reconstructed_signal[i] += amplitude_sampled[j] * lanczos_kernel(distance, a)
        return reconstructed_signal

    def zero_order_hold_interpolation(self, t_sampled, amplitude_sampled, t_interp):
        """Reconstruct the signal using zero-order hold (sample-and-hold) interpolation."""
        reconstructed_signal = np.zeros_like(t_interp)
        for i in range(len(t_sampled) - 1):
            mask = (t_interp >= t_sampled[i]) & (t_interp < t_sampled[i + 1])  # Hold the value until the next sample
            reconstructed_signal[mask] = amplitude_sampled[i]
        # Hold the last sample value for the remainder of the signal
        reconstructed_signal[t_interp >= t_sampled[-1]] = amplitude_sampled[-1]
        return reconstructed_signal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()
    sys.exit(app.exec_())
