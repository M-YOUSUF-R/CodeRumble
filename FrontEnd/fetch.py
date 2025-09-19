import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("BACKEND_URL")
#f'{os.getenv("BACKEND_URL")}/api/questions/?category=math'
def fetchQuestions (category)-> list:
    url = f'{BASE_URL}/api/questions/?category={category}'
    data = requests.get(url)
    print(data)
    # print(data.json())
    # return data.json()

print(fetchQuestions('math'))
