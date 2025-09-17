import sys

from PyQt5.QtWidgets import(
    QApplication,QWidget,QSplitter,QFrame,QLabel,QPushButton,QLineEdit,
    QHBoxLayout,QVBoxLayout,QTextEdit
)

from PyQt5.QtGui import QFont ,  QPixmap , QColor , QPalette
from PyQt5.QtCore import Qt
from editor import EditorUI
from vjudge import Vjudge
import os
import tempfile

from fetch import fetchQuestions

from dotenv import load_dotenv,dotenv_values

load_dotenv()


class MainUi(QWidget):
    def __init__(self,width=1440,height=720):
        super().__init__()
        self.setWindowTitle("Problem Solving Game")
        self.setMinimumSize(width,height)
        self.setStyleSheet("""
            background-color: #0f172a;
            color: #e2e8f0;
        """)

        self.question_widget = QTextEdit()
        self.question_widget.setReadOnly(True)
        self.question_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                color: #e2e8f0;
                font-size: 14px;
            }
        """)

        self.testcase_widget = QTextEdit()
        self.testcase_widget.setReadOnly(True)
        self.testcase_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                color: #e2e8f0;
                font-size: 13px;
            }
        """)

        self.output_widget = QTextEdit()
        self.output_widget.setReadOnly(True)
        self.output_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                color: #e2e8f0;
                font-size: 13px;
            }
        """)

        # New widgets for right panel
        self.hint_widget = QTextEdit()
        self.hint_widget.setReadOnly(True)
        self.hint_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                color: #94a3b8;
                font-size: 13px;
            }
        """)

        self.result_widget = QTextEdit()
        self.result_widget.setReadOnly(True)
        self.result_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                color: #e2e8f0;
                font-size: 13px;
            }
        """)

        self.left_panel = self.create_left_panel(title='Question Panel')
        self.left_panel.setObjectName('panel')
        self.left_panel.setMinimumWidth(420)
        self.left_panel.setMaximumWidth(480)
        self.left_panel.setStyleSheet("""
            QWidget#panel {
                background-color: #1e293b;
                border-radius: 8px;
                margin: 5px;
            }
        """)

        self.editor_widget = EditorUI()
        self.editor_widget.submit.clicked.connect(self.run_code)
        self.editor_widget.save.clicked.connect(lambda: self.editor_widget.editor.saveFile(self.editor_widget.getCode()))

        self.editor_panel = self.create_editor_panel("Code Editor")
        self.editor_panel.setObjectName('panel')
        self.editor_panel.setMinimumWidth(500)


        self.right_panel = self.create_right_panel("Right Panel")
        self.right_panel.setObjectName('panel')
        self.right_panel.setMaximumWidth(300)
        self.right_panel.setStyleSheet("""
            QWidget#panel {
                background-color: #1e293b;
                border-radius: 8px;
                margin: 5px;
            }
        """)

        self.judge = Vjudge(os.getenv("API_KEY"),os.getenv("AI_MODEL"),self.editor_widget.getCode)

        self.layout = QSplitter()
        self.layout.addWidget(self.left_panel)
        self.layout.addWidget(self.editor_panel)
        self.layout.addWidget(self.right_panel)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.layout)
        self.setLayout(self.main_layout)

        # Load sample data
        # self.load_sample_data()

    def create_panel(self, title: str):
        panel = QWidget()

        label = QLabel(title)
        label.setStyleSheet("""
            background-color:#017682;
            margin:2px;padding:0;
            border:none;
            border-top-left-radius:8px;
            border-top-right-radius:8px;
            color: white;
            font-weight: bold;
            """)
        label.setObjectName("label")
        label.setFixedHeight(30)
        font_family = "Segoe UI, monospace"
        font = QFont(font_family, 10)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(label)
        layout.addStretch(1)
        panel.setLayout(layout)
        return panel, layout

    def create_left_panel(self,
        question_text:str='question fetching....',
        title:str='Question'):
        panel,layout = self.create_panel(title);

        font = QFont()
        font.setPointSize(14)

        self.question_widget.setFont(font)

        layout.addWidget(self.question_widget, 1000)
        return panel;

    def create_editor_panel(self,title:str):
        panel,layout = self.create_panel(title);

        self.editor_widget.setObjectName("editor_widget")
        layout.addWidget(self.editor_widget,1000)
        return panel;

    def create_right_panel(self,title:str):
        panel,layout = self.create_panel(title);

        # Add hint section
        hint_label = QLabel("Solving Hint")
        hint_label.setStyleSheet("""
            color: #38bdf8;
            font-weight: bold;
            padding: 5px;
            background-color: #1e293b;
            border-bottom: 1px solid #334155;
        """)
        layout.addWidget(hint_label)
        layout.addWidget(self.hint_widget, 200)

        # Add test case section
        testcase_label = QLabel("Test Case")
        testcase_label.setStyleSheet("""
            color: #38bdf8;
            font-weight: bold;
            padding: 5px;
            background-color: #1e293b;
            border-bottom: 1px solid #334155;
        """)
        layout.addWidget(testcase_label)
        layout.addWidget(self.testcase_widget, 100)

        # Add output section
        output_label = QLabel("Desired Output")
        output_label.setStyleSheet("""
            color: #38bdf8;
            font-weight: bold;
            padding: 5px;
            background-color: #1e293b;
            border-bottom: 1px solid #334155;
        """)
        layout.addWidget(output_label)
        layout.addWidget(self.output_widget, 100)

        # Add result section
        result_label = QLabel("Result")
        result_label.setStyleSheet("""
            color: #38bdf8;
            font-weight: bold;
            padding: 5px;
            background-color: #1e293b;
            border-bottom: 1px solid #334155;
        """)
        layout.addWidget(result_label)
        layout.addWidget(self.result_widget, 100)

        return panel;


    def run_code(self,input_data = ""):
        code = self.editor_widget.getCode()
        language = self.editor_widget.getCodeLanguage()
        try:
            executable , message = self.judge.compile_code(code,language)
            print("message : ",message)
            with open("input.txt",'r') as file:
                input_data = file.read()
            with open("output.txt","w") as output:
                res,_ =  self.judge.execute_code(executable,language,input_data)
                output.write(res)

            # Check if output matches expected result
            with open("output.txt", 'r') as f:
                actual_output = f.read().strip()

            expected_output = self.output_widget.toPlainText().strip()

            if actual_output == expected_output:
                self.result_widget.setText("Accepted")
                self.result_widget.setStyleSheet("""
                    QLineEdit {
                        background-color: #14532d;
                        border: 1px solid #334155;
                        border-radius: 5px;
                        padding: 10px;
                        color: #bbf7d0;
                        font-size: 13px;
                        font-weight: bold;
                    }
                """)
            else:
                self.result_widget.setText(f"Wrong Answer. Got: {actual_output}")
                self.result_widget.setStyleSheet("""
                    QLineEdit {
                        background-color: #7c2d12;
                        border: 1px solid #334155;
                        border-radius: 5px;
                        padding: 10px;
                        color: #fed7aa;
                        font-size: 13px;
                    }
                """)

        except Exception as e:
            print("EXECUTABLE,MESSAGE ERROR: ",e)
            self.result_widget.setText(f"Error: {str(e)}")
            self.result_widget.setStyleSheet("""
                QLineEdit {
                    background-color: #7f1d1d;
                    border: 1px solid #334155;
                    border-radius: 5px;
                    padding: 10px;
                    color: #fecaca;
                    font-size: 13px;
                }
            """)
