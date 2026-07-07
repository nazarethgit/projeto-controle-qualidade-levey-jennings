# Controle de Qualidade Laboratorial — Six Sigma & Westgard

App em Streamlit que aplica o método **Six Sigma** (adaptado ao
controle de qualidade laboratorial) e o clássico **gráfico de
Levey-Jennings** para avaliar a estabilidade de um método de medição
analítica — o mesmo tipo de análise usada em laboratórios clínicos
para validar equipamentos e reagentes.

## O que o app calcula

- **CV% (Coeficiente de Variação):** dispersão relativa dos resultados
  em torno da média — quanto menor, mais preciso o método.
- **Bias (Vício):** diferença percentual entre a média obtida pelo
  método e o valor alvo/consenso do grupo de comparação.
- **Métrica Sigma:** combina o erro total admitido (ETa), o bias e o
  CV% numa única métrica de 1 a 6+, seguindo a lógica do Six Sigma
  aplicado à área da saúde.
- **Gráfico de Levey-Jennings:** os resultados ao longo do tempo, com
  limites de ±1, ±2 e ±3 desvios-padrão — usado para aplicar
  visualmente as regras de Westgard (detecção de tendências, desvios
  sistemáticos e erros aleatórios).

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Sem enviar nenhum arquivo, o app já abre com dados de exemplo. Para
testar o upload, use `dados/exemplo_controle.csv` (mesmo dado, em
formato de arquivo) — o CSV precisa ter uma coluna chamada
**Resultado** (e idealmente uma coluna **dia**).

## Interpretando o nível Sigma

| Sigma | Interpretação |
|---|---|
| < 3 | Método instável — rejeitar/revisar processo analítico |
| 3 – 6 | Aceitável |
| > 6 | Excelência |


