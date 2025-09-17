from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    QObject,
    QThread,
    pyqtSignal
    # Importing necessary modules from PyQt5.QtCore for Qt functionalities, signals and threads.
)

from PyQt5.QtGui import QIcon , QFont

from PyQt5.QtWidgets import (
    QApplication,QWidget,
    QPushButton,QLabel,QTextEdit,
    QFileDialog,QLineEdit,
    QVBoxLayout,QHBoxLayout,
)  # Importing various PyQt5.QtWidgets modules for creating GUI elements like windows, layouts, buttons, text editors, etc.

# Importing QColor from PyQt5.QtGui for color settings.
from PyQt5.QtGui import QColor

from PyQt5.Qsci import (
    QsciScintilla,
    QsciAPIs,QsciLexerPython,
    QsciLexerCPP,QsciLexerHTML,
    QsciLexerCSS,QsciLexerJavaScript
    # Importing QsciScintilla and various lexer modules from PyQt5.Qsci for advanced code editor functionalities.
)

import os  # Importing the os module for operating system functionalities.

import platform  # Importing the platform module for system functionalities.

# Importing the subprocess module for running external commands.
import subprocess

import shutil  # Importing the shutil module for high-level file operations.

import webbrowser #importing webbrowser to redirect to api key page

# Importing the sys module for system-specific parameters and functions.
import sys
import builtins
import keyword
import jedi
import inspect

