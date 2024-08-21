from traceback import print_tb

from django.shortcuts import render
from pymongo import MongoClient
# Create your views here.

# client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')

def create_prompt(request):
    client = MongoClient("mongodb://localhost:27017/") # Driver pour creer des db Mongos
    db = client.promptsdb
    prompts = db.prompts

    if request.method == 'POST':
        # print('test')
        # Creation de la collection `prompts`
        data = request.POST
        owner_username = data.get('owner_username')
        prompt_content = data.get('content')

        prompt_doc = {'user':f"{owner_username}", "content": f"{prompt_content}"}
        # print(prompt_doc)
        try:
            # insert les information dans la collection `prompts`
            prompts.insert_one(prompt_doc)
        except Exception as e:
            print(f"Erreur : {e}")
        # return redirect('index', prompt_id=prompt.pid)
    return render(request, 'prompts/create_prompt.html')
