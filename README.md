# Avaliador de Perfis LinkedIn 

Aplicação de **análise de perfis do LinkedIn com arquitetura desacoplada**, composta por backend em **FastAPI** e frontend em **JavaScript puro**.  
A ferramenta utiliza **Inteligência Artificial (Google Gemini)** para avaliar candidatos com base em dados coletados via **scraping (Selenium)**.

A coleta dos perfis é feita separadamente por um script Python (`busca_candidatos.py`), que gera o arquivo `.csv` usado na análise principal.

---

## Arquitetura do Projeto

O projeto é composto por três partes principais:

### 🔹 Backend (API FastAPI)
- **`main.py`** → Servidor principal da API. Expõe endpoints para salvar vagas, iniciar análises e obter resultados.  
- **`core_analise.py`** → Núcleo de lógica da aplicação, responsável por formatar prompts e interagir com o Google Gemini.  
- **`utils.py`** → Funções auxiliares para manipulação de arquivos (`vaga.json`, `dados_extraidos.csv`, `resultados.json`).  
- **`config.py`** → Carrega as variáveis do `.env` e inicializa o modelo de IA.  

### 🔹 Frontend (Interface do Usuário)
- **`public/index.html`** → Estrutura principal da página web.  
- **`public/app.js`** → Controla toda a interação do usuário e a comunicação com a API.  
- **`public/style.css`** → Define o design e a aparência da interface.  

### 🔹 Coletor de Dados (Script Selenium)
- **`busca_candidatos.py`** → Script Python responsável por coletar informações de perfis do LinkedIn usando um navegador Chrome logado.

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** – Criação do backend e endpoints REST  
- **Uvicorn** – Servidor ASGI para rodar o FastAPI  
- **HTML5 / CSS3 / JavaScript (Vanilla)** – Interface do usuário  
- **Selenium** – Automação e scraping de dados do LinkedIn  
- **Pandas** – Manipulação de dados (CSV)  
- **Google Generative AI (Gemini)** – Análise inteligente dos perfis  
- **Python-Dotenv** – Carregamento seguro de variáveis de ambiente  

---

## Como Executar o Projeto

A execução deve seguir **4 etapas** na ordem correta.

---

### Etapa 1 — Configuração Inicial (Apenas uma vez)

1. **Clone ou baixe o repositório**

   Coloque todos os arquivos em uma pasta local (exemplo: `N2`).

2. **Obtenha sua chave da API do Google Gemini**

   - Acesse o [Google AI Studio](https://aistudio.google.com/).  
   - Faça login com sua conta Google.  
   - Clique em **"Get API key" → "Create API key in new project"**.  
   - Copie a chave gerada.

3. **Crie o arquivo `.env`**

   Na pasta raiz do projeto (`N2`), crie um arquivo chamado **`.env`** com o conteúdo:

   ```
   GOOGLE_API_KEY=SUA_CHAVE_COPIADA_AQUI
   ```

   > **Não use aspas.**  
   > O arquivo `.gitignore` já impede o envio do `.env` ao GitHub.

4. **Crie e ative o ambiente virtual**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

5. **Instale as dependências**

   ```powershell
   pip install -r requirements.txt
   ```

---

### Etapa 2 — Coleta de Dados do LinkedIn (Obrigatória)

Esta etapa gera o arquivo `dados_extraidos.csv` com as informações dos perfis.

1. **Abra o Chrome em modo debug**

   ```powershell
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"
   ```

2. **Faça login no LinkedIn**

   Acesse **linkedin.com** e entre com sua conta na janela aberta.

3. **Execute o script de coleta**

   No terminal com o ambiente virtual ativo:

   ```powershell
   python busca_candidatos.py
   ```

   O script conectará ao Chrome logado e visitará os perfis listados em `dataset/candidatos.csv`.  
   Após o término, será criado o arquivo **`dados_extraidos.csv`** na raiz do projeto.

---

### Etapa 3 — Iniciar o Servidor da API

No mesmo terminal (com o `.venv` ativo), execute:

```powershell
uvicorn main:app --reload
```

O servidor exibirá algo como:
```
Uvicorn running on http://127.0.0.1:8000
```

Deixe este terminal aberto — ele é o **backend da aplicação**.

---

### Etapa 4 — Usar a Aplicação Web

Abra o navegador e acesse:  
 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#### Fluxo de uso:
1. **Cadastrar Vaga:**  
   Preencha o formulário “1. Cadastrar Vaga” e clique em **Salvar Vaga**.  
   Isso criará o arquivo `vaga.json`.

2. **Iniciar Análise:**  
   Clique em **Iniciar Análise dos Candidatos** para que a IA processe os dados.

3. **Aguardar:**  
   O tempo depende da quantidade de candidatos.

4. **Atualizar Resultados:**  
   Clique em **Atualizar Resultados** para visualizar o **Top 5** e os **Piores 5** candidatos analisados.

---

## Créditos

Desenvolvido por **Alexandre Salgado**  
Projeto acadêmico – Engenharia de Software – Universidade Católica de Santa Catarina

---

## Estrutura de Pastas

```
/N2/
│
├── dataset/               # Dados de entrada para scraping
│   └── candidatos.csv
│
├── public/                # Frontend (Interface do Usuário)
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── .env                   # Chave da API (ignorado pelo Git)
├── .gitignore             # Ignora arquivos sensíveis (.env, .venv/, etc.)
├── busca_candidatos.py    # Script de scraping (LinkedIn)
├── config.py              # Configuração do modelo de IA
├── core_analise.py        # Lógica de análise com Gemini
├── main.py                # Servidor FastAPI
├── requirements.txt       # Dependências Python
├── utils.py               # Funções auxiliares (salvar/carregar arquivos)
│
├── dados_extraidos.csv    # Gerado pela coleta de dados
├── vaga.json              # Gerado ao salvar vaga
└── resultados.json        # Gerado após a análise da IA
```
