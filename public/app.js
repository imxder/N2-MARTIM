document.addEventListener('DOMContentLoaded', () => {
    
    // --- Referências de Elementos ---
    const form = document.getElementById('vaga-form');
    const statusBar = document.getElementById('status-bar');
    const btnIniciarAnalise = document.getElementById('btn-iniciar-analise');
    const btnAtualizarResultados = document.getElementById('btn-atualizar-resultados');
    const resultadosContainer = document.getElementById('resultados-container');

    // --- Funções Auxiliares ---

    /**
     * Exibe uma mensagem na barra de status.
     * @param {string} message - A mensagem a ser exibida.
     * @param {'success' | 'error' | 'info'} type - O tipo de mensagem.
     */
    function showStatus(message, type) {
        statusBar.textContent = message;
        statusBar.className = `status-bar ${type}`;
        
        // Limpa a mensagem após 5 segundos
        setTimeout(() => {
            statusBar.textContent = '';
            statusBar.className = 'status-bar';
        }, 5000);
    }

    /**
     * Converte quebras de linha de um textarea para um array.
     * @param {string} text - O texto do textarea.
     * @returns {string[]} - Um array de strings.
     */
    function textToArray(text) {
        return text.split('\n').map(item => item.trim()).filter(item => item.length > 0);
    }

    /**
     * Converte um array para string de textarea (com quebras de linha).
     * @param {string[]} arr - O array de strings.
     * @returns {string} - O texto formatado.
     */
    function arrayToText(arr) {
        return (arr || []).join('\n');
    }

    // --- Funções de API ---

    /**
     * Carrega a vaga existente da API e preenche o formulário.
     */
    async function carregarVaga() {
        try {
            const response = await fetch('/api/vaga');
            if (!response.ok) throw new Error('Falha ao carregar vaga.');
            
            const vaga = await response.json();
            
            form.titulo.value = vaga.titulo || '';
            form.grau_escolaridade.value = vaga.grau_escolaridade || '';
            form.tempo_experiencia.value = vaga.tempo_experiencia || '';
            form.observacoes.value = vaga.observacoes || '';
            form.conhecimentos_obrigatorios.value = arrayToText(vaga.conhecimentos_obrigatorios);
            form.conhecimentos_desejados.value = arrayToText(vaga.conhecimentos_desejados);
            
        } catch (error) {
            console.error('Erro ao carregar vaga:', error);
            showStatus('Não foi possível carregar a vaga salva.', 'error');
        }
    }

    /**
     * Salva a vaga enviando os dados do formulário para a API.
     * @param {Event} event - O evento de submit do formulário.
     */
    async function salvarVaga(event) {
        event.preventDefault(); // Impede o recarregamento da página

        const vagaData = {
            titulo: form.titulo.value,
            grau_escolaridade: form.grau_escolaridade.value,
            tempo_experiencia: form.tempo_experiencia.value,
            observacoes: form.observacoes.value,
            conhecimentos_obrigatorios: textToArray(form.conhecimentos_obrigatorios.value),
            conhecimentos_desejados: textToArray(form.conhecimentos_desejados.value),
        };

        try {
            const response = await fetch('/api/vaga', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vagaData),
            });

            if (!response.ok) throw new Error('Falha ao salvar a vaga.');
            
            const result = await response.json();
            showStatus(result.mensagem, 'success');
        } catch (error) {
            console.error('Erro ao salvar vaga:', error);
            showStatus('Erro ao salvar a vaga.', 'error');
        }
    }

    /**
     * Dispara o início da análise em background.
     */
    async function iniciarAnalise() {
        if (!confirm('Isso iniciará a análise em background. O processo pode levar vários minutos. Deseja continuar?')) {
            return;
        }

        try {
            const response = await fetch('/api/analisar', { method: 'POST' });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Erro desconhecido');
            }
            
            showStatus(result.mensagem, 'info');
        } catch (error) {
            console.error('Erro ao iniciar análise:', error);
            showStatus(error.message, 'error');
        }
    }

    /**
     * Busca os resultados mais recentes da API e atualiza a interface.
     */
    async function carregarResultados() {
        try {
            const response = await fetch('/api/resultados');
            if (!response.ok) throw new Error('Falha ao carregar resultados.');

            const resultados = await response.json();
            renderizarResultados(resultados);
            showStatus('Resultados atualizados.', 'info');
            
        } catch (error) {
            console.error('Erro ao carregar resultados:', error);
            showStatus('Não foi possível carregar os resultados.', 'error');
        }
    }

    /**
     * Renderiza os cards de candidatos na tela.
     * @param {Array} resultados - A lista de candidatos analisados.
     */
    function renderizarResultados(resultados) {
        if (!resultados || resultados.length === 0) {
            resultadosContainer.innerHTML = '<p>Nenhum resultado de análise encontrado.</p>';
            return;
        }
        
        const top5 = resultados.slice(0, 5);
        const bottom5 = resultados.slice(-5).reverse(); // Pega os 5 últimos e inverte

        let html = '<div class="ranking-group"><h3>TOP 5 MAIS ADERENTES</h3>';
        top5.forEach((c, index) => {
            html += `
                <div class="candidato-card">
                    <h4>${index + 1}º: ${c.nome} - <span class="score-top">Score: ${c.score}%</span></h4>
                    <p><strong>Justificativa:</strong> ${c.justificativa}</p>
                    <p><strong>Perfil:</strong> <a href="${c.url}" target="_blank">${c.url}</a></p>
                </div>
            `;
        });
        html += '</div>';

        html += '<div class="ranking-group"><h3>TOP 5 MENOS ADERENTES</h3>';
        bottom5.forEach((c, index) => {
            html += `
                <div class="candidato-card">
                    <h4>${index + 1}º: ${c.nome} - <span class="score-bottom">Score: ${c.score}%</span></h4>
                    <p><strong>Justificativa:</strong> ${c.justificativa}</p>
                    <p><strong>Perfil:</strong> <a href="${c.url}" target="_blank">${c.url}</a></p>
                </div>
            `;
        });
        html += '</div>';

        resultadosContainer.innerHTML = html;
    }

    // --- Inicialização ---
    form.addEventListener('submit', salvarVaga);
    btnIniciarAnalise.addEventListener('click', iniciarAnalise);
    btnAtualizarResultados.addEventListener('click', carregarResultados);

    // Carrega os dados iniciais ao abrir a página
    carregarVaga();
    carregarResultados();
});