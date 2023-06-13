from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Libro, Autor, Categoria, Review

# Create your views here.
def home(request):
    libros = Libro.objects.all()
    return render(request, 'home.html', {'libros': libros})

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

def autor(request):
    autores = Autor.objects.all()
    return render(request, 'autor.html', {'autores': autores})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)

    comentarios = Review.objects.filter(libro=libro)

    return render(request, 'detalle_libro.html', {'libro': libro, 'comentarios': comentarios})

def detalle_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    return render(request, 'detalle_autor.html', {'autor': autor})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria.html', {'categorias': categorias})

@login_required
def guardar_comentario(request, libro_id):
    if request.method == 'POST':
        comentario = request.POST['comentario']
        libro = get_object_or_404(Libro, pk=libro_id)

        # Verificar si el usuario ya ha dejado un comentario para este libro
        existe_comentario = Review.objects.filter(libro=libro, usuario=request.user).exists()

        if existe_comentario:
            # El usuario ya ha dejado un comentario para este libro, mostrar mensaje de error
            messages.error(request, 'Ya has dejado un comentario para este libro.')
            return redirect('detalle_libro', libro_id=libro.id)

        # Crear una nueva instancia de Review y guardarla en la base de datos
        review = Review(comentario=comentario, usuario=request.user, libro=libro, valoracion=0)
        review.save()

        # Redirigir al usuario de vuelta a la página de detalles del libro
        return redirect('detalle_libro', libro_id=libro.id)

