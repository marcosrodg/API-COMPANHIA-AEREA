 # :airplane: API-COMPANHIA-AEREA :airplane: <br />
RestAPI criada em flask para venda de passagens aereas por uma companhia <br />


* ## Preparando o Ambiente para a Execucao da Api


Clone ou faça o Download do repositorio em uma pasta em sua maquina
abra a pasta raiz da aplicação em um editor de texto de sua preferência e execute os comandos:

Antes de qualquer coisa **certifique que tenha o python3 instaldo em sua maquina** executando o camando ``$ python3 --version`` (linux), caso não tenha siga as instruções do <www.python.org/downloads/>.


Após a instalação do python digite os comandos:

``$ python3 -m venv .venv``


``$ source .venv/bin/activate``


``$ pip install requirements.txt``


**PARA EXECUÇÃO EM localhost:5000** padrão flask

``$ flask run``


**PARA EXECUÇÃO EM 0.0.0.0:<port docker>** 
 
 
Caso não tenha o docker na maquina host instale o Docker em : <https://docs.docker.com/get-docker/> .

 
Crie uma conta no Docker Hub <https://hub.docker.com/> .
 
 
Na pasta raiz do projeto execute as instruções:

 
``$ docker pull python:3.9.9-bullseye``
 
 
``$ docker build -t flask-app:dev-0.0.1 .``
 
 
``$ docker run -d -P flask-app:dev-0.0.1``
 

Verifique a execução do conteiner:

``$ docker ps``

Caso seu conteiner estiver executando corretamente copie a porta de execução para consumir a Api.

 
 
* ## Consumindo Api
 

### Usando o Postman para fazer requisições


Instale o Postman  em <www.postman.com/downloads/> .Após isso crie um 'workspace' e crie as seguintes rotas:

 * ``URL:5000/register``
  

* ``URL:5000/login``


* ``URL:5000/logout``
  

* ``URL:5000//airport/from/<prefix_airport>``

  
* ``URL:5000/airport/destination/<prefix_airport>``
  
  
* ``URL:5000/airports``
  
  
* ``URL:5000/airports/<prefix_from>``
  
  
* ``URL:5000/flight``
  
  
* ``URL:5000/flight/sale``
  
  
* ``URL:5000/tickets``
  
  
* ``URL:5000/user/tickets``
 
  
* ``URL:5000/flight/tickets``

Agora basta seguir as '**Instruções de Uso**' para fazer as requisições.


**ATENÇÃO: Configure as variaveis de ambiente .**
 
 Crie um arquivo '.env' na raiz da aplicacao, com as seguintes variaveis:
 

|**.env**                                         |
|-------------------------------------------------|
|    SQLALCHEMY_DATABASE_URI='sqlite:///banco.db' |
|    SQLALCHEMY_TRACK_MODIFICATIONS=False         |
|    JWT_SECRET_KEY='YourSecretKey'               |
|    JWT_BLACKLIST_ENABLED=True                   | 



* # Instruções de Uso

Este documento explicita com exemplos, como utilizar os recursos disponíveis no FLASK API de login, acesso de dados, e registro. Assim como, as formas de se realizar uma requisição e suas possíveis respostas.

## 1. Registro:


***Requisição***
 
Exemplo de Requisição cadastrar um novo usuário.

|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /register                       | 



|**Header**         |                            |
|-------------------|----------------------------|
|  Content-Type     |  application/json          | 


|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
      {
      "id":"11111111111",
      "name":"Teste Api",
      "email":"documentacao@email.com", 
      "password":"secret"
      }
  ```
  

***Resposta***


Como resposta, obtém-se uma mensagem de sucesso informado que usuário foi criado, e status code 201 Created (Criado).


|**Status**         | **Response Body**                                   |
|-------------------|-----------------------------------------------------|
|  201 Created      |  ```{"mensage":"User created successfully"} ```     | 



***Requisição***
 
Exemplo de Requisição cadastrar outro usuario com id e/ou email ja existentes.

|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /register                 | 



|**Header**         |                            |
|-------------------|----------------------------|
|  Content-Type     |  application/json          | 


|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
      {
      "id":"11111111111",
      "email":"documentacao@email.com", 
      "password":"secret"
      }
  ```
  

