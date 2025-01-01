from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

def show_popup(title_text, message_text):
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle( "Star Citizen Scan Identifier" )
    window.setGeometry( 100, 100, 350, 150 )
    window.setFixedSize( 350, 150 )
    window.setWindowFlags( Qt.WindowType.WindowStaysOnTopHint )
    
    screen = app.primaryScreen().geometry()
    window_width = 350
    window_height = 150
    x = (screen.width() - window_width) // 2
    y = (screen.height() - window_height) // 2
    window.move(x, y)

    #python exe packager will handle this
    #window.setWindowIcon(QIcon("C:/Users/Administrator/Documents/_Python/mining_text_icon_217240.ico"))

    title_label = QLabel(title_text, window)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setStyleSheet("font-size: 14px; padding: 0px;")

    message_label = QLabel(message_text, window)
    message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    message_label.setStyleSheet("font-size: 21px; padding: 0px;")

    dismiss_button = QPushButton("Dismiss", window)
    dismiss_button.clicked.connect(window.close)

    layout = QVBoxLayout()
    layout.addWidget(title_label)
    layout.addWidget(message_label)
    layout.addWidget(dismiss_button)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())