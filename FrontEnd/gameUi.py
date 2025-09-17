from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout,
    QLabel, QProgressBar, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import sys

from main import MainUi


class ProgressModule(QWidget):
    def __init__(self, title, progress_percent):
        super().__init__()
        self.showFullScreen()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0c1521"))
        self.setPalette(palette)
        self.setStyleSheet("border: 1px solid #1a2a3a; border-radius: 8px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color:#4af8f4;")
        title_label.setFont(QFont("Sans Serif", 10))
        layout.addWidget(title_label)

        # Progress label row
        progress_row = QHBoxLayout()
        progress_row.setContentsMargins(0, 0, 0, 0)
        progress_row.setSpacing(0)

        progress_text = QLabel("Progress")
        progress_text.setStyleSheet("color: #017682; font-size: 9pt;")
        progress_row.addWidget(progress_text, alignment=Qt.AlignLeft)

        progress_percent_label = QLabel(f"{progress_percent}%")
        progress_percent_label.setStyleSheet("color: #14979a; font-size: 9pt;")
        progress_row.addWidget(progress_percent_label, alignment=Qt.AlignRight)

        layout.addLayout(progress_row)

        # Progress bar background container
        progress_bar_bg = QWidget()
        progress_bar_bg.setFixedHeight(8)
        progress_bar_bg.setStyleSheet("background-color:#80f7ef ; border-radius: 4px;")
        progress_bar_layout = QHBoxLayout(progress_bar_bg)
        progress_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Progress bar fill
        progress_bar_fill = QWidget()
        progress_bar_fill.setStyleSheet("background-color: #14979a; border-radius: 4px;")
        progress_bar_fill.setFixedWidth(int(progress_percent * 2.5))  # scale width for visibility
        progress_bar_layout.addWidget(progress_bar_fill)

        layout.addWidget(progress_bar_bg)

        # Play button
        play_button = QPushButton("▶ Play")
        play_button.setStyleSheet(
            "background-color: #80f7ef; color: black; font-weight: 600; border-radius: 6px; padding: 8px;"
        )
        layout.addWidget(play_button)
        # play_button.clicked.connect()

        self.setLayout(layout)


class SummaryModule(QWidget):
    def __init__(self, number_text, description):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0c1521"))
        self.setPalette(palette)
        self.setStyleSheet("border: 1px solid #1a2a3a; border-radius: 8px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(4)

        number_label = QLabel(number_text)
        number_label.setStyleSheet("color: #84fffe;")
        number_label.setFont(QFont("Sans Serif", 14, QFont.Bold))
        number_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(number_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #7a7a7a; font-size: 9pt;")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Modules")
        self.setStyleSheet("background-color: #0c1521;")
        self.resize(1024,480)
        self.setMaximumSize(1024, 480)


        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(16, 16, 16, 16)

        modules = [
            ("Basics Python", 62),
            ("C Language", 91),
            ("Cpp Language", 38),
            ("Mathematics", 85),
            ("Data Structure & Algorithm", 45),
            ("Dynamic Programming", 73),
        ]

        # Add progress modules (6)
        for i, (title, progress) in enumerate(modules):
            mod = ProgressModule(title, progress)
            row = i // 3
            col = i % 3
            grid.addWidget(mod, row, col)

        # Add summary modules (3)
        summary_data = [
            ("6", "Total Modules"),
            ("66%", "Average Progress"),
            ("2", "Completed"),
        ]
        for i, (num, desc) in enumerate(summary_data):
            summ = SummaryModule(num, desc)
            grid.addWidget(summ, 2, i)

        self.setLayout(grid)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

