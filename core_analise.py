import json
import time
from google.api_core.exceptions import ResourceExhausted
import utils # Importamos nosso novo módulo

def gerar_prompt_analise(candidato, vaga):
    """Gera o prompt formatado para a IA."""
    vaga_texto = json.dumps(vaga, indent=2, ensure_ascii=False)
    candidato_texto = candidato.to_string()

    return f"""
    Aja como um recrutador técnico (Tech Recruiter) sênior e analítico.
    Sua tarefa é analisar um perfil de candidato (extraído de forma bruta) 
    em relação a uma vaga de emprego específica.
    
    **--- VAGA DE EMPREGO ---**
    {vaga_texto}

    **--- PERFIL DO CANDIDATO (Dados Brutos) ---**
    {candidato_texto}

    **--- SUA TAREFA ---**
    Retorne APENAS um objeto JSON válido com os campos "nome", "score" (0-100) e "justificativa".
    """

def analisar_perfil_com_ia(model, candidato, vaga):
    """Envia o prompt para a IA e trata a resposta."""
    prompt = gerar_prompt_analise(candidato, vaga)
    
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)
    except Exception as e:
        print(f"Erro na análise de {candidato['nome']}: {e}")
        return {"nome": candidato['nome'], "score": 0, "justificativa": f"Erro inesperado na análise: {e}"}

def executar_analise_completa_e_salvar(model, vaga, df_candidatos):
    """
    Função de longa duração para ser executada em background.
    Executa a análise e salva o resultado no final.
    """
    resultados_analise = []
    total_candidatos = len(df_candidatos)
    print(f"\nIniciando análise em background de {total_candidatos} perfis...")

    for index, candidato in df_candidatos.iterrows():
        print(f"  Analisando [{index + 1}/{total_candidatos}]: {candidato['nome']}...")
        
        resultado = analisar_perfil_com_ia(model, candidato, vaga)
        resultado['url'] = candidato.get('url', 'Não encontrada') 
        resultados_analise.append(resultado)
        
        time.sleep(2) # Evitar limites de taxa da API
    
    print("...Análise em background concluída.")
    
    resultados_ordenados = sorted(resultados_analise, key=lambda x: x['score'], reverse=True)
    
    # Salva os resultados em um arquivo que o frontend pode buscar
    utils.salvar_resultados(resultados_ordenados)
    