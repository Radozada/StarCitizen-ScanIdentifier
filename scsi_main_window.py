import sys
import json
import ctypes
from PyQt6.QtWidgets import QApplication, QRadioButton, QLabel, QVBoxLayout, QPushButton, QWidget, QListWidget, QHBoxLayout, QLineEdit, QGroupBox, QGridLayout, QListWidgetItem
from PyQt6.QtGui import QMovie, QIcon, QFont, QPixmap, QFontMetrics
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from scsi_ocr_scanner import capture_screen, process_image
from scsi_utils import get_region_size, load_rectangle_bounds, clean_input_text, find_matching_headers, results_to_widget, get_widget_item, assign_icon

from scsi_search_area_overlay import OverlayRectangle

HISTORY_FILE = "data/scan_history.json"
DATABASE_FILE = "data/scsi_database.db"
GROUND_MINERALS_TABLE_NAME = "GROUND_MINERALS"
ASTEROIDS_TABLE_NAME = "ASTEROID_TYPES"
SCREENSHOT_PATH = "data/screenshot.png"
WINDOW_ICON = "resources/scsi_tool.ico"
SCAN_AREA_ACTIVE_ICON = "resources/area_settings_active_icon_128.png"
SCAN_AREA_ICON = "resources/area_settings_icon_128.png"

class ScanWorker(QThread):
    # Define custom signals for passing results back to the UI
    scan_finished = pyqtSignal(str, list)

    def __init__(self, region, screenshot_path, input_textbox,
                 scanner_used, options_radio_button_ground_mining):
        super().__init__()
        self.region = region
        self.screenshot_path = screenshot_path
        self.input_textbox = input_textbox
        self.scanner_used = scanner_used
        self.options_radio_button_ground_mining = options_radio_button_ground_mining        
        
         # Load the rectangle bounds from the saved file
        self.region = load_rectangle_bounds()
        if not self.region:
            # Fallback to a default region if no saved bounds exist
            self.region = (0, 0, 800, 600)

    def run(self):
        if self.scanner_used:
            captured_path = capture_screen(self.region, self.screenshot_path)
            scanned_text = process_image(captured_path)
        else:
            scanned_text = self.input_textbox.text()

        #Clean text from anything but numbers 
        scanned_text = clean_input_text(scanned_text)

        #SET THE TABLE TO USE BASED ON A TOGGLE ON THE UI        
        if self.options_radio_button_ground_mining.isChecked():
            TABLE_NAME = GROUND_MINERALS_TABLE_NAME
        else:
            TABLE_NAME = ASTEROIDS_TABLE_NAME
       
        matches = find_matching_headers( DATABASE_FILE, TABLE_NAME, scanned_text)  

        # Emit the results when finished
        self.scan_finished.emit(scanned_text, matches)

class ScanWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Screen region settings
        self.region = get_region_size()  # Adjust the region size
        self.screenshot_path = SCREENSHOT_PATH

        # History
        self.history = []

        # Worker thread
        self.worker = None

        # Rectangle overlay instance (initially None)
        self.overlay_rectangle = None

        # Initialize the window
        self.init_ui()
        self.load_history()
        self.update_status_image("fred")
        self.history_list.scrollToBottom()

    def init_ui(self):
        # Set up the window
        self.setWindowTitle("SC Scan ID")
        self.setWindowIcon(QIcon(WINDOW_ICON))
        self.setGeometry(100, 100, 800, 500)  # Window size
        self.setFixedSize(800, 500)  # Fixed size window

        #Dark Top Window Bar
        hwnd = int(self.winId())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int)
        )

        # Style Sheet for all the Group Boxes
        #group_box_style_sheet = "QGroupBox { font-size: 14px; color: #74006a; }"

        # Center the window
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        #Used for determining status image changes
        self.scanner_used = False              

        # OPTIONS SECTION
        options_groupbox = QGroupBox("Options", self)
        options_groupbox.setStyleSheet("QGroupBox {font-size: 14px;}")
        options_layout = QVBoxLayout()
        
        self.options_radio_button_ground_mining = QRadioButton("Ground Mining")
        self.options_radio_button_ground_mining.setChecked(True)
        self.options_radio_button_asteroid_mining = QRadioButton("Asteroid Mining")

        self.options_radio_button_asteroid_mining.clicked.connect(self.update_results_key)
        self.options_radio_button_ground_mining.clicked.connect(self.update_results_key)

        options_layout.addWidget(self.options_radio_button_ground_mining)
        options_layout.addWidget(self.options_radio_button_asteroid_mining)
        options_groupbox.setLayout(options_layout)

        # INPUT SECTION
        input_groupbox = QGroupBox("Search", self)
        input_groupbox.setStyleSheet("QGroupBox {font-size: 14px; }")
        input_layout = QVBoxLayout()

        # Input Text Box Label
        input_title_label = QLabel("Radar Signature", self)
        input_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_title_label.setStyleSheet("font-size: 16px; padding: 10px;")
        
        # Input Text Box
        self.input_textbox = QLineEdit(self)
        self.input_textbox.setPlaceholderText("Example: 7200")
        self.input_textbox.setStyleSheet("font-size: 16px; padding: 10px;")
        self.input_textbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input_textbox.returnPressed.connect(self.start_search)
        self.input_textbox.textChanged.connect(self.on_text_changed)

        # Input Search Button
        self.input_search_button = QPushButton("Search", self)
        self.input_search_button.setToolTip("Searches database for search box entry.")
        self.input_search_button.clicked.connect(self.start_search)
        self.input_search_button.setEnabled(False)

        # Input Section Layout        
        input_section_layout = QHBoxLayout()
        input_section_layout.addWidget(input_title_label)
        input_section_layout.addWidget(self.input_textbox)

        input_layout.addLayout(input_section_layout)
        input_layout.addWidget(self.input_search_button)
        input_groupbox.setLayout(input_layout)

        # SCAN SECTION
        scan_groupbox = QGroupBox("Scan Area of Screen", self)
        scan_groupbox.setStyleSheet("QGroupBox { font-size: 14px; }")
        scan_section_layout = QVBoxLayout()       

        self.toggle_scan_area_button = QPushButton("", self)
        self.toggle_scan_area_button.setFixedWidth(25)
        self.toggle_scan_area_button.setStyleSheet("QPushButton { background-color: transparent; border: none;}")
        self.toggle_scan_area_button.setIcon(QIcon("resources/area_settings_icon_128.png"))
        self.toggle_scan_area_button.setToolTip("Move, or resize scan area.")
        self.toggle_scan_area_button.setCheckable(True)
        self.toggle_scan_area_button.clicked.connect(self.toggle_scan_area)

        toggle_scan_area_button_wrapper = QHBoxLayout()
        toggle_scan_area_button_wrapper.setAlignment(Qt.AlignmentFlag.AlignRight)
        toggle_scan_area_button_wrapper.addWidget(self.toggle_scan_area_button)

        self.scan_button = QPushButton("Scan Screen", self)
        self.scan_button.setToolTip("Searches database with number found in a defined area of the screen.")
        #self.scan_button.setShortcut(tr())  #TODO
        self.scan_button.clicked.connect(self.start_scan)        
        
        self.status_image_wrapper = QVBoxLayout() #Need it so the image is centered
        self.status_image_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_image_label = QLabel(self)
        self.status_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_image_label.setFixedSize(200, 200)  # Set fixed size for the image
        self.status_image_wrapper.addWidget(self.status_image_label)

        scan_section_layout.addLayout(toggle_scan_area_button_wrapper)
        scan_section_layout.addLayout(self.status_image_wrapper)
        scan_section_layout.addWidget(self.scan_button)
        scan_groupbox.setLayout(scan_section_layout)          

        # RESULT SECTION
        result_groupbox = QGroupBox("Results", self)
        result_groupbox.setStyleSheet("QGroupBox { font-size: 14px; }")
        self.result_layout = QVBoxLayout()
        
        self.results_widget = QLabel("Ready to go")
        self.results_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setup_asteroid_results_view()
        self.setup_ground_results_view()
        self.result_layout.addWidget(self.results_widget)
        result_groupbox.setLayout(self.result_layout)

        # HISTORY SECTION
        history_groupbox = QGroupBox("History", self)
        history_groupbox.setMaximumWidth(400)
        history_groupbox.setMinimumWidth(400)
        history_groupbox.setStyleSheet("QGroupBox { font-size: 14px; }")
        history_layout = QVBoxLayout()
        
        # History Label
        history_label = QLabel("")
        history_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # History Clear Button 
        history_clear_button = QPushButton("Clear History", self)
        history_clear_button.clicked.connect(self.clear_history)

        #History Label and Scan Area Button Layout
        history_top_section_layout = QHBoxLayout()
        history_top_section_layout.addWidget(history_label)
        history_top_section_layout.addWidget(history_clear_button)

        # History List
        self.history_list = QListWidget(self)
        self.history_list.setFont(QFont("Arial Narrow",9))
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setWordWrap(True)
        self.history_list.setMaximumWidth(400)

        history_layout.addLayout(history_top_section_layout)
        history_layout.addWidget(self.history_list)
        history_groupbox.setLayout(history_layout)

        # Grid Layout
        grid_layout = QGridLayout() 

        # Add all sections to the grid layout
        grid_layout.addWidget(options_groupbox,  0, 0, 1, 1)
        grid_layout.addWidget(input_groupbox,    1, 0, 1, 1)
        grid_layout.addWidget(scan_groupbox,     2, 0, 1, 1)
        grid_layout.addWidget(result_groupbox,   0, 1, 2, 1)
        grid_layout.addWidget(history_groupbox,  2, 1, 1, 1)        

        self.setLayout(grid_layout)

    def on_text_changed(self, text):
        '''Turns off the Search Button when there is no text in the search box'''
        if text:
            self.input_search_button.setEnabled(True)
        else:
            self.input_search_button.setEnabled(False)

    def start_search(self):
        if self.input_search_button.isEnabled() == True:
            self.input_search_button.setEnabled(False)
            self.input_search_button.setText("Searching...") 
            self.scan_button.setEnabled(False)
            self.scanner_used = False        
        else:
            return

        #starts cleaning when the scanner isn't being used
        self.update_status_image("fred")
        
        self.start_scan_worker()

    def toggle_scan_area(self):
        if self.overlay_rectangle is None:
            # Define the rectangle position and size
            region = get_region_size()
            loc_x, loc_y, width, height = region[0],region[1],region[2],region[3] 
            
            # Create and show the rectangle
            self.overlay_rectangle = OverlayRectangle( loc_x, loc_y, width, height )
            self.overlay_rectangle.show()
            self.toggle_scan_area_button.setIcon(QIcon(SCAN_AREA_ACTIVE_ICON))
        else:
             # If the rectangle already exists, toggle it off
            self.overlay_rectangle.close()
            self.overlay_rectangle = None            
            self.toggle_scan_area_button.setIcon(QIcon(SCAN_AREA_ICON))

    def start_scan(self):
        # Disable the scan buttons during the scan
        self.scan_button.setText("Scanning...") 
        self.scan_button.setEnabled(False)
        self.input_search_button.setEnabled(False)
        self.update_status_image("scanning")        
        self.scanner_used = True

        self.start_scan_worker()

    def start_scan_worker(self):
        # Create and start the worker thread
        self.worker = ScanWorker(self.region, self.screenshot_path, self.input_textbox,
                                 self.scanner_used, self.options_radio_button_ground_mining)
        self.worker.scan_finished.connect(self.handle_scan_finished)
        self.worker.finished.connect(self.cleanup_worker)  # Clean up when the thread finishes
        self.worker.start()

    def handle_scan_finished(self, scanned_text, matches):
        # Display results
        results = results_to_widget(scanned_text, matches)
        self.update_results(results)

        # Add to history
        self.add_to_history(results)

        if self.scanner_used:
            # Update the status to "ready" only when the scanner was used
            self.update_status_image("ready")

        # Reenable the input box only if there is text inside
        if self.input_textbox.text():
            self.input_search_button.setEnabled(True)
            self.input_search_button.setText("Search")

        # Re-enable the scan button
        self.scan_button.setEnabled(True)
        self.scan_button.setText("Scan Screen")

    def cleanup_worker(self):
        """Clean up the worker thread after it finishes."""
        if self.worker:
            self.worker.quit()  # Signal the thread to stop
            self.worker.wait()  # Wait for it to finish
            self.worker = None  # Clear the reference to the thread

    def add_to_history(self, results):       
        # Create entry
        entry = {
            "time": results["time"],
            "scanned_text": results["scanned_text"],
            "matches": results["matches"],
        }

        # Update history
        self.history.append(entry)

        # Need to create a QListWidgetItem before making it into a custom results widget
        list_widget_item = QListWidgetItem()
        list_widget_item.setSizeHint(results["widget_item"].sizeHint())
        self.history_list.addItem(list_widget_item)
        self.history_list.setItemWidget(list_widget_item, results["widget_item"])
        self.history_list.scrollToBottom()

        # Save history to file
        self.save_history()

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r") as file:
                self.history = json.load(file)
                for entry in self.history:
                    time = entry["time"]
                    scanned_text = entry["scanned_text"]
                    matches = entry["matches"]

                    # Need to create a QListWidgetItem before making it into a custom results widget
                    list_widget_item = QListWidgetItem()
                    results_widget = get_widget_item(time, scanned_text, matches)
                    list_widget_item.setSizeHint(results_widget.sizeHint())
                    self.history_list.addItem(list_widget_item)
                    self.history_list.setItemWidget(list_widget_item, results_widget)
        except FileNotFoundError:
            # No history file exists yet
            self.history = []
            with open(HISTORY_FILE, "w") as file:
                json.dump(self.history, file)

    def save_history(self):
        with open(HISTORY_FILE, "w") as file:
            json.dump(self.history, file, indent=4)

    def clear_history(self):
        self.history = []
        with open(HISTORY_FILE, "w") as file:
                json.dump(self.history, file)

        self.history_list.clear()

    def update_status_image(self, state):
        """
        Update the status image based on the current state.
        :param state: "fred", "ready", "scanning"
        """
        gif_paths = {
            "fred": "resources/fred-fred-mopping_200.gif",
            "ready": "resources/ready_to_scan_200.gif",
            "scanning": "resources/scanning_200.gif",
        }

        if state in gif_paths:
            gif_path = gif_paths[state]
            movie = QMovie(gif_path)
            self.status_image_label.setMovie(movie)
            movie.start()
    
    def setup_ground_results_view(self):
        # Gems Key Label
        gems_label_text = "Gems means any of them."
        self.gems_label = QLabel(gems_label_text)
        self.gems_label.setToolTip("Gems share their Radio Signature.")
        self.gems_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gems_label.setFixedWidth(QFontMetrics(self.gems_label.font()).horizontalAdvance(gems_label_text) + 15)
        self.gems_label.setWordWrap(True)
        self.gems_label.setStyleSheet("color: #3ec500; font-weight: Bold; font-style:italic ;")
        
        # Icons Labels
        aph_icon_path = assign_icon("Aphorite")
        self.aph_icon_label = QLabel()
        self.aph_icon_label.setToolTip("Aphorite")
        self.aph_icon_label.setFixedWidth(24)
        self.aph_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aph_icon_label.setPixmap(QPixmap(aph_icon_path).scaled(16, 16))  # Adjust size as needed
        dol_icon_path = assign_icon("Dolivine")
        self.dol_icon_label = QLabel()
        self.dol_icon_label.setToolTip("Dolivine")
        self.dol_icon_label.setFixedWidth(24)
        self.dol_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dol_icon_label.setPixmap(QPixmap(dol_icon_path).scaled(16, 16))  # Adjust size as needed
        had_icon_path = assign_icon("Hadanite")
        self.had_icon_label = QLabel()
        self.had_icon_label.setToolTip("Hadanite")
        self.had_icon_label.setFixedWidth(24)
        self.had_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.had_icon_label.setPixmap(QPixmap(had_icon_path).scaled(16, 16))  # Adjust size as needed
        jal_icon_path = assign_icon("Janalite")
        self.jal_icon_label = QLabel()
        self.jal_icon_label.setToolTip("Janalite")
        self.jal_icon_label.setFixedWidth(24)
        self.jal_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.jal_icon_label.setPixmap(QPixmap(jal_icon_path).scaled(16, 16))  # Adjust size as needed
        
        self.gems_h_layout_1 = QHBoxLayout()
        self.gems_h_layout_1.addWidget(self.aph_icon_label)
        self.gems_h_layout_1.addWidget(self.dol_icon_label)
        self.gems_h_layout_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.gems_h_layout_2 = QHBoxLayout()
        self.gems_h_layout_2.addWidget(self.had_icon_label)
        self.gems_h_layout_2.addWidget(self.jal_icon_label)
        self.gems_h_layout_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.gems_v_layout = QVBoxLayout()
        self.gems_v_layout.addLayout(self.gems_h_layout_1)
        self.gems_v_layout.addLayout(self.gems_h_layout_2)
        self.gems_v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ground_results_key_layout = QHBoxLayout()
        self.ground_results_key_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ground_results_key_layout.setContentsMargins(1, 1, 1, 1)
        self.ground_results_key_layout.setSpacing(1)#for debugging set to 1
        self.ground_results_key_layout.addWidget(self.gems_label)
        self.ground_results_key_layout.addLayout(self.gems_v_layout)
        
        # Groupbox
        self.ground_results_key_groupbox = QGroupBox("", self)
        self.ground_results_key_groupbox.setStyleSheet("QGroupBox { font-size: 14px; }")
        self.ground_results_key_groupbox.setLayout(self.ground_results_key_layout)

        self.result_layout.addWidget(self.ground_results_key_groupbox)

    def setup_asteroid_results_view(self):        
        print("Setup Asteroid Results")

    def update_results_key(self):
        if self.options_radio_button_ground_mining.isChecked():
            self.ground_results_key_groupbox.show()
        elif self.options_radio_button_asteroid_mining.isChecked():
            self.ground_results_key_groupbox.hide()
        
    def update_results(self, results):
        if self.results_widget:      
            self.results_widget.deleteLater()
            self.results_widget = None
        self.results_widget = get_widget_item(results["time"], results["scanned_text"], results["matches"])
        self.result_layout.addWidget(self.results_widget)

import qdarkstyle

# Main entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))

    window = ScanWindow()
    window.show()
    sys.exit(app.exec())