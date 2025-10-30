import json
import pandas as pd
import os

VAGA_FILE = 'vaga.json'
CANDIDATOS_FILE = 'dados_extraidos.csv'
RESULTADOS_FILE = 'resultados.json'

def carregar_dados_vaga():
    """Carrega os dados da vaga do arquivo JSON."""
    if os.path.exists(VAGA_FILE):
        try:
            with open(VAGA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def salvar_dados_vaga(vaga_dict):
    """Salva o dicionário da vaga no arquivo JSON."""
    try:
        with open(VAGA_FILE, 'w', encoding='utf-8') as f:
            json.dump(vaga_dict, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo da vaga: {e}")
        return False

def carregar_candidatos():
    """Carrega o DataFrame de candidatos do arquivo CSV."""
    if not os.path.exists(CANDIDATOS_FILE):
        print(f"Erro: Arquivo '{CANDIDATOS_FILE}' não encontrado.")
        return None
    try:
        return pd.read_csv(CANDIDATOS_FILE, sep=';')
    except Exception as e:
        print(f"Erro ao ler o CSV de candidatos: {e}")
        return None

def carregar_resultados():
    """Carrega os resultados da última análise do arquivo JSON."""
    if os.path.exists(RESULTADOS_FILE):
        try:
            with open(RESULTADOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_resultados(resultados_list):
    """Salva a lista de resultados da análise em JSON."""
    try:
        with open(RESULTADOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(resultados_list, f, indent=4, ensure_ascii=False)
        print(f"Resultados da análise salvos em '{RESULTADOS_FILE}'")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de resultados: {e}")