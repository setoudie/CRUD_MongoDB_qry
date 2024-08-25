
# Application CRUD Django avec MongoDB

Cette application est un exemple simple de CRUD (Creat, Read, Update, Delete) développé avec Django et MongoDB comme base de données NoSQL. L'application permet aux utilisateurs de créer, visualiser, mettre à jour et supprimer des prompts dans une collection MongoDB.

## Prérequis

Avant d'exécuter le projet, assurez-vous d'avoir les éléments suivants installés :

- Python 3.11
- Django
- MongoDB
- pymongo

## Installation

### 1. Cloner le Répertoire

```bash
git clone https://github.com/setoudie/CRUD_MongoDB_qry.git
cd CRUD_MongoDB_qry
```

### 2. Créer et Activer un Environnement Virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

Assurez-vous que votre `requirements.txt` contient les éléments suivants :

```
Django
pymongo
```

### 4. Configurer MongoDB

Assurez-vous que MongoDB est installé et en cours d'exécution sur votre système. Vous pouvez démarrer MongoDB avec la commande suivante :

```bash
mongosh
```

L'application se connecte à MongoDB en utilisant la configuration par défaut suivante :
```python
client = MongoClient("mongodb://localhost:27017/")
```

Vous pouvez modifier la chaîne de connexion pour correspondre à votre configuration si nécessaire.

## Utilisation

### Démarrer le Serveur de Développement

Pour démarrer le serveur de développement Django, utilisez la commande suivante :

```bash
python manage.py runserver
```

Visitez `http://127.0.0.1:8000/` pour accéder à l'application.

## Opérations CRUD

L'application effectue les opérations suivantes sur la collection MongoDB `prompts` :

### 1. Créer un Prompt

#### Route : `prompt/create/`

- **Méthode :** POST
- **Description :** Les utilisateurs peuvent créer un nouveau prompt en fournissant un nom d'utilisateur et le contenu du prompt via un formulaire.
- **Template HTML :** `create_prompt.html`

Exemple :
```python
def create_prompt(request):
    if request.method == 'POST':
        data = request.POST
        owner_username = data.get('owner_username')
        prompt_content = data.get('content')
        prompt_doc = {'user': owner_username, 'content': prompt_content}
        prompts.insert_one(prompt_doc)
    return render(request, 'prompts/create_prompt.html')
```

### 2. Lire Tous les Prompts

#### Route : `prompt/dashboard/`

- **Méthode :** GET
- **Description :** Affiche tous les prompts stockés dans la collection MongoDB dans un format de liste sur une page HTML.
- **Template HTML :** `show_all_prompt.html`

Exemple :
```python
def show_all_prompt(request):
    collection = db.prompts.find()
    all_prompts = [{'content': doc['content'], 'user': doc['user']} for doc in collection]
    return render(request, 'prompts/show_all_prompt.html', {'prompts': all_prompts})
```

### 3. Mettre à Jour un Prompt

#### Route : `prompt/update/<prompt_id>/`

- **Méthode :** POST
- **Description :** Met à jour le contenu d'un prompt existant en utilisant son ID. Le nouveau contenu est soumis via un formulaire.
- **Template HTML :** `update_prompt.html`

Exemple :
```python
def update_prompt(request, prompt_id):
    id_of_prompt_to_update = {'_id': ObjectId(prompt_id)}
    prompt_to_update = db.prompts.find_one(id_of_prompt_to_update)

    if request.method == 'POST':
        data = request.POST
        new_prompt_content = data.get('content')
        prompts.update_one(id_of_prompt_to_update, {'$set': {'content': new_prompt_content}})
        return redirect('create_prompt')
    return render(request, 'prompts/update_prompt.html', {'prompt': prompt_to_update})
```

### 4. Supprimer un Prompt

#### Route : `prompt/delete/<prompt_id>/`

- **Méthode :** POST
- **Description :** Supprime un prompt existant en utilisant son ID.
- **Template HTML :** `delete_prompt.html`

Exemple :
```python
def delete_prompt(request, prompt_id):
    id_of_prompt_to_delete = {'_id': ObjectId(prompt_id)}
    if request.method == 'POST':
        db.prompts.delete_one(id_of_prompt_to_delete)
        return redirect('create_prompt')
    return render(request, 'prompts/delete_prompt.html', {'prompt_to_delete': prompt_content})
```

## Configuration de MongoDB

La base de données MongoDB est configurée pour se connecter en utilisant le serveur local par défaut :
```python
client = MongoClient("mongodb://localhost:27017/")
db = client.promptsdb
prompts = db.prompts
```

Vous pouvez modifier la chaîne de connexion pour correspondre à votre configuration MongoDB si nécessaire.

## Templates

Le projet utilise les templates HTML suivants :
- `create_prompt.html` : Un formulaire pour créer un nouveau prompt.
- `show_all_prompt.html` : Affiche tous les prompts dans un format de liste.
- `update_prompt.html` : Un formulaire pour mettre à jour un prompt existant.
- `delete_prompt.html` : Confirme la suppression d'un prompt.

## License

Ce projet est open-source est juste un TAF pour mieux comprendre la DB MongoDB.
