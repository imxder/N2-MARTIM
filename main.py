from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import utils
import config
import core_analise

# Inicializa o app FastAPI
app = FastAPI(
    title="Avaliador de Perfis API",
    description="API para gerenciar vagas e analisar candidatos."
)

# Carrega o modelo de IA na inicialização
model_ia = config.configurar_ia()
if model_ia is None:
    print("ERRO CRÍTICO: Não foi possível carregar o modelo de IA. A API será encerrada.")
    exit()

# --- ENDPOINTS DA API ---

@app.get("/api/vaga", tags=["Vaga"])
def get_vaga():
    """Retorna os dados da vaga atualmente salva em vaga.json."""
    return utils.carregar_dados_vaga()

@app.post("/api/vaga", tags=["Vaga"])
def post_vaga(vaga_data: dict = Body(...)):
    """
    Recebe um objeto JSON e salva como a nova vaga em vaga.json.
    Espera um body como:
    {
        "titulo": "...",
        "grau_escolaridade": "...",
        "tempo_experiencia": "...",
        "conhecimentos_obrigatorios": ["C#", ".NET"],
        "conhecimentos_desejados": ["Azure"],
        "observacoes": "..."
    }
    """
    if utils.salvar_dados_vaga(vaga_data):
        return {"status": "sucesso", "mensagem": "Vaga salva!"}
    raise HTTPException(status_code=500, detail="Erro ao salvar a vaga.")

@app.post("/api/analisar", tags=["Análise"])
def iniciar_analise(background_tasks: BackgroundTasks):
    """
    Inicia o processo de análise em background.
    Retorna imediatamente.
    """
    print("Requisição de análise recebida.")
    vaga = utils.carregar_dados_vaga()
    candidatos_df = utils.carregar_candidatos()

    if not vaga or not vaga.get("titulo"):
        raise HTTPException(status_code=400, detail="Vaga não cadastrada. Salve uma vaga primeiro.")
    if candidatos_df is None:
        raise HTTPException(status_code=400, detail="Arquivo 'dados_extraidos.csv' não encontrado.")

    # Adiciona a tarefa pesada para rodar em background
    background_tasks.add_task(
        core_analise.executar_analise_completa_e_salvar,
        model_ia, 
        vaga, 
        candidatos_df
    )
    
    # Responde imediatamente ao usuário
    return {"status": "iniciado", "mensagem": f"Análise de {len(candidatos_df)} candidatos iniciada em background."}

@app.get("/api/resultados", tags=["Análise"])
def get_resultados():
    """
    Retorna os resultados da última análise salva em resultados.json.
    """
    return utils.carregar_resultados()

# --- SERVIR O FRONTEND ESTÁTICO ---

# Monta o diretório 'public' para servir arquivos estáticos (CSS, JS)
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serve o arquivo HTML principal da interface."""
    return FileResponse('public/index.html')

# Para rodar este servidor:
# Salve este arquivo como main.py
# No terminal, execute: uvicorn main:app --reload