***Resposta***


Como resposta, obtém-se uma mensagem de erro, informando que o usuário ja existe.

Caso ja exista usuario cadastrado com tais dados:


|**Status**             | **Response Body**                                                                      |
|-----------------------|----------------------------------------------------------------------------------------|
|  400 Bad Request      |  ```{"mensage": "User already exist"} ```                   |


## 2. Login de Usuário


***Requisição***


Exemplo de Requisição logar com um usuário.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /login                          | 


|**Header**         |                            |
|-------------------|----------------------------|
|  Content-Type     |  application/json          | 


|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```{
    "id":138225688607,
    "password":"revela123"
}
  ```
  
***Resposta***


Como resposta, obtém-se uma mensagem o token de acesso que será necessário para fazer as requisições que só podem ser feitas com login ou pode ocorrer algum erro do servidor ao gerar o token.



|**Status**             | **Response Body**                                                                      |
|-----------------------|----------------------------------------------------------------------------------------|
|  200 OK               |  ```{"access_token": "                                 eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw"} ```                                 | 
| 500 INTERNAL SERVER ERROR | ```{'mensage':'Login Failed:Internal Server Error '}```                            |         


***Requisição***


Exemplo de Requisição para tentar fazer login com um usuário que não existe..


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /login                          | 


|**Header**         |                            |
|-------------------|----------------------------|
|  Content-Type     |  application/json          | 


|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
      {
      "id":"id_inexistente",
      "password":"secret or Incorrect"
      }
  ```
  

***Resposta***


Como resposta, obtém-se uma mensagem de erro 401 não autorizado, informando que cpf ou email estão incorretos.



|**Status**             | **Response Body**                 |
|-----------------------|-----------------------------------|
|  401 UNAUTHORIZED     | ```{"mensage": "Login Failed"}``` |

## 3. Logout de Usuário


***Requisição***


Exemplo de Requisição logout com um usuário.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /logout                          | 


|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw  ```       | 

***Resposta***
Como resposta, obtém-se uma mensagem que o usuario foi deslogado, ou tocken expirado ou token invalido
  
|**Status**                 | **Response Body**                                                                      |
|---------------------------|----------------------------------------------------------------------------------------|
| 200 OK                    | ```{"mensage": "User logged out"} ```                                                  | 
| 422 UNPROCESSABLE ENTITY  | ```{"msg": "Invalid payload string:....." }```                                         | 
  
  
## 4. Adicionando um Aeroporto de origem e Aeroporto de destino 


***Requisição***


Exemplo da URL para Adicionar & Deletar um Aeroporto de origem.


|**Method**     | **URL**                          |
|---------------|----------------------------------|
|   POST        |  /airport/from/udi               |
|   DELETE      |  /airport/from/udi               | 
  

 **udi** = Prefixo do aeroporto que deseja adicionar, ex: ( confins = CFN, guarulhos = SGBR)
 
:no_entry: ATENCAO: Deletando um Aeroporto caso ele tenha voos, os voos serao deletados automaticamente
  
Exemplo da URL para Adicionar & Deletar um Aeroporto de destino.


|**Method**     | **URL**                          |
|---------------|----------------------------------|
|   POST        |  /airport/destination/cfn        |
|   DELETE      |  /airport/destination/udi               | 

 **cfn** = Prefixo do aeroporto que deseja adicionar, ex: ( confins = CFN, guarulhos = SGBR)
 
 :no_entry: ATENCAO: Deletando um Aeroporto caso ele tenha voos, os voos serao deletados automaticamente
  
  
