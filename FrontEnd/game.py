from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout,
    QLabel, QProgressBar, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtGui import QGuiApplication as qgi
import sys
from fetch import fetchQuestions  # Fixed typo in function name
from main import MainUi
import os
import json

class ProgressModule(QWidget):
    playClicked = pyqtSignal(str)  # Signal to emit category when play is clicked

    def __init__(self, title, progress_percent, total_problems, solved_problems):
        super().__init__()
        self.category = title
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

        # Progress stats
        stats_label = QLabel(f"{solved_problems}/{total_problems} solved")
        stats_label.setStyleSheet("color: #017682; font-size: 9pt;")
        layout.addWidget(stats_label)

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
        play_button.clicked.connect(self.onPlayClicked)
        layout.addWidget(play_button)

        self.setLayout(layout)

    def onPlayClicked(self):
        self.playClicked.emit(self.category)

class SummaryModule(QWidget):
    def __init__(self, number_text, description):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0c1521"))
        self.setPalette(palette)
        self.setStyleSheet("""
            border: 1px solid #54bfcb;
             border-radius: 8px;
        """)

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

class ProblemListDialog(QWidget):
    problemSelected = pyqtSignal(dict)  # Signal to emit selected problem

    def __init__(self, category, problems):
        super().__init__()
        self.setWindowTitle(f"Problems - {category}")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #0c1521; color: #4af8f4;")

        layout = QVBoxLayout()

        self.mainui = MainUi()

        title = QLabel(f"Select a problem from {category}")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        # print("problems: \n",problems)
        for problem in problems:
            # print("normal problem: \n",problem)
            # exit()
            btn = QPushButton(problem['title'])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a2a3a;
                    color: #4af8f4;
                    border: 1px solid #4af8f4;
                    padding: 10px;
                    text-align: left;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2a3a4a;
                }
            """)

            btn.clicked.connect(lambda checked, p=problem: self.onProblemSelected(p))
            scroll_layout.addWidget(btn)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def onProblemSelected(self, problem):
        self.problemSelected.emit(problem)
        self.close()
        self.mainui.question_widget.setText(problem['question'])
        self.mainui.testcase_widget.setText(problem['testcase'])
        self.mainui.output_widget.setText(problem['answer'])
        self.mainui.show()

class MainWindow(QWidget):
    problemSelected = pyqtSignal(dict)  # Signal to emit selected problem to main UI

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Modules")
        self.setStyleSheet("background-color: #1e293b;")
        self.resize(1024, 480)
        self.setMaximumSize(1024, 480)

        # Sample data structure - in a real app, this would come from a database
        self.categories = {
            "math": {"total": 10, "solved": 6},
            "c": {"total": 11, "solved": 10},
            "cpp": {"total": 8, "solved": 3},
            "dsa": {"total": 15, "solved": 8},
            "dp": {"total": 12, "solved": 10},
        }

        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(16, 16, 16, 16)

        # Add progress modules for each category
        row, col = 0, 0
        for i, (category, data) in enumerate(self.categories.items()):
            progress = int((data["solved"] / data["total"]) * 100) if data["total"] > 0 else 0
            mod = ProgressModule(category, progress, data["total"], data["solved"])
            mod.playClicked.connect(self.onPlayClicked)
            grid.addWidget(mod, row, col)

            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1

        # Add summary modules (3)
        total_modules = len(self.categories)
        total_problems = sum(data["total"] for data in self.categories.values())
        solved_problems = sum(data["solved"] for data in self.categories.values())
        avg_progress = int((solved_problems / total_problems) * 100) if total_problems > 0 else 0
        completed_modules = sum(1 for data in self.categories.values() if data["solved"] == data["total"])

        summary_data = [
            (str(total_modules), "Total Modules"),
            (f"{avg_progress}%", "Average Progress"),
            (str(completed_modules), "Completed"),
        ]

        for i, (num, desc) in enumerate(summary_data):
            summ = SummaryModule(num, desc)
            grid.addWidget(summ, row + 1, i)

        self.setLayout(grid)

    def onPlayClicked(self, category):
        # Fetch problems for the selected category
        problems:list = fetchQuestions(category)
        self.problem_dialog = ProblemListDialog(category, problems)
        self.problem_dialog.problemSelected.connect(self.problemSelected.emit)
        self.problem_dialog.show()

def resurce_path(relative_path:str):
    if getattr(sys,'frozen',False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

def load_stylesheet(filename:str):
    with open(resurce_path(filename),'r') as file:
        return file.read()


def main():
    app = QApplication(sys.argv)
    screen = qgi.primaryScreen()
    size = screen.availableGeometry()
    #getting the motinor height and width
    monitor_width = size.width();
    monitor_height = size.height()  ;
    StyleSheet  = load_stylesheet('styles/style.css')
    app.setStyleSheet(StyleSheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
