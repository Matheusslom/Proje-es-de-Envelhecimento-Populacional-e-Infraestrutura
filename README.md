# Projeto Integrador — Crescimento Demográfico (Persona: Prefeitos de Capitais)

Esta pasta contém **o código individual pronto** para subir no seu próprio repositório do
GitHub e entregar na atividade **"Projeto Integrador - Entrega Individual"**.

## Conteúdo da pasta

- `app.py` → o dashboard Streamlit do seu indicador (já com upload de dados, filtros,
  estatísticas obrigatórias — média, mediana, moda, quartis, IQR, amplitude, desvio padrão —,
  detecção de outliers pela regra 1,5×IQR, gráficos e seção de notícias).
- `estatisticas.py` → módulo com as funções estatísticas usadas pelo `app.py`.
- `dados/` → base de dados real do IBGE (Censo Demográfico 2010/2022) já tratada, usada como
  padrão quando nenhum arquivo é enviado pelo upload.
- `requirements.txt` → bibliotecas necessárias para rodar o projeto.

## Passo a passo para subir no GitHub

1. **Teste localmente (opcional, mas recomendado):**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
   O navegador deve abrir em `http://localhost:8501` com o seu dashboard funcionando.

2. **Crie um repositório novo no GitHub** (pelo site: botão verde "New repository").
   Sugestão de nome: `projeto-integrador-crescimento-demografico-SEUNOME`.

3. **Suba os arquivos desta pasta** para o repositório. Pelo terminal, dentro desta pasta:
   ```bash
   git init
   git add .
   git commit -m "Projeto Integrador - Crescimento Demografico - minha parte individual"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   git push -u origin main
   ```
   (Ou, se preferir, use a interface do GitHub: "Add file" → "Upload files" e arraste todos
   os arquivos desta pasta.)

4. **Copie o link do repositório** e entregue na atividade **"Projeto Integrador - Entrega
   Individual"**, conforme combinado no grupo.

5. **No dia da integração**, todos levam o link/código do seu repositório para juntar as 5
   partes em um único painel Streamlit (com barra lateral de navegação entre os indicadores).

## Observação sobre os dados

Os dados em `dados/` vêm do **Censo Demográfico do IBGE (2010 e 2022)** — primeiros resultados
de população e domicílios, e da publicação "População por idade e sexo" (resultados do
universo). Onde o IBGE não publica o recorte exato por município nesta divulgação (ex.:
pirâmide etária por idade simples), isso está sinalizado no próprio dashboard como
**aproximação didática**, para manter o rigor e a honestidade da análise.
