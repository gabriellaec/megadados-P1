from typing import Optional
from fastapi import FastAPI, status, Form, Request
from pydantic import BaseModel, Field
from typing import List
from starlette.responses import RedirectResponse

from fastapi.templating import Jinja2Templates


tags_metadata = [
    {
        "name": "disciplina",
        "description": "disciplinas que está cursando. Incluem nome, nome do professor e notas",
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


templates = Jinja2Templates(directory="templates/")


# precisa colocar pra nao repetir nome !!!
class Disciplina(BaseModel):
    id: int
    name: str  = Field(None, title="Nome da disciplina")
    prof_name: Optional[str] = Field(None, title="Nome do professor")
    notes: str = Field(None, title="Anotações", description="Escreva sobre a disciplina") ########### tem que colocar como classe e lista
    grades:  List[float] = Field([], title="Notas")



disciplinas = [
    {"id": 0, "name": "Megadados", "prof_name": "Ayres", "notes":"Projeto 1", "grades": [9.5]},
    {"id": 1,"name": "cloud", "notes":"Roteiros", "grades": [8.2, 7.8]},
    {"id": 2,"name": "descomp", "prof_name": "Paulo", "notes":"sad", "grades": [9,6,8]}
]

id_num=len(disciplinas)



# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse('index.html', context={'request': request})


# • O usuário pode criar uma disciplina
###################### falta info se é cacheable
@app.post("/criar-disciplina/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar disciplina",
response_description="Adicionando disciplina",
tags=["disciplina"]
)
async def add(request: Request, nome: str = Form(...), nome_prof: Optional[str] = Form(...), notas: str = Form(...)):
    """
    Cria uma disciplina com todos os atributos
    - **nome**:A disciplina tem um nome único (obrigatório)
    - **nome do professor**: A disciplina tem um nome de professor (opcional)
    - **notas**: A disciplina tem um campo de anotação livre (texto)
    """

    global id_num
    new_disciplina = {
                      "id": id_num,
                      "name": nome, 
                      "prof_name": nome_prof, 
                      "notes": notas
                      } 
      
    id_num+=1 
    disciplinas.append(new_disciplina)
    result = disciplinas
    return {"nomes_disciplinas": [d for d in disciplinas]}
    # return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


# • O usuário pode listar as notas de uma disciplina
@app.get("/notas-disciplina/{item_id}",
status_code=status.HTTP_200_OK,
summary="Listar notas de uma disciplina",
response_description="Listando as notas",
tags=["notas"]
)
async def read_item(item_id: int):
     """
     Lê todas as notas de uma disciplina
    - **id**: Identificador da disciplina
    """
     d=disciplinas[item_id]
     return {"notas": d["grades"]}
    

# • O usuário pode listar os nomes de suas disciplinas
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

#################################################
@app.post("/nova-nota/{item_id}",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar Nota",
response_description="Adicionando nota",
tags=["nota"]
)
async def add_grade(request: Request, item_id: int, nota: float = Form(...)):
    """
    Cria uma disciplina com todos os atributos
    - **item_id**: id da disciplina com a nova nota
    - **nota**: Nota a ser adicionada
    """

    
    disciplinas[item_id]["grades"].append(nota)
    return {f"notas de {disciplinas[item_id]['name']}": [d for d in disciplinas[item_id]['grades']]}
    # return templates.TemplateResponse('form.html', context={'request': request, 'result': result})



##################### deu ruim
@app.delete("/delete-disciplina/{item_id}")
def delete_disciplina(item_id: int):
    disciplina = disciplinas[item_id]
    if disciplina is not None:
        disciplinas.pop(disciplina)

    # url = '/nomes-disciplinas/'
    # response = RedirectResponse(url=url)
    return disciplinas



# @app.get("/criar-disciplina/")
# def form_post(request: Request):
#     result = disciplinas
#     return templates.TemplateResponse('form.html', context={'request': request, 'result': result})