# Defining a class UI that inherits from QWidget to represent the main user interface.
class EditorUI(QWidget):

    def __init__(self):  # Constructor for UI.

        super().__init__()
        self.editor = Editor()
        self.editor.setObjectName("editor_widget")

        self.python = QPushButton('python')
        self.python.setObjectName("python_btn")
        self.python.setStyleSheet("""
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)

        self.language = ""

        self.python.setFixedWidth(50)
        self.python.setFixedHeight(25)
        self.python.clicked.connect(self.runPythonBtn)

        self.c = QPushButton('c')
        self.c.setObjectName('c_btn')
        self.c.setStyleSheet("""
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.c.setFixedWidth(50)
        self.c.setFixedHeight(25)
        self.c.clicked.connect(self.runCBtn)

        self.cxx = QPushButton('c++')
        self.cxx.setObjectName('cxx_btn')
        self.cxx.setStyleSheet("""
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.cxx.setFixedWidth(50)
        self.cxx.setFixedHeight(25)
        self.cxx.clicked.connect(self.runCxxBtn)

        #save button
        self.save = QPushButton('save')
        self.save.setStyleSheet("""
            background-color: #017682;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.save.setFixedWidth(50)
        self.save.setFixedHeight(22)
        self.save.setObjectName('save_btn')

        self.submit = QPushButton('submit')  # Creating a Send button.
        self.submit.setStyleSheet("""
            background-color: #017682;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.dummybtn = QLabel()
        self.submit.setFixedWidth(50)
        self.submit.setFixedHeight(22)
        self.submit.setObjectName('submit_btn')

        self.submitLayout = QHBoxLayout()
        self.submitLayout.addWidget(self.dummybtn)
        self.submitLayout.addWidget(self.save)
        self.submitLayout.addWidget(self.submit)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0,0,0,0)
        self.buttonLayout.setSpacing(2)
        self.buttonLayout.addWidget(self.c)
        self.buttonLayout.addWidget(self.cxx)
        self.buttonLayout.addWidget(self.python)
        self.buttonLayout.addWidget(self.dummybtn)

        self.editorLayout = QVBoxLayout()
        self.editorLayout.addLayout(self.buttonLayout)
        self.editorLayout.addWidget(self.editor)
        self.editorLayout.addLayout(self.submitLayout)

        self.setLayout(self.editorLayout)
    def getCode(self):
        return self.editor.text()
    def getCodeLanguage(self):
        return self.language
    def runPythonBtn(self):
        self.language = "python"
        self.python.setStyleSheet(
            self.python.styleSheet() +
            "background-color: #54bfcb;"
        )
        self.c.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.cxx.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.editor.setPythonLexerandAutoCompletion()
    def runCBtn(self):
        self.language = "c"
        self.c.setStyleSheet(
            self.c.styleSheet() +
            "background-color: #54bfcb;"
        )
        self.python.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.cxx.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.editor.setCLexerandAutoCompletion()
    def runCxxBtn(self):
        self.language = "cpp"
        self.cxx.setStyleSheet(
            self.cxx.styleSheet() +
            "background-color: #54bfcb;"
        )
        self.python.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.c.setStyleSheet("""
            background-color: none;
            margin: 0;
            padding: 0;
            border: 1px solid #4af8f4;
            border-radius: none;
        """)
        self.editor.setCxxLexerandAutoCompletion()


# Defining a class Editor that inherits from QsciScintilla for code editing.
class Editor(QsciScintilla):

    def __init__(self):  # Constructor for Editor.

        # Calling the superclass constructor to initialize the QsciScintilla.
        super().__init__()
        self.setPaper(QColor("#1e293b"))
        self.setColor(QColor("#FFFFFF"))
        # Setting the margin type to number margin.
        self.setMarginType(0, QsciScintilla.NumberMargin)
        # for 0000 digit line of code # Setting the width of the margin.
        self.setMarginWidth(0, '00000')

        # Setting the color of the margin.
        self.setMarginsForegroundColor(QColor("#5C6370"))
        self.setMarginsBackgroundColor(QColor("#1e293b"))

        # Setting the wrap mode to wrap by word.
        self.setWrapMode(QsciScintilla.WrapWord)

        # Setting the visual flags for wrapping.
        self.setWrapVisualFlags(QsciScintilla.WrapFlagByText)

        # Setting the indent mode for wrapping.
        self.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        #segging cursor color
        self.setCaretForegroundColor(QColor("#FFCC00"))

        self.setCaretLineVisible(True)  # Making the caret line visible.

        # Setting the background color of the caret line.
        self.setCaretLineBackgroundColor(QColor("#1e3f7ae3"))

        self.setAutoIndent(True)  # Enabling auto-indent.
        self.font = QFont()

        #setting the editor font size
        self.font.setPointSize(12)
        self.setFont(self.font)

        # Enable all sources for auto completion (api + editor stream)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)

        # threshold for the number of character the suggestion will show
        self.setAutoCompletionThreshold(1)

        self.file_path = ''  # Initializing the file path to an empty string.

        # Initializing the directory path to an empty string.
        self.dir_path = ''

    def setPythonLexerandAutoCompletion(self):
        self.lexer = QsciLexerPython()
        self.setupAutocompletePython()
        self.setLexer(self.lexer)
        self.lexer.setPaper(QColor("#1e293b"))
        self.lexer.setColor(QColor("#FFFFFF"))
        self.lexer.setFont(self.font)

    def setCLexerandAutoCompletion(self):
        self.lexer = QsciLexerCPP()
        self.cAutoCompletion()
        self.setLexer(self.lexer)
        self.lexer.setPaper(QColor("#1e293b"))
        self.lexer.setColor(QColor("#FFFFFF"))
        self.lexer.setFont(self.font)

    def setCxxLexerandAutoCompletion(self):
        self.lexer = QsciLexerCPP()
        self.cppAutoCompletion()
        self.setLexer(self.lexer)
        self.lexer.setPaper(QColor("#1e293b"))
        self.lexer.setColor(QColor("#FFFFFF"))
        self.lexer.setFont(self.font)

    def saveFile(self,code:str)->None:  # Method to create a new file.

        fileName, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            os.getcwd(),
            'Python Files (*.py);;C Files (*.c);;C++ Files (*.cpp)'
        )

        if fileName:  # Checking if a file name was selected.

            self.file_path = fileName  # Setting the file path.

            # Setting the directory path.
            self.dir_path = os.path.dirname(fileName)

            # Checking if the file already exists.
            if not os.path.exists(fileName):

                with open(fileName, 'w') as file:  # Creating the file.

                    file.write(code)  # Writing an empty string to the file.

    def setupAutocompletePython(self):
        # Initialize API object for Python Lexer
        api = QsciAPIs(self.lexer)
        # Add built-in functions, keywords, and standard libraries
        self.add_builtin_functions(api)
        self.add_keywords(api)
        self.add_standard_libraries(api)

        # Add third-party modules using jedi
        self.add_third_party_modules(api)

        # Prepare the API for usage in auto-completion
        api.prepare()

    def add_builtin_functions(self, api):
        """Add built-in Python functions (like print(), len(), etc.) to the API"""
        for name, obj in builtins.__dict__.items():
            if callable(obj):
                api.add(name)

    def add_keywords(self, api):
        """Add Python keywords (like if, else, for, etc.) to the API"""
        for kw in keyword.kwlist:
            api.add(kw)

    def add_standard_libraries(self, api):
        """Add common Python standard libraries (like os, sys, math, etc.)"""
        try:
            import sys
            standard_libs = sys.builtin_module_names
            for lib in standard_libs:
                api.add(lib)
        except Exception as e:
            print("Error while adding standard libraries:", e)

        self.add_module_functions(api,'os')
        self.add_module_functions(api,'sys')
    def add_module_functions(self,api,module_name):
        try:
            module = __import__(module_name)
            for name , obj in inspect.getmembers(module):
                if callable(obj):
                    api.add(f"{module_name}.{name}")
        except ImportError:
            print(f"Moudle {module_name} could not imported.")

    def add_third_party_modules(self, api):
        """Add third-party modules installed via pip using jedi."""
        try:
        # Create a static list of currently loaded module names
            installed_modules = list(sys.modules.keys())
            for module_name in installed_modules:
                if module_name not in sys.builtin_module_names:
                    self.add_module_functions(api, module_name)
        except Exception as e:
            print(f"Error while adding third-party modules: {e}")
    def cppAutoCompletion(self):
        api = QsciAPIs(self.lexer)
        """Add C++ keywords and common functions to the auto-completion API for faster suggestion."""
        cpp_headers = [
            "#include", "#define", "#if", "#elif", "#else", "#endif", "#ifdef", "#ifndef", "#pragma", "#error", "#warning",
            "iostream", "fstream", "sstream", "string", "vector", "map", "set", "list", "deque",
            "algorithm", "cmath", "cstdlib", "ctime", "cassert", "cstdio", "cstring", "climits",
            "cfloat", "iterator", "memory", "functional", "thread", "mutex", "condition_variable",
            "atomic", "type_traits", "initializer_list", "tuple", "exception", "stdexcept", "utility",
            "bitset", "random", "regex", "locale", "valarray", "array", "unordered_map", "unordered_set",
            "chrono", "future", "numeric", "memory", "complex", "valarray", "exception", "bitset",
            "tuple", "initializer_list", "atomic", "thread", "mutex", "shared_mutex", "condition_variable",
            "unordered_map", "unordered_set", "deque", "array", "map", "set", "queue", "stack", "bitset",
            "typeindex", "typeinfo", "exception", "stdexcept", "limits", "locale", "random", "regex", "functional",
            "cctype", "cstdlib", "clocale", "cfenv", "cassert", "cstdarg", "cstdio", "cstring", "ctime", "cmath",
            "cstdio", "cfloat", "climits", "iterator", "type_traits", "chrono", "thread", "future", "atomic",
            "sstream", "sstream", "unordered_map", "unordered_set", "shared_ptr", "unique_ptr", "weak_ptr",
            "mutex", "condition_variable", "tuple", "string", "functional", "memory", "exception", "numeric",
            "type_traits", "initializer_list", "cstdint", "iostream", "iomanip", "sstream", "cstdlib", "cstdio",
            "valarray", "array", "tuple", "unordered_map", "unordered_set", "memory", "atomic", "complex", "queue",
            "deque", "list", "map", "set", "vector", "algorithm", "functional", "random", "regex", "locale",
            "bitset", "numeric", "chrono", "thread", "mutex", "condition_variable", "shared_mutex", "memory"
        ]


        for library in cpp_headers:
            api.add(library)

        cpp_keywords = [
            "int", "float", "double", "char", "bool", "void", "if", "else", "while", "for", "switch", "case",
            "break", "continue", "return", "struct", "class", "public", "private", "protected", "namespace",
            "using", "include", "define", "template", "typename", "new", "delete", "try", "catch", "throw",
            "alignas", "alignof", "const", "constexpr", "decltype", "dynamic_cast", "explicit", "export",
            "friend", "inline", "mutable", "noexcept", "nullptr", "operator", "private", "protected",
            "public", "reinterpret_cast", "static", "static_assert", "static_cast", "thread_local", "typeid"
        ]
        for kw in cpp_keywords:
            api.add(kw)

        cpp_functions = [
            "main", "std::cout", "std::cin", "std::endl", "std::string", "std::vector", "std::map",
            "std::set", "std::list", "std::deque", "std::sort", "std::find", "std::max", "std::min",
            "std::abs", "std::swap", "std::to_string", "std::stoi", "std::stod", "std::stof",
            "std::thread", "std::mutex", "std::lock_guard", "std::unique_lock", "std::condition_variable"
        ]
        for func in cpp_functions:
            api.add(func)

        cpp_types = [
            "std::string", "std::vector", "std::map", "std::set", "std::list", "std::deque", "std::pair",
            "std::tuple", "std::array", "std::unique_ptr", "std::shared_ptr", "std::weak_ptr", "std::function",
            "std::atomic", "std::mutex", "std::thread", "std::chrono", "std::exception", "std::runtime_error",
            "std::invalid_argument", "std::out_of_range", "std::logic_error"
        ]
        for t in cpp_types:
            api.add(t)
        api.prepare()

    def cAutoCompletion(self):
        api = QsciAPIs(self.lexer)
        """Add C keywords, functions, and common headers to the auto-completion API."""
        # C headers
        c_headers = [
        "#include", "#define", "#if", "#elif", "#else", "#endif", "#ifdef", "#ifndef", "#pragma", "#error", "#warning",
        "stdio.h", "stdlib", "string", "math", "time", "ctype", "assert", "float.h", "limits.h", "stdarg.h", "stddef.h",
        "inttypes.h", "stdint.h", "errno.h", "signal.h", "setjmp.h", "pthread.h", "unistd.h", "fcntl.h", "sys/types.h",
        "sys/stat.h", "sys/time.h", "sys/socket.h", "netinet/in.h", "arpa/inet.h", "dirent.h", "poll.h", "sys/ioctl.h",
        "sys/mman.h", "sys/utsname.h", "sys/sysctl.h", "syslog.h", "locale.h", "regex.h", "complex.h", "sys/resource.h",
        "pthread.h", "unistd.h", "fcntl.h", "signal.h", "stdalign.h"
        ]

        for header in c_headers:
            api.add(header)

        # C keywords
        c_keywords = [
        "int", "float", "double", "char", "long", "short", "signed", "unsigned", "void", "const", "volatile", "static",
        "extern", "register", "auto", "inline", "typedef", "sizeof", "enum", "struct", "union", "goto", "if", "else",
        "switch", "case", "break", "continue", "return", "for", "while", "do", "default", "typedef", "sizeof",
        "typeof", "alignas", "alignof", "restrict", "noreturn", "noexcept", "typeof"
        ]

        for kw in c_keywords:
            api.add(kw)

        # C standard library functions
        c_functions = [
        "printf", "scanf", "sprintf", "sscanf", "fopen", "fclose", "fread", "fwrite", "fseek", "ftell", "rewind",
        "feof", "ferror", "perror", "malloc", "calloc", "realloc", "free", "exit", "abort", "atexit", "system",
        "getenv", "setenv", "unsetenv", "putenv", "memcpy", "memmove", "memcmp", "memset", "strcpy", "strncpy",
        "strcat", "strncat", "strcmp", "strncmp", "strlen", "strchr", "strrchr", "strstr", "strtok", "strdup",
        "strtol", "strtoul", "strtod", "strtof", "atof", "atoi", "atol", "abs", "labs", "div", "ldiv", "rand",
        "srand", "time", "clock", "localtime", "gmtime", "strftime", "difftime", "mktime", "exit", "fmod", "pow",
        "sqrt", "log", "log10", "exp", "sin", "cos", "tan", "asin", "acos", "atan", "atan2", "ceil", "floor",
        "fabs", "frexp", "modf", "ldexp", "ldexp", "isalpha", "isdigit", "isalnum", "isspace", "isupper", "islower",
        "isprint", "isgraph", "isxdigit", "isblank", "toupper", "tolower", "strcoll", "strxfrm", "strcspn",
        "strspn", "strpbrk", "strlcpy", "strlcat", "getchar", "putchar", "getch", "putch", "gets", "puts"
        ]

        for func in c_functions:
            api.add(func)

        # C types
        c_types = [
        "int", "float", "double", "char", "long", "short", "signed", "unsigned", "void", "const", "volatile",
        "FILE", "size_t", "ptrdiff_t", "ssize_t", "off_t", "clock_t", "time_t", "jmp_buf", "va_list", "sigset_t",
        "pthread_t", "pthread_mutex_t", "pthread_cond_t", "pthread_attr_t", "pthread_key_t", "pthread_once_t",
        "pthread_rwlock_t", "pthread_spinlock_t", "pthread_barrier_t"
        ]

        for t in c_types:
            api.add(t)
        api.prepare()
