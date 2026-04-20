import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("musica.csv")
df = df[['Danceability', 'Stream', 'Valence', 'Album_type']].dropna()


df['dance_bin'] = pd.cut(df['Danceability'], bins=8)

# Agrupamos por tipo de álbum y bin
grouped = df.groupby(['Album_type', 'dance_bin'], observed=True).agg(
    dance_mean=('Danceability', 'mean'),
    stream_mean=('Stream', 'mean'),
    valence_mean=('Valence', 'mean'),
    count=('Stream', 'count')
).reset_index()

# Escalamos tamaño de burbujas
grouped['bubble_size'] = grouped['valence_mean'] * 40

colores = {
    'album': 'red',
    'single': 'blue',
    'compilation': 'green'
}
nombres = {
    'album': 'Álbum',
    'single': 'Single',
    'compilation': 'Compilación'
}

fig = go.Figure()

for tipo in ['album', 'single', 'compilation']:
    data = grouped[grouped['Album_type'] == tipo]
    fig.add_trace(go.Scatter(
        x=data['dance_mean'],
        y=data['stream_mean'] / 1e6,
        mode='markers',
        name=nombres[tipo],
        marker=dict(
            size=data['bubble_size'],
            color=colores[tipo],
            line=dict(width=1.5)
        ),
        text=data.apply(lambda r: f"Bailabilidad: {r['dance_mean']:.2f}<br>Streams: {r['stream_mean']/1e6:.1f}M<br>Valencia: {r['valence_mean']:.2f}", axis=1),
        hovertemplate='%{text}<extra></extra>'
    ))

fig.update_layout(
    title='Relación entre Bailabilidad, Streams y Valencia por Tipo de Álbum',
    xaxis_title='Bailabilidad',
    yaxis_title='Streams promedio (millones)',
    template='plotly_dark',
    legend_title='Tipo de álbum'
)

fig.show()