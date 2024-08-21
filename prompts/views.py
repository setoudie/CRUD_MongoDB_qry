from binascii import a2b_uu
from traceback import print_tb

from django.shortcuts import render
from pymongo import MongoClient
# Create your views here.
cmptr = -1
def auto_id(i):
    return i+1

# client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')
client = MongoClient("mongodb://localhost:27017/") # Driver pour creer des db Mongos
db = client.promptsdb
prompts = db.prompts

# Function pour creer un nouveau prompt
def create_prompt(request):
    if request.method == 'POST':
        # print('test')
        # Creation de la collection `prompts`
        global cmptr
        data = request.POST
        owner_username = data.get('owner_username')
        prompt_content = data.get('content')
        cmptr = cmptr+1
        print(cmptr)

        prompt_doc = {'user':f"{owner_username}", "content": f"{prompt_content}"}
        print(prompt_doc)
        try:
            # insert les information dans la collection `prompts`
            prompts.insert_one(prompt_doc).insert_id
        except Exception as e:
            print(f"Erreur : {e}")
        # return redirect('index', prompt_id=prompt.pid)
    return render(request, 'prompts/create_prompt.html')

def delete_prompt(request, prompt_id):
#     prompts.find_one(objInstance)
    print(prompt_id)

    if request.method == 'POST':
        data = request.POST