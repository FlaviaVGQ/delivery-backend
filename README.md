<h1 align="center"> Sistema Delivery Express </h1>

<p align="center">
    <img src="imagens/logo_delivery.png" alt="Sistema Delivery Express" width="20%" />
</p>

O Sistema Delivery Express é uma plataforma web de delivery projetada para gerenciar e otimizar o processo de pedidos e entregas de restaurantes. A plataforma abrange todas as etapas, desde a criação do cardápio e o acompanhamento dos pedidos pelo restaurante (comerciante) até a experiência de visualização e realização de pedidos pelo cliente.

Este projeto foi desenvolvido no contexto da disciplina de Gerência de Projetos da UEBP, com o objetivo de aplicar conceitos de gestão de atividades e demandas em todas as fases de um projeto, desde sua concepção até a entrega final. O Sistema Delivery Express envolve as seguintes etapas de desenvolvimento:

- Planejamento da ideia
- Elaboração da documentação do projeto
- Uso de ferramentas de gerenciamento e organização das atividades para a equipe
- Configuração das tecnologias utilizadas
- Desenvolvimento completo do Frontend, Backend e integração com o banco de dados

## Status
Finalizado.

## Repositórios

- Frontend : https://github.com/FlaviaVGQ/delivery-frontend
- Backend : https://github.com/FlaviaVGQ/delivery-backend

## Tecnologias e ferramentas envolvidas

Para o desenvolvimento do Backend, foram utilizadas as seguintes tecnologias e ferramentas:

- Python
- Django

## Banco de Dados

O banco de dados escolhido foi:

- PostgreSQL

<h1 align="center"> Guia de Instalação e Execução </h1>

Este guia tem como objetivo fornecer instruções passo a passo para configurar o ambiente de desenvolvimento e executar o Sistema Delivery Express em sua máquina local. Siga as instruções abaixo para garantir que tudo esteja corretamente configurado.


<h2 align="center"> Pré-requisitos de instalação necessários </h2>

### Instalando o Python

1. Abra o terminal e execute os seguintes comandos para instalar o Python 3.x (recomendado 3.8 ou superior):

sudo apt update
sudo apt install python3 python3-pip python3-venv

2. Verifique a instalação executando:

python3 --version

### Instalando o PostgreSQL

1. Instale o PostgreSQL com os comandos abaixo:

sudo apt update
sudo apt install postgresql postgresql-contrib

2. Após a instalação, inicie o serviço:

sudo systemctl start postgresql

3. Verifique se o serviço está ativo:

sudo systemctl status postgresql

4. Acesse o PostgreSQL como superusuário:

sudo -i -u postgres

5. Crie um usuário para o banco de dados: (Exemplo: Escolha um nome de usuário e se deseja que ele seja um superusuário.)

createuser --interactive

6. Configure uma senha para o usuário:

psql
ALTER USER seu_usuario WITH PASSWORD 'sua_senha';
\q

7. Crie um banco de dados:

createdb delivery_bd -O seu_usuario


### IDE de Desenvolvimento
Para executar o projeto, é importante utilizar uma IDE de sua preferência. Abaixo está a IDE utilizada pela equipe durante o desenvolvimento:

 * PyCharm Community: https://www.jetbrains.com/pycharm/


<h2 align="center"> Passos para Configuração do Projeto em sua Máquina Local </h2>
Você pode configurar o projeto de 2 formas pelo arquivo .ZIP OU pelo link do GitHub.

### Descompactando o Projeto pelo arquivo .ZIP

1. Realize o download da pasta (LINK PASTA)
2. Localize o arquivo ZIP do projeto no seu computador.
3. Clique com o botão direito no arquivo e selecione a opção Extrair ou Extrair aqui, dependendo do seu sistema operacional.
4. Após a descompactação, você verá uma pasta (NOME PASTA) contendo todos os arquivos do projeto.

### Abrindo o Projeto na IDE
Você pode abrir o projeto em sua IDE de preferência de 2 formas :

1.  * Abra a sua IDE de escolha (por exemplo, Visual Studio Code, PyCharm, etc.).
    * No menu da IDE, selecione a opção Abrir pasta ou Open Folder.
    * Navegue até a pasta do projeto descompactado e clique em Abrir.

2.  * Clique com o botão direito na pasta que foi descompactada
    * E clique em "Abrir com" e selecione a sua IDE de preferência

### Configurando o Projeto pelo link do GitHub

1. Abra o terminal ou prompt de comando da sua IDE.
2. Execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/FlaviaVGQ/delivery-backend.git
 ```
3. Navegue até o diretório do projeto:

cd delivery-backend


<h2 align="center"> Instalando as Dependências do Projeto </h2>

1. Abra o terminal da sua IDE de preferência
2. Certifique-se de estar no diretório do projeto.
3. Crie um ambiente virtual:

python3 -m venv venv
source venv/bin/activate

4. Instale as dependências listadas em requirements.txt:

```bash
pip install -r requirements.txt
 ```

<h2 align="center"> Configurando o Banco de Dados </h2>

### Crie o Banco de Dados

1. Abra o pgAdmin ou o terminal do PostgreSQL.
2. Clique em Servers
3. O postgres pede para inserir os dados do login no qual você configurou na hora da instalação
4. Clique com o botão direito em Databases e selecione Create > Database
5. Insira o nome  **delivery_bd** no campo DataBase e clique em Save.

### Configuração do banco de dados no Django:

1. No diretório do projeto, localize a pasta **delivery** e abra o arquivo **settings.py**
2. Encontre a seção **DATABASES** e configure as informações do banco de dados de acordo com as configurações locais que você configurou na instalação (usuário, senha, host, etc.):

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'delivery_bd',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': 'sua_porta (geralmente é 5432)',
    }
}
 ```

### Sincronizando o Banco de Dados com o Django

1. Abra o terminal da sua IDE.
2. Execute os seguintes comandos para criar as tabelas necessárias em seu banco de dados:


```bash
python3 manage.py makemigrations
python3 manage.py migrate
 ```

<h2 align="center"> Iniciando o Servidor </h2>

Agora que o banco de dados está configurado e sincronizado, é hora de iniciar o servidor.

1. Execute o comando abaixo para rodar o servidor local:

```bash
python3 manage.py runserver
 ```

<h2 align="center"> Conclusão </h2>

Agora você deve ter o Sistema Delivery Express rodando localmente na sua máquina. Se precisar de mais informações ou ajuda com a configuração, entre em contato com algum integrante do projeto.

### Integrantes:
* [Flávia Vitória](https://github.com/FlaviaVGQ)
* [Helânio Renê](https://github.com/helaniobf)
* [Maria Luiza](https://github.com/LuizaLLeite)









