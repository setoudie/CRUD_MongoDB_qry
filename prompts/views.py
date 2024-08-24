"""
    Objectif : Creer une app CRUD en utilisant une base de donnnes NoSQL de type document (MongoDB ici)
    C (Create) --> create_prompt(request) : avec cette fonction on arrive a inserer des prompts dans la DB
    R (Read) --> show_all_prompt(request) : On arrive a visualiser tous les prompts de la DB sur une interface
    U (Update) --> update_prompt(request, prompt_id) : On doit pouvoir modifier n'importe quel prompt en connaissant l'id
    D (Delete) --> delete_promt(request, prompt_id) : ```````````````` supprimer ```````````````````````````````````l'id
"""

from bson.objectid import ObjectId
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
# Create your views here.


# client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')
client = MongoClient("mongodb://localhost:27017/") # Connection a la DB Mongo
db = client.promptsdb
prompts = db.prompts

# Function pour creer un nouveau prompt
"""
    Cette fonction est celui qui permet de creer un prompt
    Elle recupere les informations d'un form html et cree un document (prompt) dans la collection prompts. 
    Ce document est stocke dans une base de donnes MongoDB (promptsdb) qui une BD NoSQL de type document.
"""
def create_prompt(request):
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



# This function is used to delete a specific prompt
"""
    Dans cette fonction a partir de l'Id du prompt, on recupere les informations relatifs au prompt a supprimer.
    Une fois ces informations recuperees on cree un dict ou on les stockent. 
    Au niveau de mon template il y a un bouton supprimer (action "POST"), ce bouton supprime et redirige vers la page 
    de c reation de prompt.
"""
def delete_prompt(request, prompt_id):
    # Trouver et vérifier si le prompt existe
    # print('1 --> ',prompt_id)
    id_of_prompt_to_delete = {'_id': ObjectId(prompt_id)}
    prompt_to_delete = db.prompts.find_one(id_of_prompt_to_delete)

    # prompt_info = [val for val in prompt_to_delete.values()]
    prompt_content = {
        'id': prompt_id,
        'owner_username': prompt_to_delete['user'],
        'content': prompt_to_delete['content']
    }

    # print('2 --> ', prompt_content)

    # print('3 --> ', type(prompt_to_delete), prompt_to_delete['content'])

    if request.method == 'POST':
        db.prompts.delete_one(id_of_prompt_to_delete) # Delete the prompt
        return redirect('create_prompt')

    return render(request, 'prompts/delete_prompt.html', {'prompt_to_delete':prompt_content})

def show_all_prompt(request):
    return HttpResponse('<h1>Here we\'ll show all prompt</h1>')