|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw ```        | 
  

BODY: Necessario apenas para o metodo POST
  
|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
      {
    "name":"udi air",
    "city":"uberlandia",
    "state":"mg",
    "zone":0
}
  ```
  
  
**zone** = Indica a zona de trafego do aeroporto, veja a tabela abaixo:
  
|**zone**     | **trafego**                                                                   |
|-------------|-------------------------------------------------------------------------------|
|   0         |  Os voos desse aeroporto faz voos para TODOS aeroporto de todas as zonas      |
|   1         |  Os voos desse aeroporto faz voos APENAS aeroportos de mesma zona             |
|   X         |  Os voos desse aeroporto faz voos APENAS aeroportos de mesma zona X           |
  
  
  
***Resposta***
Como resposta, obtém-se o json de confirmacao dos dados
  
|**Status**                 | **Response Body**                                                                      |
|---------------------------|----------------------------------------------------------------------------------------|
| 201 CREATED               | ```"mensage": { _json com os dados informados_ }   ```                                 | 
| 501 INTERNAL SERVER ERROR | ```{"mensage":"Fail to save Airport"}```                                               | 
| 400  BAD REQUEST          | ```{"mensage":f"Airport prefix {prefix_airport} already exists"}```                    | 
 

## 5. Adicionando um Voo 


***Requisição***


Exemplo da URL para Adicionar um Aeroporto de origem.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   POST      |  /flight                         | 
  

|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw  ```      | 
  
  
|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
     {
    "air_from_prefix":"udi",
    "air_destination_prefix":"cgn",
    "seats":520,
    "date":"03-04-2022",
    "price": 750.55
}
  ```


***Resposta***
Como resposta, obtém-se o json de confirmacao dos dados
  
|**Status**                 | **Response Body**                                                                      |
|---------------------------|----------------------------------------------------------------------------------------|
| 201 CREATED               | ```"mensage": { _json com os dados informados_ }   ```                                 | 
| 501 INTERNAL SERVER ERROR | ```{"mensage":"Fail to save Airport"}```                                               | 
| 400  BAD REQUEST          | ```{"mensage":"Origin or Destination not found or not in the flight zone "}```         |
| 400  BAD REQUEST          | ```{"mensage":""mensage":"impossible flight with same origin and destination" "}```    |
  
 
  
## 6.Buscar promocoes de voos usando parametros de busca

***Requisição***

|**Method**   | **URL**                                                             |
|-------------|---------------------------------------------------------------------|
|   GET       |  /flight/sale?tickets=30&from=cgn&destination=udi                   | 


|**Params**         |                                           |
|-------------------|-------------------------------------------|
|  tickets          |  quantidade de tickets                   |
|  from             |  prefixo do aeroporto de origem           |
|  destination      |  prefixo do aeroporto de destino          |


***Resposta***

Exemplos de Respostas: pUma lista de voos ou voo nao encontrado

|**Status**             | **Response Body**                                                       |
|-----------------------|-------------------------------------------------------------------------|
|  200 OK               | ``` lista com voos encontrados e como desconto aplicado no preco```     |
|  404 NOT FOUND        | ``` {"mensage":"no flights found"}```                                     |


 ## 7. Listando os aeroportos cadastrados


***Requisição***


Exemplo da URL para listar todos  Aeroporto que a companhia aerea trabalha.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   GET       |  /aeroports                      | 
  

