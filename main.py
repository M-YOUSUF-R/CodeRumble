import sys

from PyQt5.QtWidgets import(
    QApplication,QWidget,QSplitter,QFrame,QLabel,QPushButton,QLineEdit,
    QHBoxLayout,QVBoxLayout
)

from PyQt5.QtGui import QFont ,  QPixmap , QColor , QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as qgi
from editor import EditorUI
import os
class GameUI(QWidget):
    def __init__(self,width,height):
        super().__init__()
        self.setWindowTitle("Problem Solving Game")
        self.setMinimumSize(width,height)
        print(f"height: {height} and width: {width}")
        print(f"ration: {width/height} 16:9 = {16/9}")
        self.setStyleSheet("background-color:black; color: #4af8f4;")

        self.left_panel = self.create_left_panel("Questions")
        self.left_panel.setObjectName('panel')
        self.left_panel.setMinimumWidth(470)
        self.left_panel.setMaximumWidth(480)
        self.editor_panel = self.create_editor_panel("Code editor")
        self.editor_panel.setObjectName('panel')
        self.editor_panel.setMinimumWidth(500)
        self.right_panel = self.create_right_panel("Right panel")
        self.right_panel.setObjectName('panel')
        self.right_panel.setMaximumWidth(350)
        

        self.layout = QSplitter()
        self.layout.addWidget(self.left_panel)
        self.layout.addWidget(self.editor_panel)
        self.layout.addWidget(self.right_panel)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.layout)
        self.setLayout(self.main_layout)



    def create_panel(self, title: str):
        panel = QWidget()
        # panel.setFrameShape(QFrame.StyledPanel) # Good practice for QFrame

        label = QLabel(title)
        label.setStyleSheet("""
            background-color:#017682;
            margin:2px;padding:0;
            border:none;
            border-top-left-radius:2px;
            border-top-right-radius:2px;
            """)
        label.setObjectName("label")
        label.setFixedHeight(30)
        font_family = "Share Tech Mono, monospace"
        font = QFont(font_family, 10)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) # Remove margins inside the frame layout
        layout.setSpacing(0) # Remove spacing between label and content
        layout.addWidget(label)
        layout.addStretch(1) # Remove stretch for now, add content directly
        panel.setLayout(layout)
        return panel, layout # Return layout too
   
    def create_left_panel(self,title:str):
        panel,layout = self.create_panel(title);
        return panel;
    def create_editor_panel(self,title:str):
        panel,layout = self.create_panel(title);
        editor_widget = EditorUI()
        editor_widget.setObjectName("editor_widget")
        layout.addWidget(editor_widget,1000)
        return panel;
    def create_right_panel(self,title:str):
        panel,layout = self.create_panel(title);
        return panel;
        
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
    window = GameUI(1080,720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
