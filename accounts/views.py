from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate

User = get_user_model()

# création d'une page de connexion avec des users

def signup(request):
    if request.method == 'POST':
        #traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username = username,
                                        password = password)
        login(request, user)
        return redirect('index')

    return render(request,'signup.html')

# déconnexion de l'utilisateur : index.html la vue, voir dans urls pour le chemin
def logout_user(request):
    logout(request)
    return redirect('index')

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect('index')



    return render(request, 'login.html')
