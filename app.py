"""
Projeto Integrador — "Números que Falam: Descobrindo o Brasil"
Tema do Grupo: Crescimento Demográfico (Persona: Prefeitos de Capitais)

Integrante: SALOMÉ
Indicador individual: Projeções de Envelhecimento Populacional e Infraestrutura
Fonte: IBGE, Censo Demográfico 2022 — População por idade e sexo (índice de envelhecimento).

Como rodar localmente:
    pip install -r requirements.txt
    streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from estatisticas import resumo_estatistico, detectar_outliers, classificar_outlier, formatar_numero

st.set_page_config(page_title="Envelhecimento e Infraestrutura | Salomé", page_icon="🏗️", layout="wide")

CAMINHO_DADOS_PADRAO = "dados/estrutura_etaria_uf_capitais.csv"

PERSONAS = {
    "Curitiba": "Carlos (Prefeito de Curitiba)", "Porto Alegre": "Eduardo (Prefeito de Porto Alegre)",
    "Belo Horizonte": "Elisa (Prefeita de Belo Horizonte)", "Salvador": "Jorge (Prefeito de Salvador)",
    "Florianopolis": "Roberto (Prefeito de Florianópolis)",
}


@st.cache_data
def carregar_dados_padrao() -> pd.DataFrame:
    return pd.read_csv(CAMINHO_DADOS_PADRAO)


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    for c in ["pct_0_14", "pct_15_64", "pct_65_mais", "indice_envelhecimento", "idade_mediana", "ano"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def projetar_linear(anos: np.ndarray, valores: np.ndarray, anos_futuros: np.ndarray) -> np.ndarray:
    """Projeção simples por regressão linear (mínimos quadrados) — adequada para um
    indicador didático de tendência; não substitui as projeções demográficas oficiais do IBGE."""
    coef = np.polyfit(anos, valores, deg=1)
    return np.polyval(coef, anos_futuros)


st.sidebar.title("⚙️ Filtros")
st.sidebar.caption("Projeto Integrador • Envelhecimento e Infraestrutura")

arquivo = st.sidebar.file_uploader("Upload da base IBGE (CSV ou XLSX)", type=["csv", "xlsx"])
if arquivo is not None:
    try:
        df_bruto = pd.read_excel(arquivo) if arquivo.name.endswith(".xlsx") else pd.read_csv(arquivo)
        st.sidebar.success("Arquivo carregado com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo: {e}")
        df_bruto = carregar_dados_padrao()
else:
    df_bruto = carregar_dados_padrao()
    st.sidebar.info("Usando a base padrão do IBGE (Censo 2022 — índice de envelhecimento).")

df = tratar_dados(df_bruto)

capitais = sorted(df["capital"].dropna().unique().tolist())
capital_sel = st.sidebar.selectbox("Capital (persona)", capitais, index=capitais.index("Curitiba") if "Curitiba" in capitais else 0)

horizonte = st.sidebar.slider("Horizonte da projeção (anos à frente de 2022)", min_value=4, max_value=28, value=12, step=4)

df_capital = df[df["capital"] == capital_sel].sort_values("ano")

# --------------------------------------------------------------------------------------
st.title("🏗️ Projeções de Envelhecimento Populacional e Infraestrutura")
st.caption(
    f"Startup de Análise de Dados • Consultoria para {PERSONAS.get(capital_sel, capital_sel)} • "
    f"Responsável: **Salomé**"
)

with st.expander("📋 Cenário da persona (clique para ler)"):
    st.markdown(
        """
        Os prefeitos revisam os **Planos Diretores** olhando para a década seguinte: quanto
        mais rápido a cidade envelhece, maior a urgência de investir agora em UBS geriátricas,
        mobilidade acessível e centros de convivência — e menor a pressão futura sobre creches
        e escolas de ensino fundamental.
        """
    )

# --------------------------------------------------------------------------------------
# KPIs — situação atual (2022)
# --------------------------------------------------------------------------------------
linha_2022 = df_capital[df_capital["ano"] == 2022].iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("% 65+ em 2022", f"{formatar_numero(linha_2022['pct_65_mais'])}%")
c2.metric("Índice de envelhecimento 2022", formatar_numero(linha_2022["indice_envelhecimento"]))
c3.metric("Idade mediana (UF) 2022", f"{int(linha_2022['idade_mediana'])} anos")

# --------------------------------------------------------------------------------------
# PROJEÇÃO LINEAR SIMPLES
# --------------------------------------------------------------------------------------
st.subheader(f"📈 Projeção de envelhecimento — {capital_sel}")

anos_hist = df_capital["ano"].values.astype(float)
pct_65_hist = df_capital["pct_65_mais"].values.astype(float)
ano_final_projecao = 2022 + horizonte
anos_futuros = np.arange(2023, ano_final_projecao + 1)
projecao = projetar_linear(anos_hist, pct_65_hist, anos_futuros)
projecao = np.clip(projecao, 0, 100)  # percentual não pode passar de 100%

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(x=anos_hist, y=pct_65_hist, mode="lines+markers", name="Histórico (Censo)", line=dict(color="#1f77b4")))
fig_proj.add_trace(go.Scatter(x=anos_futuros, y=projecao, mode="lines+markers", name="Projeção linear", line=dict(color="#d62728", dash="dash")))
fig_proj.update_layout(
    title=f"% da população com 65+ anos — histórico e projeção até {ano_final_projecao}",
    xaxis_title="Ano", yaxis_title="% da população com 65 anos ou mais", height=450,
)
st.plotly_chart(fig_proj, use_container_width=True)

pct_projetado = projecao[-1]
st.info(
    f"Pela tendência linear dos últimos censos, **{capital_sel}** pode chegar a "
    f"**{formatar_numero(pct_projetado)}%** de idosos (65+) em **{ano_final_projecao}** "
    f"— um crescimento de {formatar_numero(pct_projetado - linha_2022['pct_65_mais'])} p.p. "
    "em relação a 2022. ⚠️ Projeção didática por regressão linear simples; para decisões reais "
    "de política pública, usar as **Projeções da População do IBGE**, que incorporam fecundidade, "
    "mortalidade e migração."
)

# --------------------------------------------------------------------------------------
# ESTATÍSTICA DESCRITIVA — comparação entre as 5 capitais em 2022
# --------------------------------------------------------------------------------------
st.subheader("📊 Resumo estatístico — Índice de envelhecimento entre as 5 capitais (2022)")
df_2022 = df[df["ano"] == 2022]
stats = resumo_estatistico(df_2022["indice_envelhecimento"])
cA, cB, cC, cD = st.columns(4)
cA.metric("Média", formatar_numero(stats["media"]))
cB.metric("Mediana", formatar_numero(stats["mediana"]))
cC.metric("IQR", formatar_numero(stats["iqr"]))
cD.metric("Desvio padrão", formatar_numero(stats["desvio_padrao"]))

outliers = detectar_outliers(df_2022, "indice_envelhecimento")
if not outliers.empty:
    st.warning("Capital(is) com índice de envelhecimento estatisticamente atípico: " + ", ".join(outliers["capital"].tolist()))
else:
    st.success("Nenhuma capital é outlier de envelhecimento nesta seleção (1,5×IQR).")

fig_comp = px.bar(
    df_2022.sort_values("indice_envelhecimento"), x="indice_envelhecimento", y="capital", orientation="h",
    labels={"indice_envelhecimento": "Índice de envelhecimento (idosos por 100 crianças)", "capital": ""},
    title="Índice de envelhecimento por capital (2022) — quanto maior, mais envelhecida a estrutura",
    color="indice_envelhecimento", color_continuous_scale="OrRd",
)
st.plotly_chart(fig_comp, use_container_width=True)

# --------------------------------------------------------------------------------------
# IMPACTO EM INFRAESTRUTURA — ESTIMATIVA ILUSTRATIVA
# --------------------------------------------------------------------------------------
st.subheader("🏥 Impacto estimado em infraestrutura")
st.caption(
    "Estimativa didática: assume 1 vaga de UBS geriátrica / centro de convivência a cada "
    "1.000 idosos adicionais, apenas para ilustrar a ordem de grandeza do planejamento."
)
pop_atual = {
    "Curitiba": 1773733, "Porto Alegre": 1332570, "Belo Horizonte": 2315560,
    "Salvador": 2418005, "Florianopolis": 537213,
}.get(capital_sel, 1_000_000)

idosos_2022 = pop_atual * linha_2022["pct_65_mais"] / 100
idosos_projetado = pop_atual * pct_projetado / 100
novos_idosos = max(idosos_projetado - idosos_2022, 0)
vagas_estimadas = int(novos_idosos / 1000)

c1, c2, c3 = st.columns(3)
c1.metric("Idosos (65+) em 2022 (estimado)", f"{int(idosos_2022):,}".replace(",", "."))
c2.metric(f"Idosos (65+) em {ano_final_projecao} (projetado)", f"{int(idosos_projetado):,}".replace(",", "."))
c3.metric("Novas vagas de atenção ao idoso sugeridas", f"{vagas_estimadas:,}".replace(",", "."))

# --------------------------------------------------------------------------------------
# RESPOSTA ÀS PERGUNTAS DE NEGÓCIO
# --------------------------------------------------------------------------------------
st.subheader("💼 Resposta às Perguntas de Negócio da Persona")
st.markdown(
    f"""
