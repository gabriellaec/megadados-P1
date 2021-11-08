from typing import Optional
from fastapi import FastAPI, status, Form, Request, HTTPException
from fastapi.param_functions import Path
from pydantic import BaseModel, Field
from typing import List, Dict
from starlette.responses import RedirectResponse


tags_metadata = [
    {
        "name": "disciplina",
        "description": "disciplinas que está cursando. Incluem nome, nome do professor, anotações e notas",
    },
    {
        "name": "notas",
        "description": "Conjunto de notas de cada matéria.",
    },
]

description = """
    Microsserviço de controle de notas para um App para gerenciar disciplinas 🚀
    Permite:
       - Criar disciplinas e notas
       - Consultar informações de cada disciplina
       - Alterar disciplinas e notas
       - Deletar disciplinas e notas
    

    Alunos: Gabriella Cukier e Manuel Castanares
"""


app = FastAPI(
    title="Minhas Disciplinas",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)



class Nota(BaseModel):
    disciplina: str  = Field(None, title="Nome da disciplina")
    titulo: str  = Field(None, title="Título")
    descricao: str = Field(None, title="Nota")


class Disciplina(BaseModel):
        id: int
        name: str  = Field(None, title="Nome da disciplina")
        prof_name: Optional[str] = Field(None, title="Nome do professor")
        anotacoes: List[Nota] = Field(None, title="Anotações", description="Escreva sobre a disciplina")


disciplinas = [
    {"id": 0, "name": "Megadados", "prof_name": "Ayres", "anotacoes": [{"titulo": "Proj1", "nota": "indo"}]},
    {"id": 1,"name": "cloud", "anotacoes": [{"titulo": "h1", "nota": "acabei:"}, {"titulo": "h3", "nota": "precisa acabar"}]},
    {"id": 2,"name": "descomp", "prof_name": "Paulo", "anotacoes": [{"titulo": "P1", "nota": "já foi"}, {"titulo": "P2", "nota": "será"}]}
]

id_num=len(disciplinas)


#---------------------------------------------------#
#    	             Disciplinas    	            #
#---------------------------------------------------#
#####################################################
# • O usuário pode criar uma disciplina
#####################################################
@app.post("/disciplina/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar disciplina",
response_description="Adicionando disciplina",
tags=["disciplina"]
)
async def add(nome: str = Form(...), nome_prof: Optional[str] = Form(None)):
    """
    Cria uma disciplina com todos os atributos
    - **nome**: A disciplina tem um nome único (obrigatório) 
    - **nome do professor**: A disciplina tem um nome de professor (opcional)
    - **anotacoes**: A disciplina tem um campo de anotação livre (texto) - inicialmente vazio

    Nova disciplina criada com nome, nome do professor e anotações
    - **cached**: False
    """

# Garantindo que o nome da disciplina é único
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Disciplina já existe")
    
    global id_num
    new_disciplina = {
                      "id": id_num,
                      "name": nome, 
                      "prof_name": nome_prof, 
                      "anotacoes": []
                      } 
      
    id_num+=1 
    disciplinas.append(new_disciplina)
    return {"nomes_disciplinas": [d for d in disciplinas]}


######################################################
# • O usuário pode listar os nomes de suas disciplinas
######################################################
@app.get("/disciplina/",
status_code=status.HTTP_200_OK,
summary="Listar os nomes das disciplinas",
response_description="Listando as disciplinas",
tags=["disciplina"]
)
async def show():
    """
     Lê todos os nomes das disciplinas existentes
    """
    print(disciplinas)
    return {"nomes_disciplinas": [d["name"] for d in disciplinas]}



##################################################################################
#U • O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
##################################################################################
@app.put("/disciplina/", 
status_code=status.HTTP_200_OK,
summary="Atualizar disciplina",
response_description="Atualizando disciplina",
tags=["disciplina"]
)
async def update(nome_disciplina: str = Form(...), novo_nome_disciplina: Optional[str] = Form(None), nome_prof: Optional[str] = Form(None)):
    """
    Atualiza as informações de uma determinada disciplina
    - **nome_disciplina**: A disciplina que será alterada
    - **novo_nome_disciplina**: Novo nome que a disciplina receberá
    - **nome_prof**: Novo nome do professor que se deseja alterar
    """
  
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

    nome_prof_old = disciplinas[item_id]["prof_name"]
    anotacoes = disciplinas[item_id]["anotacoes"]
    id_disciplina = disciplinas[item_id]["id"]


    if nome_prof is None:
        nome_prof=nome_prof_old
    if novo_nome_disciplina is not None:
        nome_disciplina = novo_nome_disciplina
    
    new_disciplina = {
                      "id": id_disciplina,
                      "name": nome_disciplina, 
                      "prof_name": nome_prof, 
                      "anotacoes": anotacoes
                      } 
      
    disciplinas[item_id]=new_disciplina
    return disciplinas


