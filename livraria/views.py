import imghdr  # biblioteca nova

from django.shortcuts import get_object_or_404, redirect, render

from livraria.forms import LivroForm
from livraria.models import Autor, Categoria, Livro

def buscar_livro(request):
    infor = request.POST['infor']
    livros = Livro.objects.filter(nome__contains=infor)
    return render(request, 'livraria/pages/listar_livros.html', {'livros':livros})

def editar_livro(request, id):
    livro = get_object_or_404(Livro, pk=id)
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            livro = form.save(commit=False)
            form.save()
            return redirect('detalhar_livro', id=livro.id)
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livraria/pages/editar_livro.html', {'form': form})

def cadastrar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            img = request.FILES
            dados_img = imghdr.what(img['imagem'])
            if dados_img == 'png' or dados_img == 'jpeg':
                form.save()
                return redirect('detalhar_livro', id=livro.id)
            else:
                form = LivroForm()
                return render(request, 'livraria/pages/editar_livro.html', {'form': form})             
    else:
        form = LivroForm()
    return render(request, 'livraria/pages/editar_livro.html', {'form': form})

def detalhar_livro(request, id):
    livro = get_object_or_404(Livro, pk=id)
    return render(request, 'livraria/pages/detalhar_livro.html', {'livro':livro})

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'livraria/pages/listar_categorias.html', {'categorias':categorias})

def listar_autores(request):
    autores = Autor.objects.all()
    return render(request, 'livraria/pages/listar_autores.html', {'autores':autores})

def listar_livros(request):
    livros = Livro.objects.all()
    return render(request, 'livraria/pages/listar_livros.html', {'livros':livros})

#definições de login
from django.contrib.auth import authenticate, login, logout

def page_login(request):
    return render(request, 'livraria/pages/login.html',{})

def logout_usuario(request):
    logout(request)
    return render(request, 'livraria/pages/login.html',{})

def autenticar_usuario(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        livros = Livro.objects.all()
        return render(request, 'livraria/pages/listar_livros.html', {'livros':livros})
    else:
        return render(request, 'livraria/pages/login.html',{})