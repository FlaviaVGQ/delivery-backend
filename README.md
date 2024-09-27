# Sistema Delivery Express

O Sistema Delivery Express é uma plataforma web de delivery desenvolvida para gerenciar e otimizar o processo de pedidos e entregas de restaurantes. Ele abrange desde o recebimento do pedido até a entrega ao cliente, integrando funções como gestão de pedidos, rastreamento de entregas e comunicação com o cliente, proporcionando uma experiência eficiente e satisfatória para ambos os lados.

Este projeto foi criado como parte da disciplina de Gerência de Projetos na UEBP, com o objetivo de praticar a gestão de atividades e demandas de um projeto desde o início. Ele envolve todas as etapas de desenvolvimento de um projeto, incluindo:

- Planejamento da ideia
- Elaboração da documentação do projeto
- Uso de ferramentas de gerenciamento e organização das atividades para a equipe
- Configuração das tecnologias utilizadas
- Desenvolvimento completo do Frontend, Backend e integração com o banco de dados

## Status
Em desenvolvimento.

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

## Para conseguir acessar e rodar o projeto
Para rodar o projeto, siga os seguintes passos:

1 - Clone o repositório do GitHub para uma IDE de sua preferência.

2 - Configure o banco de dados: Baixe e instale o PostgreSQL. Em seguida, crie um banco de dados chamado "delivery_bd".

3 - Ajuste as configurações do banco de dados: No projeto, acesse o arquivo "settings.py" e localize a seção DATABASES. Atualize essa seção com as configurações do seu banco de dados local (usuário, senha, host, etc.).

4 - Sincronize o banco de dados:
- No terminal, execute os comandos:
- python manage.py makemigrations
- python manage.py migrate
  
Isso garantirá que o banco de dados esteja sincronizado com os modelos do Django.

5 - Inicie o servidor:
- Após a sincronização, execute o comando:
- python manage.py runserver
  
Isso iniciará o servidor local para o projeto.


Observação: Pode ser necessário instalar dependências adicionais. Para isso, use o comando pip install -r requirements.txt no diretório do Backend, que instalará todas as bibliotecas listadas no arquivo requirements.txt.