1. **Qual a velocidade do envelhecimento em {capital_sel}?**
   O índice de envelhecimento saltou de forma expressiva entre 2010 e 2022; mantendo a
   tendência linear, a cidade pode chegar a **{formatar_numero(pct_projetado)}%** de idosos
   em **{ano_final_projecao}**, reforçando a urgência de antecipar investimentos em saúde e
   mobilidade para a terceira idade.

2. **Como priorizar o orçamento de infraestrutura entre as 5 capitais?**
   Capitais com maior índice de envelhecimento hoje (ver ranking acima) devem priorizar
   **UBS geriátricas e transporte acessível**; capitais relativamente mais jovens ainda têm
   janela para investir em **educação infantil e fundamental** antes que a pirâmide se inverta.
    """
)

# --------------------------------------------------------------------------------------
# CONTEÚDO ADICIONAL
# --------------------------------------------------------------------------------------
st.subheader("📰 Conteúdo adicional")
st.markdown(
    """
    **🔗 Censo 2022: número de pessoas com 65 anos ou mais de idade cresceu 57,4% em 12 anos**
    *IBGE Agência de Notícias*
    [Ler reportagem](https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-denoticias/noticias/38186-)

    **🔗 Censo 2022: Minas está entre os estados com maior população idosa do Brasil**
    *Itatiaia* [Ler reportagem](https://www.itatiaia.com.br/brasil/censo-2022-minas-esta-entre-os-estados-com-maior-populacao-idosa-do-brasil/)
    """
)

st.divider()
st.caption(
    "Fonte dos dados: IBGE, Censo Demográfico 2022 — População por idade e sexo (índice de envelhecimento). "
    "Projeção: regressão linear simples sobre os censos históricos (uso didático). "
    "Desenvolvido por Salomé • Projeto Integrador — Python & Matemática."
)
