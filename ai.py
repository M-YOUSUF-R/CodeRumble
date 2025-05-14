from google import genai

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
