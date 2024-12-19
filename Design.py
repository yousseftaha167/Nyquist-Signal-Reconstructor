from PyQt5 import Qt, QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QComboBox, QSizePolicy, QSlider, QMenuBar, \
    QStatusBar, \
    QGroupBox, QPushButton, QGridLayout
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtCore import QRect, QSize, QCoreApplication, QMetaObject, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Initializes and sets up the main window layout and widgets.
        """
        # Main window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 820)
        MainWindow.setStyleSheet(u"background-color:black;")

        # Central widget to contain all layouts and controls
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Section: Plot Controls (Bottom panel for reconstruction, sampling, and SNR settings)
        self.plot_contrlos_layoutWidget = QWidget(self.centralwidget)
        self.plot_contrlos_layoutWidget.setObjectName(u"plot_contrlos_layoutWidget")
        self.plot_contrlos_layoutWidget.setGeometry(QRect(10, 720, 1265, 50))
        font = QFont()
        font.setFamily(u"Times New Roman")
        self.plot_contrlos_layoutWidget.setFont(font)

        # Horizontal layout for plot controls
        self.plot_contrlos_layout = QHBoxLayout(self.plot_contrlos_layoutWidget)
        self.plot_contrlos_layout.setObjectName(u"plot_contrlos_layout")
        self.plot_contrlos_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_plot_button = QPushButton()
        self.toggle_plot_button.setFont(font)
        self.toggle_plot_button.setMaximumSize(QSize(130, 30))
        self.toggle_plot_button.setGeometry(20, 720, 150, 30)  # Adjust position as needed
        self.toggle_plot_button.setStyleSheet("QPushButton {"
                                              "background-color: rgb(15, 15, 15);"
                                              "color:rgb(191, 191, 191);"
                                              "}"
                                              "QPushButton:hover{"
                                              "background-color: rgb(25, 25, 25);"
                                              "}")
        self.toggle_plot_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.plot_contrlos_layout.addWidget(self.toggle_plot_button)

        # Create the frequency layout container
        self.frequency_layout = QHBoxLayout()
        self.frequency_layout.setObjectName(u"frequency_layout")
        self.frequency_layout.setContentsMargins(0, 0, 0, 0)
        self.frequency_layout.setSpacing(15)

        # Frequency slider label
        self.frequency_slider_label = QLabel(self.plot_contrlos_layoutWidget)
        self.frequency_slider_label.setObjectName(u"frequency_slider_label")
        self.frequency_slider_label.setMaximumSize(QSize(130, 20))
        self.frequency_slider_label.setFont(font)
        self.frequency_slider_label.setStyleSheet(u"color:rgb(191, 191, 191);")
        self.frequency_slider_label.setAlignment(Qt.AlignCenter)
        self.frequency_slider_label.setText("Sampling Frequency")  # Set text directly here
        self.frequency_layout.addWidget(self.frequency_slider_label)

        # Reconstruction method dropdown
        self.reconstruction_method = QComboBox(self.plot_contrlos_layoutWidget)
        self.reconstruction_method.setObjectName(u"reconstruction_method")
        self.reconstruction_method.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.reconstruction_method.sizePolicy().hasHeightForWidth())
        self.reconstruction_method.setSizePolicy(sizePolicy)
        self.reconstruction_method.setMaximumSize(QSize(150, 30))
        self.reconstruction_method.setFont(font)
        self.reconstruction_method.setCursor(QCursor(Qt.PointingHandCursor))
        self.reconstruction_method.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                                 "color: rgb(255, 255, 255);")
        self.reconstruction_method.setEditable(False)

        # Add combo box to layout
        self.frequency_layout.addWidget(self.reconstruction_method)

        # Sampling frequency slider
        self.sampling_frequency = QSlider(self.plot_contrlos_layoutWidget)
        self.sampling_frequency.setObjectName(u"sampling_frequency")
        self.sampling_frequency.setMaximumSize(QSize(250, 60))
        self.sampling_frequency.setFont(font)
        self.sampling_frequency.setCursor(QCursor(Qt.PointingHandCursor))
        self.sampling_frequency.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                              "color: rgb(255, 255, 255);")
        self.sampling_frequency.setOrientation(Qt.Horizontal)
        self.frequency_layout.addWidget(self.sampling_frequency)

        # Add a label/button to display the current frequency
        self.frequency_value_label_button = QPushButton()
        self.frequency_value_label_button.setFont(font)
        self.frequency_value_label_button.setMaximumSize(QSize(60, 30))
        self.frequency_value_label_button.setStyleSheet("QPushButton {"
                                                        "background-color: rgb(15, 15, 15);"
                                                        "color:rgb(191, 191, 191);"
                                                        "}"
                                                        "QPushButton:hover{"
                                                        "background-color: rgb(25, 25, 25);"
                                                        "}")
        self.frequency_value_label_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.frequency_value_label_button.setText(f"{self.sampling_frequency.value()} Hz")
        self.frequency_layout.addWidget(self.frequency_value_label_button)

        self.set_min_valid_frequency = QPushButton()
        self.set_min_valid_frequency.setFont(font)
        self.set_min_valid_frequency.setMaximumSize(QSize(130, 30))
        self.set_min_valid_frequency.setGeometry(20, 720, 150, 30)  # Adjust position as needed
        self.set_min_valid_frequency.setStyleSheet("QPushButton {"
                                                   "background-color: rgb(15, 15, 15);"
                                                   "color:rgb(191, 191, 191);"
                                                   "}"
                                                   "QPushButton:hover{"
                                                   "background-color: rgb(25, 25, 25);"
                                                   "}")
        self.set_min_valid_frequency.setCursor(QCursor(Qt.PointingHandCursor))
        self.set_min_valid_frequency.setText("Valid Freq Sampling")
        self.frequency_layout.addWidget(self.set_min_valid_frequency)

        # Add the frequency layout to the main controls layout
        self.plot_contrlos_layout.addLayout(self.frequency_layout)

        # Create the frequency layout container for SNR
        self.SNR_layout = QHBoxLayout()
        self.SNR_layout.setObjectName(u"SNR_layout")
        self.SNR_layout.setContentsMargins(0, 0, 0, 0)

        # Frequency slider label
        self.SNR_slider_label = QLabel(self.plot_contrlos_layoutWidget)
        self.SNR_slider_label.setObjectName(u"SNR_slider_label")
        self.SNR_slider_label.setMaximumSize(QSize(40, 20))
        self.SNR_slider_label.setFont(font)
        self.SNR_slider_label.setStyleSheet(u"color:rgb(191, 191, 191);")
        self.SNR_slider_label.setAlignment(Qt.AlignCenter)
        self.SNR_slider_label.setText("SNR")
        self.SNR_layout.addWidget(self.SNR_slider_label)

        # SNR level slider
        self.SNR_level = QSlider(self.plot_contrlos_layoutWidget)
        self.SNR_level.setObjectName(u"SNR_level")
        self.SNR_level.setMaximumSize(QSize(200, 30))
        self.SNR_level.setFont(font)
        self.SNR_level.setRange(0, 50)  # Slider range from 0 dB to 50 dB
        self.SNR_level.setValue(50)
        self.SNR_level.setCursor(QCursor(Qt.PointingHandCursor))
        self.SNR_level.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                     "color: rgb(255, 255, 255);")
        self.SNR_level.setOrientation(Qt.Horizontal)
        self.SNR_layout.addWidget(self.SNR_level)

        # Add a QLabel to display the SNR value as a percentage
        self.SNR_value_label = QLabel(self.plot_contrlos_layoutWidget)
        self.SNR_value_label.setObjectName(u"SNR_value_label")
        self.SNR_value_label.setMaximumSize(QSize(50, 30))
        self.SNR_value_label.setFont(font)
        self.SNR_value_label.setStyleSheet(u"color:rgb(191, 191, 191);")
        self.SNR_value_label.setAlignment(Qt.AlignCenter)
        self.SNR_level.setRange(0, 100)  # Change to represent 0% to 100%
        self.SNR_level.setValue(100)  # Set initial value to maximum (100%)
        self.SNR_value_label.setText(f"{self.SNR_level.value()}%")  # Set initial text
        self.SNR_layout.addWidget(self.SNR_value_label)

        self.plot_contrlos_layout.addLayout(self.SNR_layout)

        # Title Section (Top-left with icon and title)
        self.title_container = QWidget(self.centralwidget)
        self.title_container.setObjectName(u"title_container")
        self.title_container.setGeometry(QRect(0, 0, 391, 62))
        self.title_container.setFont(font)

        # Title layout with icon and text
        self.title_layout = QHBoxLayout(self.title_container)
        self.title_layout.setObjectName(u"title_layout")
        self.title_layout.setContentsMargins(0, 0, 0, 0)

        # Icon for the title
        self.title_icon = QLabel(self.title_container)
        self.title_icon.setObjectName(u"title_icon")
        self.title_icon.setMaximumSize(QSize(60, 60))
        self.title_icon.setFont(font)
        self.title_icon.setPixmap(QPixmap(u"src/icons8-graph-100.png"))
        self.title_icon.setScaledContents(True)
        self.title_layout.addWidget(self.title_icon)

        # Title text label
        self.title = QLabel(self.title_container)
        self.title.setObjectName(u"label")
        self.title.setMaximumSize(QSize(220, 40))
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        font1.setPointSize(22)
        self.title.setFont(font1)
        self.title.setStyleSheet(u"color:rgb(191, 191, 191);")
        self.title.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title)

        # Main Buttons (Top-right: Upload Signal, Composer and Quit buttons)
        self.main_buttons_container = QWidget(self.centralwidget)
        self.main_buttons_container.setObjectName(u"main_buttons_container")
        self.main_buttons_container.setGeometry(QRect(720, 5, 561, 51))
        self.main_buttons_container.setFont(font)

        # Button layout
        self.main_buttons_layout = QHBoxLayout(self.main_buttons_container)
        self.main_buttons_layout.setObjectName(u"main_buttons_layout")
        self.main_buttons_layout.setContentsMargins(0, 0, 15, 0)
        self.main_buttons_layout.setSpacing(30)

        # Upload Signal button
        self.upload_signal = QPushButton(self.main_buttons_container)
        self.upload_signal.setObjectName(u"upload_signal")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.upload_signal.setSizePolicy(sizePolicy1)
        self.upload_signal.setMaximumSize(QSize(200, 40))
        self.upload_signal.setFont(font)
        self.upload_signal.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_signal.setStyleSheet(u"QPushButton { border: none; padding: 10px; color: rgb(255, 255, 255); "
                                         u"background-color: rgb(15,15,15); border-bottom: 2px solid transparent; } "
                                         u"QPushButton:hover { border-bottom-color:rgb(125, 142, 255); "
                                         u"color:rgb(125, 142, 255); }")
        self.main_buttons_layout.addWidget(self.upload_signal)

        # Signal Composer button
        self.signal_composer = QPushButton(self.main_buttons_container)
        self.signal_composer.setObjectName(u"signal_composer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.signal_composer.setSizePolicy(sizePolicy1)
        self.signal_composer.setMaximumSize(QSize(200, 40))
        self.signal_composer.setFont(font)
        self.signal_composer.setCursor(QCursor(Qt.PointingHandCursor))
        self.signal_composer.setStyleSheet(u"QPushButton { border: none; padding: 10px; color: rgb(255, 255, 255); "
                                           u"background-color: rgb(15,15,15); border-bottom: 2px solid transparent; } "
                                           u"QPushButton:hover { border-bottom-color:rgb(183, 255, 171); "
                                           u"color:rgb(183, 255, 171); }")
        self.main_buttons_layout.addWidget(self.signal_composer)

        # Quit Application button
        self.quit_app = QPushButton(self.main_buttons_container)
        self.quit_app.setObjectName(u"quit_app")
        self.quit_app.setSizePolicy(sizePolicy1)
        self.quit_app.setMaximumSize(QSize(200, 40))
        self.quit_app.setFont(font)
        self.quit_app.setCursor(QCursor(Qt.PointingHandCursor))
        self.quit_app.setStyleSheet(u"QPushButton { border: none; padding: 10px; color: rgb(255, 255, 255); "
                                    u"background-color: rgb(15,15,15); border-bottom: 2px solid transparent; } "
                                    u"QPushButton:hover { border-bottom-color:rgb(179, 15, 66); color:rgb(179, 15, 66); }")
        self.quit_app.clicked.connect(QtWidgets.QApplication.quit)
        self.main_buttons_layout.addWidget(self.quit_app)

        # Plot Display Area (Center grid for displaying signals in 4 sections)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 69, 1261, 641))
        self.gridLayoutWidget.setFont(font)

        # Grid layout to hold 4 group boxes for signal plots
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # Group box 1: Original Signal
        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"")
        self.og_signal_label = QLabel(self.groupBox)
        self.og_signal_label.setObjectName(u"og_signal_label")
        self.og_signal_label.setGeometry(QRect(6, 6, 615, 20))
        self.og_signal_label.setFont(font)
        self.og_signal_label.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                           u"color:rgb(191, 191, 191);")
        self.og_signal_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        # Group box 2: Reconstructed Signal
        self.groupBox_2 = QGroupBox(self.gridLayoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet(u"")
        self.rc_signal_label = QLabel(self.groupBox_2)
        self.rc_signal_label.setObjectName(u"rc_signal_label")
        self.rc_signal_label.setGeometry(QRect(6, 6, 615, 20))
        self.rc_signal_label.setFont(font)
        self.rc_signal_label.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                           u"color:rgb(191, 191, 191);")
        self.rc_signal_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        # Group box 3: Difference Plot
        self.groupBox_3 = QGroupBox(self.gridLayoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet(u"")
        self.diff_plot_label = QLabel(self.groupBox_3)
        self.diff_plot_label.setObjectName(u"diff_plot_label")
        self.diff_plot_label.setGeometry(QRect(6, 6, 615, 20))
        self.diff_plot_label.setFont(font)
        self.diff_plot_label.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                           u"color:rgb(191, 191, 191);")
        self.diff_plot_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)

        # Group box 4: Frequency Domain Plot
        self.groupBox_4 = QGroupBox(self.gridLayoutWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet(u"")
        self.freq_plot_label = QLabel(self.groupBox_4)
        self.freq_plot_label.setObjectName(u"freq_plot_label")
        self.freq_plot_label.setGeometry(QRect(6, 6, 615, 20))
        self.freq_plot_label.setFont(font)
        self.freq_plot_label.setStyleSheet(u"background-color: rgb(15, 15, 15);\n"
                                           u"color:rgb(191, 191, 191);")
        self.freq_plot_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)

        # Set central widget and status/menu bars
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Set text and placeholder text for UI components
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Sets the display text for various UI components.
        """
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.reconstruction_method.setCurrentText("")
        self.reconstruction_method.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Interpolation Method", None))
        self.title_icon.setText("")
        self.title.setText(QCoreApplication.translate("MainWindow", u"Signal Reconstruction", None))
        self.upload_signal.setText(QCoreApplication.translate("MainWindow", u"Upload Signal", None))
        self.signal_composer.setText(QCoreApplication.translate("MainWindow", u"Composer", None))
        self.quit_app.setText(QCoreApplication.translate("MainWindow", u"Quit Application", None))
        self.groupBox.setTitle("")
        self.og_signal_label.setText(QCoreApplication.translate("MainWindow", u"Original Signal", None))
        self.groupBox_2.setTitle("")
        self.rc_signal_label.setText(QCoreApplication.translate("MainWindow", u"Difference Plot", None))
        self.groupBox_3.setTitle("")
        self.diff_plot_label.setText(QCoreApplication.translate("MainWindow", u"Reconstructed Signal", None))
        self.groupBox_4.setTitle("")
        self.freq_plot_label.setText(QCoreApplication.translate("MainWindow", u"Frequency Domain Plot", None))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
