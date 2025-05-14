from PyQt5.QtCore import Qt, QThread ,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QVBoxLayout
from ai import GenaiResponse
import requests
import os
import sys
from dotenv import load_dotenv,dotenv_values
class GeminiVerifyCode(QThread):
    progress = pyqtSignal(str)
    def __init__(self,api_key:str,model:str,original_code:str):
        super().__init__()
        self.prompt = """
        You are a code security expert. Your task is to carefully review submitted code and identify any potentially harmful or malicious behavior. Look specifically for:
        1.System-level access (e.g., reading/writing files, modifying system settings)
        2.Network operations (e.g., socket usage, HTTP requests)
        3.Execution of shell commands or subprocesses
        4.Attempts to access or modify environment variables, sensitive directories, or user/system data
        5.Any code that could break out of a sandboxed or restricted environment
        if there is something unsafe just response:"unsafe " and then add those lines which are making the code unsafe and also comment about why it is unsafe in very short 2-3 line.else response: "safe".no introduction or extra words form ai are required or permitted.
        """
        self.code  = original_code;
        self.ai = GenaiResponse(api_key,model,self.prompt)
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
        if not os.path.exists(BASE_TEMP_DIR):
            try:
                os.makedirs(BASE_TEMP_DIR)
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
    def compile_code(self,code:str, language:str, job_dir:str):
        """Compiles code (C++, Java) within the job directory."""
        if language == "cpp":
            with open(os.path.join(job_dir, "source.cpp"), "w") as source_file:
                source_file.write(code)
            executable_name = "a.out" if platform.system() == "Linux" else "a.exe"
            executable_path = os.path.join(job_dir, executable_name)
            compile_command = ["g++", "source.cpp", "-o", executable_path]
            try:
                process = subprocess.run(
                    compile_command,
                    cwd=job_dir,  # Run in job dir
                    capture_output=True,
                    timeout=10,
                )
                if process.returncode != 0:
                    return None, f"Compilation Error: {process.stderr.decode('utf-8')}"
                return executable_path, None
            except subprocess.TimeoutExpired:
                return None, "Compilation timed out"

        elif language == "c":
            with open(os.path.join(job_dir, "source.c"), "w") as source_file:
                source_file.write(code)
            executable_name = "a.out" if platform.system() == "Linux" else "a.exe"
            executable_path = os.path.join(job_dir, executable_name)

            compile_command = ["gcc", "source.c","-o",executable_path]

            try:
                process = subprocess.run(
                    compile_command,
                    cwd=job_dir,  # Run in job dir
                    capture_output=True,
                    timeout=10,
                )
                if process.returncode != 0:
                    return None, f"Compilation Error: {process.stderr.decode('utf-8')}"
                return executable_path, None
            except subprocess.TimeoutExpired:
                return None, "Compilation timed out"
        elif language == "python":
            with open(os.path.join(job_dir, "script.py"), "w") as script_file:
                script_file.write(code)
            return os.path.join(job_dir, "script.py"), None
        else:
            return None, "Unsupported language"
    def execute_code(self,executable, language, input_data, job_dir):
        """Executes code within the job directory, with resource limits."""

        env = create_restricted_environment()
        start_time = time.time()
        try:
            if language == "cpp":
                process = subprocess.run(
                    [executable],
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                    cwd=job_dir,  # Run in the job directory
                )
            elif language == "c":
                process = subprocess.run(
                    [executable],  # Assumes Main class
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                    cwd=job_dir,
                )
            elif language == "python":
                process = subprocess.run(
                    ["python3", executable],
                    input=input_data.encode("utf-8"),
                    capture_output=True,
                    timeout=self.MAX_EXECUTION_TIME,
                    env=env,
                    cwd=job_dir,
                )
            else:
                return "Error: Unsupported language", 5

            end_time = time.time()
            execution_time = end_time - start_time
            if execution_time > MAX_EXECUTION_TIME:
                return "Time Limit Exceeded", 1

            if process.returncode != 0:
                return f"Runtime Error: {process.stderr.decode('utf-8')}", 2
            return process.stdout.decode("utf-8"), 0

        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", 1
        except Exception as e:
            return f"Error: {str(e)}", 3


    def chekc_network_connection(self):
        try:
            response = requests.get("https://google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False  
    def run(self):
        if(self.chekc_network_connection()):
            self.response = self.ai.response(self.code)
            if("unsafe" in self.response.text):
                text = self.response.text.split("unsafe")
                self.progress.emit(f"<h3>unsafe</h3>{text[-1]}")
        else:
            self.progress.emit("No Internet Connection...")

class VjudgeAi(QWidget):
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
    def setResponse(self,text:str):
        self.warrning_widget.setText(text)

    def read_env(self):
        global API_KEY , AI_MODEL
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        AI_MODEL= os.getenv("AI_MODEL")
    def WarrningShow(self):
        original_code = """
    import os
        
    directory_path = "~"
        
    try:
            os.rmdir(directory_path)
            print(f"Directory '{directory_path}' removed successfully.")
    except FileNotFoundError:
            print(f"Directory '{directory_path}' not found.")
    except OSError:
            print(f"Directory '{directory_path}' is not empty.")
        """

        self.read_env()
        #getting the motinor height and width
        window = VjudgeAi(API_KEY,AI_MODEL,original_code)
        window.show()
