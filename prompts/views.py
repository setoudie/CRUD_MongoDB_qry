"""
    Objectif : Creer une app CRUD en utilisant une base de donnnes NoSQL de type document (MongoDB ici)
    C (Create) --> create_prompt(request) : avec cette fonction on arrive a inserer des prompts dans la DB
    R (Read) --> show_all_prompt(request) : On arrive a visualiser tous les prompts de la DB sur une interface
    U (Update) --> update_prompt(request, prompt_id) : On doit pouvoir modifier n'importe quel prompt en connaissant l'id
    D (Delete) --> delete_promt(request, prompt_id) : ```````````````` supprimer ```````````````````````````````````l'id
"""
from http.client import ResponseNotReady

from bson.objectid import ObjectId
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
# Create your views here.

# Informations de connexion a la base de donnees
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
    de creation de prompt.
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


# This is the function used to show all prompt
"""
    Cette fonction a ete la plus facile a implementer, il siffut juste de recuperer les datas et de les stocke dans un dico afin 
    de pouvoir les manipuler (afficher) dans le template html. C'est pas sorcier :)
"""
def show_all_prompt(request):
    collection = db.prompts.find() # `collection` is all raw prompt data of the promptsdb database
    # Getting all prompt and save it in a list of dict ---> [{'content': 'prompt content', 'user': 'own prompt username'},...]
    all_prompts = [{'content' : doc['content'], 'user': doc['user']} for doc in collection]
    # print(all_prompts)
    # return HttpResponse('<h1>Here we\'ll show all prompt</h1>')
    return render(request, 'prompts/show_all_prompt.html', {'prompts':all_prompts})


# This is the function used to update a prompt
"""
    
"""
def update_prompt(request, prompt_id):
    id_of_prompt_to_update = {'_id': ObjectId(prompt_id)}
    prompt_to_update = db.prompts.find_one(id_of_prompt_to_update)

    prompt_to_update = {
        'id': prompt_id,
        'owner_username': prompt_to_update['user'],
        'content': prompt_to_update['content']
    }

    if request.method == 'POST':
        data = request.POST


    return render(request, 'prompts/update_prompt.html', {'prompt':prompt_to_update})