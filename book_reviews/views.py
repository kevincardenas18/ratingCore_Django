from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Libro, Autor, Categoria, Review
from django.db.models import Avg, Count, Sum


# Create your views here.
def home(request):
    libros = Libro.objects.annotate(num_comentarios=Count('review')).order_by('-valoracion', '-num_comentarios')[:3]
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

def libro(request):
    libros = Libro.objects.all()
    return render(request, 'libro.html', {'libros': libros})

@login_required
def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)

    # Obtener la instancia de Review del usuario actual para este libro
    usuario = request.user
    review_usuario = Review.objects.filter(libro=libro, usuario=usuario).first()

    comentarios = Review.objects.filter(libro=libro)

    context = {
        'libro': libro,
        'comentarios': comentarios,
        'review_usuario': review_usuario,  # Pasa la instancia de Review del usuario actual al contexto
    }

    return render(request, 'detalle_libro.html', context)

def autor(request):
    autores = Autor.objects.all()
    return render(request, 'autor.html', {'autores': autores})

def detalle_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    return render(request, 'detalle_autor.html', {'autor': autor})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria.html', {'categorias': categorias})

def agregar_categoria(request):
    error = None   
    if request.method == 'POST':
        nombre_categoria = request.POST.get('categoria-name')
        
        try:
            Categoria.objects.create(nombre=nombre_categoria)
            return redirect('lista_categorias')
        except IntegrityError:
            error = 'Ya existe una categoría con ese nombre.'
    
    categorias = Categoria.objects.all()
    
    return render(request, 'categoria.html', {'categorias': categorias, 'error_present': error is not None, 'error': error})

@login_required
def guardar_valoracion(request, libro_id):
    if request.method == 'POST':
        valoracion = int(request.POST['valoracion'])
        libro = get_object_or_404(Libro, pk=libro_id)
        usuario = request.user

        # Verificar si el usuario ya ha dejado una valoración para este libro
        existe_valoracion = Review.objects.filter(libro=libro, usuario=usuario).exists()

        if existe_valoracion:
            # El usuario ya ha dejado una valoración para este libro, actualizar la valoración existente
            review = Review.objects.get(libro=libro, usuario=usuario)
            review.valoracion = valoracion
            review.save()

            # Mostrar mensaje de éxito
            messages.success(request, 'Se ha actualizado tu valoración.')

        else:
            # El usuario no ha dejado una valoración para este libro, crear una nueva valoración
            review = Review(usuario=usuario, libro=libro, valoracion=valoracion)
            review.save()

            # Mostrar mensaje de éxito
            messages.success(request, 'Tu valoración ha sido guardada.')

        #calcular_promedio_valoraciones(libro)  # Calcular y actualizar el promedio de valoraciones
        valoraciones_libro(libro)

        # Redirigir al usuario de vuelta a la página de detalles del libro
        return redirect('detalle_libro', libro_id=libro.id)

@login_required
def guardar_comentario(request, libro_id):
    if request.method == 'POST':
        comentario = request.POST['comentario'].strip()
        libro = get_object_or_404(Libro, pk=libro_id)
        usuario = request.user

        # Verificar si el usuario ha dejado una valoración para este libro
        existe_valoracion = Review.objects.filter(libro=libro, usuario=usuario).exists()

        if not existe_valoracion:
            # El usuario no ha dejado una valoración, mostrar mensaje de error
            messages.error(request, 'Debes dejar una valoración antes de comentar.')
            return redirect('detalle_libro', libro_id=libro.id)

        if not comentario:
            # El usuario no ha ingresado un comentario, mostrar mensaje de error
            messages.error(request, 'Por favor, ingresa un comentario.')
            return redirect('detalle_libro', libro_id=libro.id)

        # Obtener la instancia de Review existente del usuario
        review = get_object_or_404(Review, libro=libro, usuario=usuario)

        # Actualizar el comentario de la instancia de Review
        review.comentario = comentario
        review.save()

        # Mostrar mensaje de éxito
        messages.success(request, 'Se ha ingresado el comentario.')

        # Redirigir al usuario de vuelta a la página de detalles del libro
        return redirect('detalle_libro', libro_id=libro.id)