|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw  ```      | 


***Resposta***
  
|**Status**             | **Response Body**                                                       |
|-----------------------|-------------------------------------------------------------------------|
|  200 OK               | ``` lista com aeroportos encontrados ```                                |
|  404 NOT FOUND        | ``` {"mensage":"no aeroports found"}```                                 |
  
 
 ## 8. Listando os aeroportos de destino apartir de um aeroporto de origem informado


***Requisição***


Exemplo da URL para Listar aeroportos de destino apartir de um Aeroporto de origem.


|**Method**   | **URL**                              |
|-------------|--------------------------------------|
|   GET       |  /aeroports/< prefixo do aeroporto>  | 
  


***Resposta***
  O retorno sera uma lista de aeroportos de destino encontrada,lista vazia caso nao seja encontrado nenhum,
  ou 'not found' caso o aeroporto de origem informao nao exista na base de dados de origem
  
|**Status**             | **Response Body**                                                       |
|-----------------------|-------------------------------------------------------------------------|
|  200 OK               | ``` lista com aeroportos encontrados ```                                |
|  404 NOT FOUND        | ``` {"mensage":"Airport not found"}```                                  |
  
 

 ## 9. Fazendo reserva de um ticket(s) em um determiado

***Requisição***


Exemplo da URL para Adicionar um Aeroporto de origem.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|  POST       |  /tickets                        | 
  

  
 EX de header:
  
|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw ```        | 

  
REQUEST BODY: Informamos o ID do voo onde desejamos realizar a reserva. As posicoes de cada assento. E a quantidade de Assentos
  
  
|**Request Body**                                                                        |
|----------------------------------------------------------------------------------------|
 ```json 
 {
    "id_flight": 3,
    "seat":"230, 201, 15",
    "quantity":3
}
  ```
  

***Resposta***
  
|**Status**             | **Response Body**                                                                                                |
|-----------------------|------------------------------------------------------------------------------------------------------------------|
|  200 OK               | ``` lista com todos os tickets comprados com sucesso, e o valor final da compra```                               |
|  207 MULTI-STATUS     | ``` lista com tickets comprados com sucesso,as posicoes dos assentos que deram erro e o valor final da compra``` |
|  404 NOT FOUND        | ``` Voo nao encontrado ou o numero de assentos diferente da quantidade de tickets informada```                   |
 |  422 UNPROCESSABLE ENTITY | ``` Tocken informado errado```                                                                              |


  
 ## 10. Listando os tickets reservados pelo usuario Logado


***Requisição***


Exemplo da URL para os tickets reservados pelo usuario Logado  na sessão atual.


|**Method**   | **URL**                          |
|-------------|----------------------------------|
|   GET       |  /user/tickets                   | 
  

|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw  ```       | 


***Resposta***
  
|**Status**                 | **Response Body**                                                       |
|---------------------------|-------------------------------------------------------------------------|
|  200 OK                   | ``` lista com tickets encontrados ```                                   |
|  422 UNPROCESSABLE ENTITY | ``` Tocken informado errado```                                          |
 
 

  ## 11. Listando os tickets reservados pelo usuario Logado


***Requisição***


Exemplo da URL para listar os tickets reservados em um determinado voo.


|**Method**   | **URL**                            |
|-------------|------------------------------------|
|   GET       |  /flight/tickets                   | 
  

|**Header**         |                            |
|-------------------|----------------------------|
|  Authorization    |   ```  Bearer                               eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTMxMzg0MywianRpIjoiNWI0ZTJmZTEtN2U0MC00OWI1LWJiMTMtOTBjMjdjZTA4ZmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJjcGYiOiIwMDAwMDAwMDAwMCIsImVtYWlsIjoiZG9jdW1lbnRhXHUwMGU3XHUwMGUzb0BlbWFpbC5jb20ifSwibmJmIjoxNjQxMzEzODQzLCJleHAiOjE2NDEzMTc0NDN9.MLokeR2UG8M-QWxKnfhU_mF7mZJ8zvXs74kMrLLK9__wupRra3_E7SWmSsFlpMuKtddG_QyzFOFo0K4TX3Jkvw  ```       | 


***Resposta***
  
|**Status**                 | **Response Body**                                                       |
|---------------------------|-------------------------------------------------------------------------|
|  200 OK                   | ``` lista com tickets encontrados ```                                   |
|  404 OK                   | ``` o voo nao foi encontrado apartir do id informado```                 |
|  422 UNPROCESSABLE ENTITY | ``` Tocken informado errado```                                          |
