import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("musica.csv")
cols = ['Danceability', 'Energy', 'Loudness', 'Acousticness', 'Valence', 'Views', 'Likes', 'Stream']
pares = df[cols].corr().unstack().reset_index(name='corr')
pares = pares[(pares['level_0'] < pares['level_1']) & (pares['corr'].abs() > 0.2)].sort_values('corr')
pares['nombre'] = pares['level_0'] + " vs " + pares['level_1']

fig = go.Figure()

for _, row in pares.iterrows():
    color = 'steelblue' if row['corr'] < 0 else 'tomato'
    fig.add_shape(type="line", x0=0, y0=row['nombre'], x1=row['corr'], y1=row['nombre'],
                  line=dict(color=color, width=2))

fig.add_trace(go.Scatter(
    x=pares['corr'],
    y=pares['nombre'],
    mode='markers+text',
    text=pares['corr'].round(2),
    textposition=['middle left' if c < 0 else 'middle right' for c in pares['corr']],
    marker=dict(size=12, color=['steelblue' if c < 0 else 'tomato' for c in pares['corr']])
))

fig.add_shape(type="line", x0=0, y0=-0.5, x1=0, y1=len(pares)-0.5,
              line=dict(color="black", width=1, dash="dot"))

fig.update_layout(
    title="Correlaciones de variables",
    showlegend=False,
    plot_bgcolor='#EEF2F7',
    xaxis=dict(range=[-1.2, 1.2], gridcolor='white'),
    yaxis=dict(gridcolor='white'),
    margin=dict(l=180)
)

fig.show()