from google import genai
from PyQt5.QtCore import QThread , pyqtSignal
import requests
class GenaiResponse():
    def __init__(self,api_key:str,model:str,prompt:str):
        self.client = genai.Client(api_key=api_key)
        self.prompt = prompt+"\n"

    def response(self,content:str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[self.prompt + content]
        ) 
        return response;
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
        self.code  = str(original_code);
        self.ai = GenaiResponse(api_key,model,self.prompt)
        


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
