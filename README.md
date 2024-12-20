# Signal Reconstruction Application

An educational desktop application demonstrating signal sampling and recovery techniques. The app is designed to illustrate the importance of the Nyquist rate and validate the concepts of signal reconstruction using various interpolation methods. Ideal for learners and educators interested in digital signal processing.

---

## Features

### 1. **Signal Sampling & Reconstruction**
   - **Original Signal Display:** Visualize the original signal with sampling points marked.
   - **Reconstructed Signal:** View the reconstructed signal using selectable interpolation methods.
   - **Difference Graph:** Toggle between the difference plot and side-by-side comparison of original and reconstructed signals.
   - **Frequency Domain Analysis:** Inspect the frequency domain to detect aliasing.

### 2. **Signal Mixer/Composer**
   - Generate new signals by:
     - Selecting the number of terms (sinusoidal components).
     - Defining frequency, amplitude, and phase for each component.
   - Remove individual components to modify the signal dynamically.

### 3. **Customizable Sampling Frequency**
   - Adjust the sampling frequency using a slider.
   - Toggle between absolute frequency (Hz) and normalized frequency (% of \(f_{max}\)).
   - Quickly set valid sampling frequencies (\(f_s \geq 2f_{max}\)) with a dedicated button.

### 4. **Interpolation Methods**
   - Explore reconstruction techniques:
     - Shannon Interpolation
     - Lanczos Interpolation
     - Step Interpolation
   - Compare performance, pros, and cons of each method.

### 5. **Noise Control**
   - Add noise to the signal using an SNR slider.
   - Observe the impact of noise on the reconstructed signal and frequency domain.

### 6. **Real-time Updates**
   - Instantaneous updates to all plots when parameters are changed.

### 7. **Resizable UI**
   - Responsive and flexible user interface that adapts seamlessly to resizing.

---

## Usage Instructions

1. **Load or Compose a Signal:**
   - Use the "Composer" to create a new signal by specifying sinusoidal terms, frequencies, amplitudes, and phases.
   - Alternatively, load a signal from a file.

2. **Set Sampling Parameters:**
   - Adjust the sampling frequency using the slider or set a valid sampling frequency with the quick toggle button.
   - Toggle between Hz and normalized \(f_{max}\) display.

3. **Add Noise (Optional):**
   - Use the SNR slider to introduce noise and observe its effects.

4. **Reconstruct Signal:**
   - Choose an interpolation method from the dropdown menu.
   - Compare the reconstructed signal with the original using the difference graph.

5. **Analyze Results:**
   - Inspect the frequency domain for aliasing.
   - View differences between the original and reconstructed signals.

---

## Testing Scenarios

### 1. **2Hz + 6Hz Sinusoids**
   - Expected Behavior:
     - **12Hz Sampling:** Perfect reconstruction.
     - **4Hz Sampling:** Aliasing occurs, showing a single frequency.
     - **8Hz Sampling:** Partial reconstruction with visible artifacts.

### 2. **High-frequency Signal with Noise**
   - Mix of high-frequency components.
   - Add varying levels of noise to demonstrate reconstruction performance under noisy conditions.

### 3. **Multiple Frequencies with Small Gaps**
   - Demonstrates the limitations of reconstruction when frequencies are close to the Nyquist limit.

---

## Visuals

### Screenshots
- **Original and Reconstructed Signal**  
  ![Screenshot 1](https://github.com/user-attachments/assets/405f6756-7cfe-4b54-abe8-7c4276e5f837)

- **Frequency Domain Analysis**  
  ![Screenshot 2](https://github.com/user-attachments/assets/5e10d14a-a1cd-42ca-933f-b22684bef504)



### Video Demo
<video src="Uploading Signal Reconstructor Video.mp4…" controls="controls" style="max-width: 100%;"></video>



Uploading Signal Reconstructor Video.mp4…


---

## Team

This project wouldn’t have been possible without the hard work and collaboration of my amazing team. Huge shout-out to:

- [Nancy Mahmoud](https://github.com/nancymahmoud1)
- [Madonna Mosaad](https://github.com/madonna-mosaad)
- [Yassien Tawfik](https://github.com/YassienTawfikk)


Your support, ideas, and teamwork made this project a success. 🎉

---

## Educational Value
This application is tailored for educational purposes, providing a hands-on experience in understanding:
   - The Nyquist–Shannon sampling theorem.
   - Signal reconstruction techniques and their limitations.
   - The effects of noise and aliasing on signal processing.

---

## System Requirements
- **OS:** Windows/Linux/MacOS
- **Python Dependencies:** `numpy`, `matplotlib`, `scipy`, `PyQt5` (or any GUI library used).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/signal-reconstruction-app.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
---
## Contact

For any questions or suggestions, feel free to reach out:

- **Name**: Yassien Tawfik
- **Email**: Yassien.m.m.tawfik@gmail.com
