import pandas as pd
import plotly.express as px

df = pd.read_csv("musica.csv")
df['genre_clean'] = df['genre'].str.split(',').str[0]
df = df[df['genre_clean'] != 'set()']

top10_artistas = df['genre_clean'].value_counts().head(10).index

artistas_streams = df.groupby(['genre_clean', 'artist'])['Stream'].sum().reset_index()
artistas_streams = artistas_streams[artistas_streams['genre_clean'].isin(top10_artistas)]

top10_streams = artistas_streams.sort_values(['genre_clean', 'Stream'], ascending=[True, False]).groupby('genre_clean').head(10)

df_filtrado = df.merge(top10_streams[['genre_clean', 'artist']], on=['genre_clean', 'artist'], how='inner')
canciones_streams = df_filtrado.groupby(['genre_clean', 'artist', 'song'])['Stream'].sum().reset_index()

top5_canciones = canciones_streams.sort_values(['genre_clean', 'artist', 'Stream'], ascending=[True, True, False]).groupby(['genre_clean', 'artist']).head(5)

fig_streams = px.treemap(top5_canciones,
                  path=[px.Constant("Géneros"), 'genre_clean', 'artist', 'song'],
                  values='Stream',
                  color='genre_clean',
                  title="Top 10 Artistas por Género y con sus Top 5 Canciones")

fig_streams.update_traces(textinfo="label+value", textfont_size=12)
fig_streams.show()