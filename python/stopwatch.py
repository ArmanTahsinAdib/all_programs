import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QWidget as QW,
)
from PyQt6.QtCore import QTime, QTimer, Qt


class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time = QTime(0, 0, 0, 0)
        self.time_label = QLabel("00:00:00:00", self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)
        self.record_button = QPushButton("Record", self)
        self.clear_all_button = QPushButton("Clear All", self)

        self.timer = QTimer(self)
        self.records = []

        # To display recorded times as a list
        self.records_display = QListWidget(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("StopWatch")
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)
        hbox.addWidget(self.record_button)
        hbox.addWidget(self.clear_all_button)
        vbox.addLayout(hbox)

        vbox.addWidget(self.records_display)  # Add the records display widget

        # Disable Stop, Reset, and Record buttons initially
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.record_button.setEnabled(False)

        self.setStyleSheet(
            """
            QPushButton, QLabel{
                padding: 20px;
                font-weight:bold;
            }
            QPushButton{
                font-size: 30px;
            }
            QLabel{
                font-size:80px;
                font-weight:bold;
                font-family:JetBrainsMono Nerd Font;
            }
            QListWidget{
                padding: 10px;
            }
        """
        )
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.record_button.clicked.connect(self.record)
        self.clear_all_button.clicked.connect(self.clear_all)
        self.timer.timeout.connect(self.update_display)

    def record(self):
        current_time = self.format_time(self.time)
        record_number = len(self.records) + 1  # Get the next record number
        self.records.append(current_time)
        # Display the recorded time
        self.add_record_to_display(record_number, current_time)

    def add_record_to_display(self, number, time):
        item_widget = QW()
        item_layout = QHBoxLayout()

        record_label = QLabel(f"{number}: {time}")
        # Smaller font size here
        record_label.setStyleSheet("font-size: 14px;")
        delete_button = QPushButton("Delete")
        # Smaller font for delete button
        delete_button.setStyleSheet("font-size: 12px;")
        delete_button.clicked.connect(
            lambda: self.delete_record(item_widget, time))

        item_layout.addWidget(record_label)
        item_layout.addWidget(delete_button)
        item_widget.setLayout(item_layout)

        list_item = QListWidgetItem(self.records_display)
        list_item.setSizeHint(item_widget.sizeHint())
        self.records_display.addItem(list_item)
        self.records_display.setItemWidget(list_item, item_widget)

    def delete_record(self, item_widget, time):
        index = self.records_display.row(
            self.records_display.itemWidget(item_widget))
        if index != -1:
            self.records_display.takeItem(index)  # Remove from display
            self.records.pop(index)  # Remove from internal records list
            self.update_record_numbers()  # Update record numbers after deletion

    def update_record_numbers(self):
        for i in range(self.records_display.count()):
            item_widget = self.records_display.itemWidget(
                self.records_display.item(i))
            record_label = item_widget.layout().itemAt(0).widget()  # Get the label
            # Update record number and time
            record_label.setText(f"{i + 1}: {self.records[i]}")

    def clear_all(self):
        self.records.clear()  # Clear the recorded times
        self.records_display.clear()  # Clear the display

    def start(self):
        self.timer.start(10)
        self.stop_button.setEnabled(True)
        self.record_button.setEnabled(True)
        self.reset_button.setEnabled(False)
        self.start_button.setEnabled(False)

    def stop(self):
        self.timer.stop()
        self.stop_button.setEnabled(False)
        self.record_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        self.start_button.setEnabled(True)

    def reset(self):
        self.time = QTime(0, 0, 0, 0)
        self.time_label.setText("00:00:00.00")
        self.records.clear()  # Clear the recorded times
        self.records_display.clear()  # Clear the display

        self.stop_button.setEnabled(False)
        self.record_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.reset_button.setEnabled(False)

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"

    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec())
