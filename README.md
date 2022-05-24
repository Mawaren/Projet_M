# Projet_M
Projet_Python_Groupe_M

Adresse de test: 0xaf8ae6955d07776ab690e565ba6fbc79b8de3a5d

Adresse de test 2: 0xde23d846b7247c72944722e7d0a59258c8595a29

Idée :

Pouvoir avoir un aperçu clair et précis des transactions et 
de la composition d’un portefeuille de cryptomonnaie en rentrant simplement l’adresse de ce même portefeuille.

Description du projet :

1. Utilisation des apis des principales blockchains de cryptomonnaie pour requêter les données nécessaires à la construction de nos dataframes. (Clés en annexe)

2. Nos dataframes principaux sont :

• L’historique de transaction d’un portefeuille

• Composition du portefeuille

3. Nous utilisons les dataframes afin de matérialiser nos données à travers différents tableaux et graphiques.
Nous avons utilisé Plotly principalement très utile pour visualiser et manipuler la data.

4. Création d’un projet Django afin de display ce que nous avons produit en 3).

5. Utilisation de l’HTML puis du CSS pour finaliser la mise en page.

Django Tutoriel

Création de l’espace de travail
	
Le plus simple est d’utiliser Pycharm et de créer un nouveau projet en choisissant Django et un environnement virtuel



Structure d’un Projet Django



Il est constitué de plusieurs fichiers mais seulement settings, urls  et templates vont nous intéresser.

Settings.py contient tous les réglages d’origine de Django. Lorsque, il y a des modifications à faire comme changer la langue, ajouter des modèles ou des applications, cela se fait dans settings.

Urls contient tous les chemins d’urls du site web. A chaque fois qu' un nouveau chemin est créé il faut le rajouter dans ce fichier.

Enfin, le dossier templates est constitué des fichiers html.

Les commandes principales
Pour lancer le serveur local:
python manage.py runserver 

Pour créer une nouvelle application
	python manage.py startapp + nom  du dossier

Pour effectuer les migrations
	python manage.py makemigrations
	python manage.py migrate

Création d’une nouvelle application
	
python manage.py startapp aloal



On remarque que la structure du dossier est similaire à celle de base avec un views.py et models.py en plus

Models va servir à créer de nouvelles tables dans la base de donnée

views.py va servir à afficher les fichier html + des fonctions python et relier les 2.
Ne pas oublier d’ajouter le chemin de l’application dans settings.