##############################################
### • O usuário pode deletar uma disciplina
##############################################
@app.delete("/disciplina/",
status_code=status.HTTP_200_OK,
summary="Deletar disciplina",
response_description="Deletando disciplina",
tags=["disciplina"]
)
def delete_disciplina(nome_disciplina: str = Form(...)):
    """
    Deleta uma disciplina
    - **nome_disciplina**: Nome da disciplina que será deletada
    """
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Se ela existe, encontra sua posição na lista
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

# Remove a disciplina
    disciplina = disciplinas[item_id]
    if disciplina is not None:
        disciplinas.pop(item_id)
    return disciplinas


#---------------------------------------------------#
#    	                 Notas    	                #
#---------------------------------------------------#
#######################################################
#C • O usuário pode adicionar uma nota a uma disciplina
#######################################################
@app.post("/disciplina/{nome_disciplina}/notas",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar Nota",
response_description="Adicionando nota",
tags=["notas"]
)
async def add_note(nome_disciplina: str = Path(..., title="nome da disciplina"), titulo: str = Form(...), nota: str = Form(...)):
    """
    Cria uma nota com todos os atributos
    - **nome_disciplina**: nome da disciplina com a nova nota
    - **titulo**: titulo da nota 
    - **nota**: Nota a ser adicionada


    Nova nota criada com título e anotações
    - **cached**: False
    """
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

    v = {"titulo": titulo,
          "nota": nota }
    disciplinas[item_id]["anotacoes"].append(v)
    return {f"notas de {disciplinas[item_id]['name']}": [d for d in disciplinas[item_id]['anotacoes']]}



#####################################################
#R • O usuário pode listar as notas de uma disciplina
#####################################################
@app.get("/disciplina/{nome_disciplina}/notas",
status_code=status.HTTP_200_OK,
summary="Listar notas de uma disciplina",
response_description="Listando as notas",
tags=["notas"]
)
async def read_item(nome_disciplina: str = Path(..., title="nome da disciplina")):
     """
     Lê todas as notas de uma disciplina
    - **nome_disciplina**: Nome da disciplina em que estão as notas
    """
     if not any(d["name"]==nome_disciplina for d in disciplinas):
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
     for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i
    
     
     d=disciplinas[item_id]
     return {"notas": d["anotacoes"]}
    


##########################################################
#U • O usuário pode modificar uma nota de uma disciplina
##########################################################
@app.patch("/disciplina/{nome_disciplina}/notas", 
status_code=status.HTTP_200_OK,
summary="Atualizar nota",
response_description="Atualizando nota",
tags=["notas"]
)
async def update(nome_disciplina: str = Path(..., title="nome da disciplina"), nome_titulo: str = Form(...), nova_nota: str = Form(...)):
    """
    Atualiza uma nota de determinada matéria
    - **nome_disciplina**: A disciplina cuja nota vai ser alterada
    - **nome_titulo**: O título da nota a ser alterada
    - **nova_nota**: A nova nota a ser salva
    """
  
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i
    
# Checa se nota daquela titulo existe
    if not any(d["titulo"]==nome_titulo for d in disciplinas[item_id]["anotacoes"]):
            raise HTTPException(status_code=404, detail="titulo não encontrado")  

# Encontra a titulo e modifica a nota
    for d in range(len(disciplinas[item_id]["anotacoes"])):
        if disciplinas[item_id]["anotacoes"][d]["titulo"] == nome_titulo:
           disciplinas[item_id]["anotacoes"][d]["nota"] = nova_nota
    
    return disciplinas



#######################################
#D • O usuário pode deletar uma nota
#######################################
@app.delete("/disciplina/{nome_disciplina}/notas",
status_code=status.HTTP_200_OK,
summary="Deletar nota",
response_description="Deletando nota",
tags=["notas"]
)
def delete_nota(nome_disciplina: str = Path(..., title="nome da disciplina"), nome_titulo: str = Form(...)):
    """
    Deleta uma nota de determinada matéria
    - **nome_disciplina**: A disciplina em que a nota a ser deletada está
    - **nome_titulo**: O título cuja nota se deseja deletar
    """
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

# Checa se nota daquela titulo existe
    if not any(d["titulo"]==nome_titulo for d in disciplinas[item_id]["anotacoes"]):
            raise HTTPException(status_code=404, detail="titulo não encontrado")  

# Encontra a titulo e a deleta
    for d in range(len(disciplinas[item_id]["anotacoes"])):
        if disciplinas[item_id]["anotacoes"][d]["titulo"] == nome_titulo:
            titulo_id=d
    titulo = disciplinas[item_id]["anotacoes"][titulo_id]
    if titulo is not None:
        (disciplinas[item_id]["anotacoes"]).pop(titulo_id)

    return disciplinas
