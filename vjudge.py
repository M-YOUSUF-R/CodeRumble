from PyQt5.QtCore import Qt, QThread ,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QVBoxLayout
from ai import GeminiVerifyCode
import subprocess
import time
import platform
import tempfile
import os
import sys


class Vjudge(QWidget):
    def __init__(self,api_key:str,model:str,original_code:str):
        super().__init__()
        self.gemini_verify = GeminiVerifyCode(api_key,model,original_code)
        self.gemini_verify.progress.connect(self.setResponse)
        self.gemini_verify.start()

        self.warrning_widget = QLabel()
        self.warrning_widget.setWordWrap(True)
        self.warrning_widget.setStyleSheet(
            """
            background-color: black;
            color: #4af8f4;
            padding: 10px;
            border: 2px solid #4af8f4;
            border-radius: 5px;
            """
        )
        self.warrning_widget.setAlignment(Qt.AlignCenter)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.warrning_widget)
        self.setLayout(self.main_layout)
        self.setStyleSheet(
            """
            background-color: black;
            color: #4af8f4;
            border: 1px solid #4af8f4;
            """
        )
        self.setFixedSize(480,240)
        self.ALLOWED_LANGUAGES = ["python", "cpp", "c"]
        self.MAX_EXECUTION_TIME = 5  # Seconds
        self.MAX_MEMORY_MB = 128  # MB (Enforcing this in Python is tricky)
        self.BASE_TEMP_DIR = "/tmp"  #  Good default for Linux

    def create_restricted_environment(self):
        """Creates a restricted execution environment (more robust)."""
        if platform.system() == "Windows":
            BASE_TEMP_DIR = os.path.join(
            os.environ.get("TEMP"), "vjudge_temp"
        )   # Use user's temp, create vjudge_temp
        #  Create base temp dir if it does not exist
        if not os.path.exists(self.BASE_TEMP_DIR):
            try:
                os.makedirs(self.BASE_TEMP_DIR)
            except OSError as e:
                print(f"Error creating temp dir: {e}")
                #  Consider logging and exiting.  If you can't create a temp dir,
                #  you're in serious trouble.
                raise
        env = os.environ.copy()
        for var in [
        "LD_PRELOAD",
        "DYLD_INSERT_LIBRARIES",
        "PATH",
        "HOME",  # Remove HOME
        "USER",  # Remove USER
        "USERNAME",  # Remove USERNAME
        ]:
            env.pop(var, None)
        #  Explicitly set a very minimal PATH
        if platform.system() == "Linux":
            env["PATH"] = "/usr/bin:/bin"  #  essential
        elif platform.system() == "Windows":
            env["PATH"] = "C:\\Windows\\System32;C:\\Windows"
        return env        
    def compile_code(self,code:str, language:str):
        """Compiles code (C++, Java) within the job directory."""
        ###############################################
        # creating temporary directory for  code      #
        # this will be deleted after the work is done #
        ###############################################
        temp_dir = ".temp"
        if (not os.path.isdir(temp_dir)):
            os.mkdir(temp_dir)
        ########################################
        # compilation process for c++ language #
        ########################################
        if language == "cpp":
            temp_file_name = "script.cpp"
            temp = f"{temp_dir}/{temp_file_name}"
            with open(temp, "w") as source_file:
                source_file.write(str(code))
            executable_name = "a.out" if platform.system() == "Linux" else "a.exe"
            executable_path = executable_name
            compile_command = ["g++", temp_file_name, "-o", executable_path]
            try:
                process = subprocess.run(
                    compile_command,
                    cwd = temp_dir,
                    capture_output=True,
                    timeout=10,
                )
                if process.returncode != 0:
                    return None, f"Compilation Error: {process.stderr.decode('utf-8')}"
                return executable_path, None
            except subprocess.TimeoutExpired:
                return None, "Compilation timed out"
        ##############################
        # compilation for c language #
        ##############################
        elif language == "c":
            temp_file_name = "script.c"
            temp = f"{temp_dir}/{temp_file_name}"
            with open(temp, "w") as source_file:
                source_file.write(str(code))
            executable_name = "a.out" if platform.system() == "Linux" else "a.exe"
            executable_path = executable_name

            compile_command = ["gcc", temp_file_name ,"-o",executable_path]

            try:
                process = subprocess.run(
                    compile_command,
                    cwd= temp_dir, 
                    capture_output=True,
                    timeout=10,
                )
                if process.returncode != 0:
                    return None, f"Compilation Error: {process.stderr.decode('utf-8')}"
                return executable_path, None
            except subprocess.TimeoutExpired:
                return None, "Compilation timed out"
        ###################################
        # compilation for python language #
        ###################################
        elif language == "python":
            temp_file_name = "script.py"
            temp = f"{temp_dir}/{temp_file_name}"
            with open(temp, "w") as script_file:
                # print(type(code))
                script_file.write(str(code))
            return temp, None
        else:
            return None, "Unsupported language"
    def execute_code(self,executable, language, input_data):
        """Executes code within the job directory, with resource limits."""
        ####################################################
        # creating a restricted environment to run program #
        ####################################################
        env = self.create_restricted_environment()
        start_time = time.time()
        try:
            ##########################################################
            # executing 'c++' program executable to the restricted env #
            ##########################################################
            if language == "cpp":
                process = subprocess.run(
                    [executable],
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                )
            ##########################################################
            # executing 'c' program executable to the restricted env #
            ##########################################################

            elif language == "c":
                process = subprocess.run(
                    [executable],  # Assumes Main class
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                )
            ##################################################
            # running 'python' program to the restricted env #
            ##################################################
            elif language == "python":
                python_path = sys.executable
                process = subprocess.run(
                    [python_path, executable],
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                )
            else:
                return "Error: Unsupported language", 5

            end_time = time.time()
            execution_time = end_time - start_time
            if execution_time > self.MAX_EXECUTION_TIME:
                return "Time Limit Exceeded", 1

            if process.returncode != 0:
                return f"Runtime Error: {process.stderr.decode('utf-8')}", 2
            return process.stdout.decode("utf-8"), 0

        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", 1
        except Exception as e:
            return f"Error: {str(e)}", 3
    def setResponse(self,text:str):
        self.warrning_widget.setText(text)
    def removeFileAndExecutable(self):
        
        pass

        
