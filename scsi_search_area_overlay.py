import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QRect, QPoint

class OverlayRectangle(QMainWindow):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x, y, width, height)

        # Variables for dragging and resizing
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge_threshold = 10  # Pixels near edges for resizing
        self.drag_start_position = QPoint()
        self.resize_start_rect = QRect()
        self.resize_direction = None

        # Minimum size for the rectangle (adjust as needed)
        self.min_width = 50
        self.min_height = 50

        # File to save the rectangle bounds
        self.bounds_file = "rectangle_bounds.json"
        self.load_bounds()  # Load saved bounds if available

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Set pen for the rectangle's border
        pen = QPen(Qt.GlobalColor.red, 3)
        painter.setPen(pen)
        
        # Set brush for the rectangle's interior (semi-transparent)
        brush = QBrush(QColor(255, 0, 0, 50))  # RGBA (Red, Green, Blue, Alpha)
        painter.setBrush(brush)
        
        # Draw the rectangle
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()

            # Check if the user clicked near the edges for resizing
            self.resize_direction = self.get_resize_direction(mouse_pos)
            if self.resize_direction:
                self.is_resizing = True
                self.resize_start_rect = self.geometry()
                self.drag_start_position = event.globalPosition().toPoint()
            else:
                # Otherwise, start dragging
                self.is_dragging = True
                self.drag_start_position = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            # Calculate resizing based on the direction
            self.handle_resize(event.globalPosition().toPoint())
        elif self.is_dragging:
            # Handle dragging
            new_position = event.globalPosition().toPoint() - self.drag_start_position
            self.move(new_position)
        else:
            # Update cursor to indicate resize edges
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.is_resizing = False
            self.resize_direction = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

            # Save the rectangle bounds when resizing is complete
            self.save_bounds()

    def get_resize_direction(self, mouse_pos):
        """Determine the resize direction based on mouse position."""
        rect = self.rect()
        resize_direction = None

        if mouse_pos.x() <= self.resize_edge_threshold:
            resize_direction = 'left'
        elif mouse_pos.x() >= rect.width() - self.resize_edge_threshold:
            resize_direction = 'right'

        if mouse_pos.y() <= self.resize_edge_threshold:
            resize_direction = 'top' if resize_direction is None else resize_direction + '_top'
        elif mouse_pos.y() >= rect.height() - self.resize_edge_threshold:
            resize_direction = 'bottom' if resize_direction is None else resize_direction + '_bottom'

        return resize_direction

    def handle_resize(self, global_mouse_pos):
        """Resize the rectangle based on the drag position."""
        delta = global_mouse_pos - self.drag_start_position
        new_rect = QRect(self.resize_start_rect)

        if 'left' in self.resize_direction:
            new_rect.setLeft(new_rect.left() + delta.x())
        if 'right' in self.resize_direction:
            new_rect.setRight(new_rect.right() + delta.x())
        if 'top' in self.resize_direction:
            new_rect.setTop(new_rect.top() + delta.y())
        if 'bottom' in self.resize_direction:
            new_rect.setBottom(new_rect.bottom() + delta.y())

        # Ensure the new width and height are not smaller than the minimum size
        if new_rect.width() < self.min_width:
            new_rect.setWidth(self.min_width)
        if new_rect.height() < self.min_height:
            new_rect.setHeight(self.min_height)

        # Apply the new geometry
        self.setGeometry(new_rect)

    def update_cursor(self, mouse_pos):
        """Update the mouse cursor to indicate resizing edges."""
        resize_direction = self.get_resize_direction(mouse_pos)

        if resize_direction is None:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif 'left' in resize_direction or 'right' in resize_direction:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif 'top' in resize_direction or 'bottom' in resize_direction:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif 'top_left' in resize_direction or 'bottom_right' in resize_direction:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif 'top_right' in resize_direction or 'bottom_left' in resize_direction:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)

    def save_bounds(self):
        """Save the rectangle bounds to a file."""
        rect = self.geometry()
        bounds_data = {
            "x": rect.x(),
            "y": rect.y(),
            "width": rect.width(),
            "height": rect.height()
        }
        with open(self.bounds_file, "w") as file:
            json.dump(bounds_data, file, indent=4)

    def load_bounds(self):
        """Load saved rectangle bounds from a file, if available."""
        try:
            with open(self.bounds_file, "r") as file:
                bounds_data = json.load(file)
                # Set the geometry based on saved bounds
                self.setGeometry(bounds_data["x"], bounds_data["y"], bounds_data["width"], bounds_data["height"])
        except FileNotFoundError:
            # If no saved bounds exist, don't adjust
            pass



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main window setup
        self.setWindowTitle("Draw Rectangle Example")
        self.setGeometry(100, 100, 400, 200)

        # Button to draw rectangle
        self.draw_button = QPushButton("Draw Rectangle")
        self.draw_button.clicked.connect(self.draw_rectangle)

        # Layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.draw_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def draw_rectangle(self):
        # Example coordinates and size (adjust as needed)
        x, y, width, height = 500, 300, 200, 100

        # Create the overlay rectangle
        self.overlay = OverlayRectangle(x, y, width, height)
        self.overlay.show()


if __name__ == "__main__":
    app = QApplication([])

    # Launch the main window
    window = MainWindow()
    window.show()

    app.exec()
