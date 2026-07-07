"""
Controle de Qualidade Laboratorial — Six Sigma + Regras de Westgard
=====================================================================

App em Streamlit que aplica o método Six Sigma (adaptado ao contexto
de laboratório clínico) para avaliar a estabilidade analítica de um
método de medição, além de plotar o clássico gráfico de
Levey-Jennings usado no controle de qualidade interno de laboratórios.

Conceitos usados:
- CV% (Coeficiente de Variação): dispersão relativa dos resultados.
- Bias (Vício): diferença percentual entre a média obtida e o valor
  alvo esperado (média do grupo/consenso).
- Métrica Sigma: quanto maior, mais "folga" o método tem entre o erro
  que ele realmente comete e o erro total máximo admitido (ETa).
- Gráfico de Levey-Jennings: mostra os resultados ao longo do tempo
  com limites de ±1, ±2 e ±3 desvios-padrão — usado para aplicar as
  regras de Westgard (detecção visual de tendências e erros).

Rode: streamlit run app.py
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Six Sigma & Westgard — Controle de Qualidade",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Aplicando Six Sigma com Regras de Westgard")
st.caption(
    "Avaliação da estabilidade analítica de um método laboratorial "
    "a partir de dados de controle de qualidade interno."
)

# ----------------------------------------------------------------
# SIDEBAR — upload de dados e parâmetros do método
# ----------------------------------------------------------------
st.sidebar.title("Controle")

st.sidebar.subheader("Upload de Dados")
arquivo_subido = st.sidebar.file_uploader("Escolha um arquivo CSV", type=["csv"])
st.sidebar.caption("O CSV precisa ter uma coluna chamada **Resultado** (e idealmente uma coluna **dia**).")

if arquivo_subido is not None:
    df = pd.read_csv(arquivo_subido)
else:
    # Dados de exemplo — usados quando nenhum arquivo é enviado, para
    # o app já nascer com algo pra mostrar (bom para portfólio/demo).
    dados_exemplo = {
        "dia": range(1, 21),
        "Resultado": [100, 102, 97, 98, 103, 101, 99, 100, 102, 97, 98, 104, 101, 99, 100, 102, 97, 98, 103, 97],
    }
    df = pd.DataFrame(dados_exemplo)
    st.sidebar.info("Nenhum arquivo enviado — exibindo dados de exemplo.")

st.sidebar.subheader("Parâmetros do método")
et_a_admitido = st.sidebar.number_input(
    "ETa — Erro Total Admitido (%)",
    help="Erro total máximo que o método pode cometer, definido pela especificação da qualidade (ex: CLIA, RiliBÄK).",
)
media_grupo = st.sidebar.number_input(
    "Média do Grupo (valor alvo/consenso)",
    help="Valor de referência do grupo de comparação (ex: consenso do fornecedor de controle), usado para calcular o vício (bias).",
)

# ----------------------------------------------------------------
# Estatísticas descritivas
# ----------------------------------------------------------------
media = df["Resultado"].mean()
desvio_padrao = df["Resultado"].std()
cv = (desvio_padrao / media) * 100 if media else 0

if media_grupo > 0:
    # Mantemos o sinal para ver a direção do erro (super ou subestimando)
    bias = ((media - media_grupo) / media_grupo) * 100
else:
    bias = 0

st.sidebar.write(f"**Bias (Vício):** {bias:.2f} %")

# ----------------------------------------------------------------
# Dados brutos + KPIs
# ----------------------------------------------------------------
with st.expander("Ver dados brutos"):
    st.dataframe(df, use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média", value=f"{media:.2f}")
with col2:
    st.metric(label="Desvio Padrão (DP)", value=f"{desvio_padrao:.2f} mg/dL")
with col3:
    st.metric(label="Coeficiente de Variação (CV%)", value=f"{cv:.2f} %")

st.divider()

# ----------------------------------------------------------------
# Métrica Sigma
# ----------------------------------------------------------------
st.subheader("Calculando a Métrica Sigma")

with st.expander("Como interpretar o nível Sigma"):
    st.write(
        "- **< 3 Sigma:** método instável, rejeitar/revisar processo analítico.\n"
        "- **3 a 6 Sigma:** aceitável, dentro da faixa esperada para a maioria dos métodos.\n"
        "- **> 6 Sigma:** excelência — erro do método bem menor que o erro total admitido."
    )

# Usamos abs(bias) para garantir que o erro (independente da direção)
# seja subtraído do erro total permitido, antes de dividir pelo CV%.
if cv > 0:
    nivel_sigma = (et_a_admitido - abs(bias)) / cv
else:
    nivel_sigma = 0

if nivel_sigma >= 6:
    st.success(f"Excelente! Sigma: {nivel_sigma:.2f}")
elif nivel_sigma >= 3:
    st.warning(f"Aceitável. Sigma: {nivel_sigma:.2f}")
else:
    st.error(f"Rejeitar! Sigma: {nivel_sigma:.2f} — Método instável.")

st.divider()

# ----------------------------------------------------------------
# Gráfico de Levey-Jennings
# ----------------------------------------------------------------
st.subheader("Gráfico de Levey-Jennings")
st.caption(
    "Resultados ao longo do tempo com limites de ±1, ±2 e ±3 desvios-padrão — "
    "base visual para aplicar as regras de Westgard (ex: 1-3s, 2-2s, R-4s)."
)

fig = go.Figure()

# Linha dos resultados diários
fig.add_trace(
    go.Scatter(
        x=df["dia"],
        y=df["Resultado"],
        mode="lines+markers",
        name="Resultado Diário",
        line=dict(color="blue"),
    )
)

# Linha da média
fig.add_hline(y=media, line_dash="dash", line_color="green", annotation_text="Média")

# Limites de desvio-padrão (±1s discreto, ±2s e ±3s com anotação)
fig.add_hline(y=media + desvio_padrao, line_dash="dot", line_color="orange", opacity=0.5)
fig.add_hline(y=media - desvio_padrao, line_dash="dot", line_color="orange", opacity=0.5)

fig.add_hline(y=media + 2 * desvio_padrao, line_dash="dash", line_color="orange", annotation_text="+2s")
fig.add_hline(y=media - 2 * desvio_padrao, line_dash="dash", line_color="orange", annotation_text="-2s")

fig.add_hline(y=media + 3 * desvio_padrao, line_dash="solid", line_color="red", annotation_text="+3s")
fig.add_hline(y=media - 3 * desvio_padrao, line_dash="solid", line_color="red", annotation_text="-3s")

fig.update_layout(
    title="Controle de Qualidade — Glicemia",
    xaxis_title="Dia / Corrida Analítica",
    yaxis_title="Concentração (mg/dL)",
    yaxis=dict(range=[media - 4 * desvio_padrao, media + 4 * desvio_padrao]),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)
