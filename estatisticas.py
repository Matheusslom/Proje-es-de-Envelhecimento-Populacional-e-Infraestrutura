"""
Módulo de funções estatísticas — Projeto Integrador "Números que Falam: Descobrindo o Brasil"
Grupo: Crescimento Demográfico (Persona: Prefeitos de Capitais)

Implementa as métricas obrigatórias do guia do projeto:
média, mediana, moda, quartis (Q1/Q2/Q3), IQR, amplitude,
variância, desvio padrão e detecção de outliers (regra 1,5 x IQR).

Cada integrante usa este módulo na sua seção individual do dashboard.
"""

import numpy as np
import pandas as pd


def resumo_estatistico(serie: pd.Series) -> dict:
    """Calcula o resumo estatístico completo de uma série numérica.

    Retorna um dicionário com: n, média, mediana, moda, mínimo, máximo,
    Q1, Q2 (mediana), Q3, IQR, amplitude, desvio padrão, variância e os
    limites de corte de outliers pela regra 1,5 x IQR.
    """
    s = pd.to_numeric(serie, errors="coerce").dropna()
    if s.empty:
        return {}

    moda_calc = s.mode()
    moda = moda_calc.iloc[0] if not moda_calc.empty else np.nan

    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)
    q3 = s.quantile(0.75)
    iqr = q3 - q1

    return {
        "n": int(s.shape[0]),
        "media": s.mean(),
        "mediana": s.median(),
        "moda": moda,
        "minimo": s.min(),
        "maximo": s.max(),
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "amplitude": s.max() - s.min(),
        "desvio_padrao": s.std(ddof=1) if len(s) > 1 else 0.0,
        "variancia": s.var(ddof=1) if len(s) > 1 else 0.0,
        "limite_inferior_outlier": q1 - 1.5 * iqr,
        "limite_superior_outlier": q3 + 1.5 * iqr,
    }


def detectar_outliers(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Retorna as linhas de df cujo valor em `coluna` é outlier pela regra 1,5 x IQR."""
    s = pd.to_numeric(df[coluna], errors="coerce")
    validos = s.dropna()
    if validos.empty:
        return df.iloc[0:0]
    q1, q3 = validos.quantile(0.25), validos.quantile(0.75)
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = (s < lim_inf) | (s > lim_sup)
    return df[mask.fillna(False)].copy()


def classificar_outlier(valor: float, q1: float, q3: float, iqr: float) -> str:
    """Classifica um valor individual segundo a regra 1,5 x IQR."""
    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    if pd.isna(valor):
        return "Sem dado"
    if valor > lim_sup:
        return "Outlier superior (muito acima do padrão)"
    if valor < lim_inf:
        return "Outlier inferior (muito abaixo do padrão)"
    return "Dentro do padrão"


def formatar_numero(valor, casas=2) -> str:
    """Formata número no padrão brasileiro (vírgula decimal, ponto de milhar)."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "-"
    txt = f"{valor:,.{casas}f}"
    return txt.replace(",", "X").replace(".", ",").replace("X", ".")