@login_required
def eliminar_comentario(request, libro_id):
    if request.method == 'POST':
        comentario = request.POST['comentario'].strip()
        libro = get_object_or_404(Libro, pk=libro_id)
        usuario = request.user
        review = get_object_or_404(Review, libro=libro, usuario=usuario)

        # Verificar si el usuario tiene permiso para eliminar el comentario
        if review.usuario == request.user:
            # Actualizar el campo de comentario a null o none
            review.comentario = None
            review.save()

            # Mostrar mensaje de éxito
            messages.success(request, 'El comentario ha sido eliminado.')
        else:
            # El usuario no tiene permiso para eliminar el comentario
            messages.error(request, 'No tienes permiso para eliminar este comentario.')

    return redirect('detalle_libro', libro_id=review.libro.id)


def calcular_promedio_valoraciones(libro):
    promedio = Review.objects.filter(libro=libro).aggregate(promedio=Avg('valoracion'))['promedio']
    libro.valoracion = promedio or 0.00
    libro.save()

def valoraciones_libro(libro):
    reviews = Review.objects.filter(libro=libro)

    suma = 0
    cantidad_registros = 0

    for review in reviews:
        suma += review.valoracion
        cantidad_registros += 1

    promedio = suma / cantidad_registros if cantidad_registros > 0 else 0

    libro.valoracion = promedio
    libro.save()

def top_personalizado(request):
    if not request.user.is_authenticated or not Review.objects.filter(usuario=request.user).exists():
        # Usuario no logueado o sin reviews ingresadas, mostrar top 10
        libros_top = Libro.objects.annotate(num_comentarios=Count('review')).order_by('-valoracion', '-num_comentarios')[:3]
    else:
        categorias = Categoria.objects.all()
        score_1 = 0
        score_2 = 0
        categoria_1 = None
        categoria_2 = None

        for categoria in categorias:
            suma = Review.objects.filter(usuario=request.user, libro__categorias=categoria).aggregate(Sum('valoracion')).get('valoracion__sum', 0)
            cantidad_review = Review.objects.filter(usuario=request.user, libro__categorias=categoria).count()

            if cantidad_review > 0:
                score_categoria = suma / cantidad_review

                if score_categoria > score_1:
                    score_2 = score_1
                    categoria_2 = categoria_1
                    score_1 = score_categoria
                    categoria_1 = categoria.nombre
                elif score_categoria > score_2:
                    score_2 = score_categoria
                    categoria_2 = categoria.nombre
        
        '''
        for categoria in categorias:
            suma = 0
            cantidad_review = Review.objects.filter(usuario=request.user, libro__categorias=categoria).count()

            if cantidad_review > 0:
                for review in Review.objects.filter(libro__categorias=categoria):
                    if review.usuario == request.user :
                        suma += review.valoracion

                score_categoria = suma / cantidad_review

                if score_categoria > score_1:
                    score_2 = score_1
                    categoria_2 = categoria_1
                    score_1 = score_categoria
                    categoria_1 = categoria.nombre
                elif score_categoria > score_2:
                    score_2 = score_categoria
                    categoria_2 = categoria.nombre
        '''

        libros_1 = Libro.objects.filter(categorias__nombre=categoria_1).exclude(review__usuario=request.user).order_by('-valoracion')[:3]
        libros_2 = Libro.objects.filter(categorias__nombre=categoria_2).exclude(review__usuario=request.user).order_by('-valoracion')[:3]

        libros_top = libros_1 | libros_2

    return render(request, 'top_personalizado.html', {'libros_top': libros_top, 'score_1': score_1, 'score_2': score_2, 'categoria_1': categoria_1, 'categoria_2': categoria_2, 'libros_1': libros_1, 'libros_2': libros_2})