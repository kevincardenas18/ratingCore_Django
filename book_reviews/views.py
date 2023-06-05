from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def singup(request):

    if request.method == 'GET':
        return render(request, 'singup.html', {
        'form' : UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('successfull')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form' : UserCreationForm,
                    'error': 'El usuario ya existe'
                    }) 
        return render(request, 'singup.html', {
                      'form' : UserCreationForm,
                      'error': 'Las contrasseñas no son iguales'
                      }) 
@login_required
def singout(request):
    logout(request)
    return redirect('home')

@login_required
def welcome(request, user_id):
    #user = User.objects.get(id=user_id)
    #print(user.id)
    return render(request, 'welcome.html')    

def singin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('welcome',user_id=user.id)

@login_required    
def profile(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        # Actualizar los datos del usuario con la información enviada
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        # Mostrar mensaje de éxito
        messages.success(request, 'Los cambios se guardaron correctamente.')

    return render(request, "profile.html", {"user": user})

@login_required
def deleteUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()

    return redirect('/')

def successfull(request):
    return render(request, 'successfull.html')  

@login_required
@user_passes_test(lambda u: u.is_superuser)
def administrador(request):
    return render(request, 'administrador.html')
