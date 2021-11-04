from typing import Optional
from fastapi import FastAPI, status, Form, Request, HTTPException
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
"""


app = FastAPI(
    title="Minhas Disciplinas",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)



class Nota(BaseModel):
    disciplina: str  = Field(None, title="Nome da disciplina")
    prova: str  = Field(None, title="Nome da prova")
    nota: float = Field(None, title="Nota da prova")


class Disciplina(BaseModel):
    id: int
    name: str  = Field(None, title="Nome da disciplina")
    prof_name: Optional[str] = Field(None, title="Nome do professor")
    anotacoes: str = Field(None, title="Anotações", description="Escreva sobre a disciplina") 
    grades: List[Nota] = Field(None, title="Anotações", description="Escreva sobre a disciplina")



disciplinas = [
    {"id": 0, "name": "Megadados", "prof_name": "Ayres", "notes":"Projeto 1", "grades": [{"prova": "PI", "nota": 9.3}]},
    {"id": 1,"name": "cloud", "notes":"Roteiros", "grades": [{"prova": "h1", "nota": 7.8}, {"prova": "h3", "nota": 8.1}]},
    {"id": 2,"name": "descomp", "prof_name": "Paulo", "notes":"?", "grades": [{"prova": "P1", "nota": 8.4}, {"prova": "P2", "nota": 10.0}]}
]

id_num=len(disciplinas)



#---------------------------------------------------#
#    	             Disciplinas    	            #
#---------------------------------------------------#
#####################################################
# • O usuário pode criar uma disciplina
#####################################################
@app.post("/criar-disciplina/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar disciplina",
response_description="Adicionando disciplina",
tags=["disciplina"]
)
async def add(request: Request, nome: str = Form(...), nome_prof: Optional[str] = Form(None), anotacoes: str = Form(...)):
    """
    Cria uma disciplina com todos os atributos
    - **nome**: A disciplina tem um nome único (obrigatório) - 
    - **nome do professor**: A disciplina tem um nome de professor (opcional)
    - **anotacoes**: A disciplina tem um campo de anotação livre (texto)
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
                      "notes": anotacoes,
                      "grades": []
                      } 
      
    id_num+=1 
    disciplinas.append(new_disciplina)
    result = disciplinas
    return {"nomes_disciplinas": [d for d in disciplinas]}



######################################################
# • O usuário pode listar os nomes de suas disciplinas
######################################################
@app.get("/nomes-disciplinas/",
status_code=status.HTTP_200_OK,
summary="Listar os nomes das disciplinas",
response_description="Listando as disciplinas",
tags=["disciplina"]
)
async def show():
    """
     Lê todas os nomes das disciplinas existentes
    """
    print(disciplinas)
    return {"nomes_disciplinas": [d["name"] for d in disciplinas]}




##################################################################################
#U • O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
##################################################################################
@app.put("/update-disciplina/", 
status_code=status.HTTP_200_OK,
summary="Atualizar disciplina",
response_description="Atualizando disciplina",
tags=["disciplina"]
)
async def update(nome_disciplina: str = Form(...), novo_nome_disciplina: Optional[str] = Form(None), nome_prof: Optional[str] = Form(None), anotacoes: Optional[str] = Form(None)):
    """
    Atualiza as informações de uma determinada disciplina
    - **nome_disciplina**: A disciplina que será alterada
    - **novo_nome_disciplina**: Novo nome que a disciplina receberá
    - **nome_prof**: Nome do professor que se deseja alterar
    - **anotacoes**: Novas anotacoes a serem alteradas
    """
  
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

    nome_prof_old = disciplinas[item_id]["prof_name"]
    anotacoes_old = disciplinas[item_id]["notes"]
    grades = disciplinas[item_id]["grades"]
    id_disciplina = disciplinas[item_id]["id"]




    if nome_prof is None:
        nome_prof=nome_prof_old
    if anotacoes is None:
        anotacoes=anotacoes_old
    if novo_nome_disciplina is not None:
        nome_disciplina = novo_nome_disciplina
    
    new_disciplina = {
                      "id": id_disciplina,
                      "name": nome_disciplina, 
                      "prof_name": nome_prof, 
                      "notes": anotacoes,
                      "grades": grades
                      } 
      
    disciplinas[item_id]=new_disciplina
    return disciplinas


