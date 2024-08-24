from binascii import a2b_uu
from http.client import HTTPResponse
from traceback import print_tb

from bson.objectid import ObjectId
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
# Create your views here.


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

        prompt_doc = {'user':f"{owner_username}", "content": f"{prompt_content}"}
        # print(prompt_doc)
        try:
            # insert les information dans la collection `prompts`
            prompts.insert_one(prompt_doc)

            # prompt_id = '66c5e8cc13491d3f2bdb91cc'
            # prompt = db.prompts.find_one({'_id': ObjectId(prompt_id)})
            #
            # if prompt:
            #     print(prompt)
            # else:
            #     print("Prompt not found.")

        except Exception as e:
            print(f"Erreur : {e}")
        # return redirect('index', prompt_id=prompt.pid)
    return render(request, 'prompts/create_prompt.html')



# This function is used to delete a specific prompt
def delete_prompt(request, prompt_id):
    # Trouver et vérifier si le prompt existe
    print(prompt_id)
    prompt_to_delete = db.prompts.find_one({'_id': ObjectId(prompt_id)})

    if not prompt_to_delete:
        return HttpResponse("Prompt not found", status=404)

    # Supprimer le document
    db.prompts.delete_one({'_id': ObjectId(prompt_id)})

    return HttpResponse("good")