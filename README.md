# Cadastro e Listagem de Usuários no Django

## Introdução
Este projeto é uma aplicação Django simples que permite:
- Cadastrar usuários com nome e e-mail
- Listar todos os usuários cadastrados
- Usar um formulário estilizado e um CSS básico

O objetivo é aprender na prática o ciclo completo de Model → Form → View → Template.

---

# Passo a Passo de Como Funciona

## 1. Criar o Model (models.py)

No Django, **Model** é a estrutura que define o formato dos dados que serão armazenados no banco de dados.

```python
from django.db import models  # Importa o módulo de models do Django

# Define a classe Usuario, que representa uma tabela no banco de dados
class Usuario(models.Model):
    nome = models.CharField(max_length=100)  # Cria uma coluna de texto chamada 'nome' com no máximo 100 caracteres
    email = models.EmailField()              # Cria uma coluna específica para armazenar e-mails

    def __str__(self):
        return self.nome  # Define que ao printar o objeto, será mostrado o nome do usuário
```

---

## 2. Criar o Form (forms.py)

**Form** é o componente que cria e valida formulários automaticamente baseado no Model.

```python
from django import forms               # Importa o módulo de formulários do Django
from .models import Usuario             # Importa o modelo Usuario criado no models.py

# Define a classe UsuarioForm baseada no Model Usuario
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario                # Diz ao Django que o formulário será baseado no modelo Usuario
        fields = ['nome', 'email']      # Informa quais campos do modelo serão usados no formulário
```

---

## 3. Criar as Views (views.py)

**Views** são as funções que controlam o que acontece quando o usuário acessa uma URL.

```python
from django.shortcuts import render, redirect  # Importa funções para renderizar páginas e redirecionar
from .models import Usuario                    # Importa o modelo Usuario
from .forms import UsuarioForm                 # Importa o formulário UsuarioForm

# Função que lida com o cadastro de um novo usuário
def cadastrar_usuario(request):
    if request.method == 'POST':                # Se o formulário foi enviado (POST)
        form = UsuarioForm(request.POST)         # Pega os dados enviados e cria um formulário
        if form.is_valid():                      # Verifica se os dados são válidos
            form.save()                          # Salva o novo usuário no banco de dados
            return redirect('listar_usuarios')   # Redireciona para a lista de usuários
    else:
        form = UsuarioForm()                     # Se for apenas acessar a página (GET), cria um formulário vazio
    return render(request, 'cadastrar_usuario.html', {'form': form})  # Renderiza o formulário no template

# Função que lida com a exibição de todos os usuários cadastrados
def listar_usuarios(request):
    usuarios = Usuario.objects.all()             # Pega todos os usuários cadastrados no banco
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})  # Renderiza a lista no template
```

---

## 4. Criar os Templates (HTML)

**Templates** são os arquivos HTML que o Django renderiza para o navegador.

### cadastrar_usuario.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">  
    <title>Cadastro de Usuário</title>
    {% load static %}  <!-- Carrega a funcionalidade de arquivos estáticos (CSS) -->
    <link rel="stylesheet" href="{% static 'style.css' %}">  <!-- Linka o CSS -->
</head>
<body>
    <h1>Cadastrar Usuário</h1>

    <form method="post">  <!-- Cria o formulário com método POST -->
        {% csrf_token %}  <!-- Protege o formulário contra ataques CSRF -->
        {{ form.as_p }}   <!-- Exibe os campos do formulário como parágrafos -->
        <button type="submit">Cadastrar</button>  <!-- Botão para enviar o formulário -->
    </form>

    <a href="{% url 'listar_usuarios' %}">Ver usuários cadastrados</a>  <!-- Link para a lista de usuários -->
</body>
</html>
```

---

### listar_usuarios.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Lista de Usuários</title>
    {% load static %}  <!-- Carrega a funcionalidade de arquivos estáticos -->
    <link rel="stylesheet" href="{% static 'style.css' %}">  <!-- Linka o CSS -->
</head>
<body>
    <h1>Usuários Cadastrados</h1>

    <ul>
        {% for usuario in usuarios %}  <!-- Loop que passa por todos os usuários -->
            <li>{{ usuario.nome }} - {{ usuario.email }}</li>  <!-- Mostra nome e e-mail do usuário -->
        {% empty %}  <!-- Caso não tenha nenhum usuário cadastrado -->
            <li>Nenhum usuário cadastrado ainda.</li>
        {% endfor %}
    </ul>

    <a href="{% url 'cadastrar_usuario' %}">Cadastrar novo usuário</a>  <!-- Link para voltar ao cadastro -->
</body>
</html>
```

---

## 5. Configurar as URLs (urls.py)

As **URLs** conectam o navegador às views corretas.

```python
from django.urls import path  # Importa a função path para criar rotas
from . import views           # Importa as views do projeto

# Define as rotas e quais funções elas devem executar
urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),  # /cadastrar chama a função cadastrar_usuario
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),       # /usuarios chama a função listar_usuarios
]
```

---

## 6. Criar a Estilização Básica (static/style.css)

Este arquivo deixa a página mais agradável visualmente.

```css
body {
    font-family: Arial, sans-serif;  /* Define uma fonte padrão para o site */
    margin: 20px;                    /* Adiciona espaço nas bordas da página */
}

h1 {
    color: #333;                     /* Define a cor do título */
}

form {
    margin-bottom: 20px;              /* Adiciona espaço embaixo do formulário */
}

button {
    padding: 8px 12px;                /* Define tamanho interno do botão */
    background-color: #4CAF50;        /* Define a cor de fundo do botão */
    color: white;                     /* Define a cor do texto do botão */
    border: none;                     /* Remove a borda do botão */
    border-radius: 4px;               /* Deixa as bordas do botão arredondadas */
    cursor: pointer;                  /* Faz o cursor virar uma mãozinha ao passar no botão */
}

a {
    text-decoration: none;            /* Remove o sublinhado dos links */
    color: #4CAF50;                   /* Define a cor dos links */
}
```

---

# Estrutura de Pastas

```bash
seu_app/
├── migrations/                # Arquivos de controle de versões do banco de dados
├── static/                    # Arquivos estáticos (CSS, imagens)
│   └── style.css              # Estilização do site
├── templates/                 # Templates HTML
│   ├── cadastrar_usuario.html
│   └── listar_usuarios.html
├── __init__.py
├── admin.py
├── apps.py
├── forms.py                   # Formulário de usuário
├── models.py                  # Modelo de dados do usuário
├── tests.py
├── urls.py                    # Rotas do app
└── views.py                   # Funções que processam as páginas
```

---

# Resumo Geral

| Arquivo | Função |
|:---|:---|
| models.py | Define o que é um usuário no banco de dados |
| forms.py | Cria e valida o formulário de cadastro |
| views.py | Controla o cadastro e a listagem dos usuários |
| urls.py | Liga as URLs às views corretas |
| templates/ | HTML que o usuário vê no navegador |
| static/ | Arquivos de CSS para estilizar as páginas |

---

# Requisitos para Rodar

- Ter Django instalado (`pip install django`)
- Adicionar o app criado em `INSTALLED_APPS` no `settings.py`
- Criar e aplicar as migrações (`python manage.py makemigrations` e `python manage.py migrate`)
- Rodar o servidor (`python manage.py runserver`)