##############################################
### • O usuário pode deletar uma disciplina
##############################################
@app.delete("/delete-disciplina/",
status_code=status.HTTP_200_OK,
summary="Deletar disciplina",
response_description="Deletando disciplina",
tags=["disciplina"]
)
def delete_disciplina(nome_disciplina: str = Form(...)):

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
@app.post("/nova-nota/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar Nota",
response_description="Adicionando nota",
tags=["notas"]
)
async def add_grade(nome_disciplina: str = Form(...), prova: str = Form(...), nota: float = Form(..., ge=0, le=10)):
    """
    Cria uma disciplina com todos os atributos
    - **item_id**: id da disciplina com a nova nota
    - **prova**: Prova a qual a nota pertence
    - **nota**: Nota a ser adicionada
    """
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

    v = {"prova": prova,
          "nota": nota }
    disciplinas[item_id]["grades"].append(v)
    return {f"notas de {disciplinas[item_id]['name']}": [d for d in disciplinas[item_id]['grades']]}



#####################################################
#R • O usuário pode listar as notas de uma disciplina
#####################################################
@app.get("/notas-disciplina/{nome_disciplina}",
status_code=status.HTTP_200_OK,
summary="Listar notas de uma disciplina",
response_description="Listando as notas",
tags=["notas"]
)
async def read_item(nome_disciplina: str):
     """
     Lê todas as notas de uma disciplina
    - **id**: Identificador da disciplina
    """
     if not any(d["name"]==nome_disciplina for d in disciplinas):
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
     for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i
    
     
     d=disciplinas[item_id]
     return {"notas": d["grades"]}
    


##########################################################
#U • O usuário pode modificar uma nota de uma disciplina
##########################################################
@app.patch("/update-nota/", 
status_code=status.HTTP_200_OK,
summary="Atualizar nota",
response_description="Atualizando nota",
tags=["notas"]
)
async def update(nome_disciplina: str = Form(...), nome_prova: str = Form(...), nova_nota: float = Form(..., ge=0, le=10)):
    """
    Atualiza uma nota de determinada matéria
    - **disciplina**: A disciplina que teve a prova
    - **prova**: A prova cuja nota se deseja alterar
    - **nota**: A nova nota da prova
    """
  
# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i
    
# Checa se nota daquela prova existe
    if not any(d["prova"]==nome_prova for d in disciplinas[item_id]["grades"]):
            raise HTTPException(status_code=404, detail="Prova não encontrada")  

# Encontra a prova e modifica a nota
    for d in range(len(disciplinas[item_id]["grades"])):
        if disciplinas[item_id]["grades"][d]["prova"] == nome_prova:
           disciplinas[item_id]["grades"][d]["nota"] = nova_nota
    
    return disciplinas



#######################################
#D • O usuário pode deletar uma nota
#######################################
@app.delete("/delete-nota/",
status_code=status.HTTP_200_OK,
summary="Deletar nota",
response_description="Deletando nota",
tags=["notas"]
)
def delete_nota(nome_disciplina: str = Form(...), nome_prova: str = Form(...)):

# Checa se disciplina existe
    if not any(d["name"]==nome_disciplina for d in disciplinas):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# Pega a posição da lista em que a matéria está
    for i in range(len(disciplinas)):
        if disciplinas[i]["name"] == nome_disciplina:
            item_id=i

# Checa se nota daquela prova existe
    if not any(d["prova"]==nome_prova for d in disciplinas[item_id]["grades"]):
            raise HTTPException(status_code=404, detail="Prova não encontrada")  

# Encontra a prova e a deleta
    for d in range(len(disciplinas[item_id]["grades"])):
        if disciplinas[item_id]["grades"][d]["prova"] == nome_prova:
            prova_id=d
    prova = disciplinas[item_id]["grades"][prova_id]
    if prova is not None:
        (disciplinas[item_id]["grades"]).pop(prova_id)

    return disciplinas
