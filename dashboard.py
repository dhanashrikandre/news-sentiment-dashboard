import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd

from etl import fetch_rss_headlines
from sentiment import analyze_sentiment

# Prepare data
df = fetch_rss_headlines()
df['sentiment'] = df['headline'].apply(analyze_sentiment)

country_sentiment = df.groupby('country')['sentiment'] \
                     .agg(lambda x: x.value_counts().idxmax()) \
                     .reset_index()

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🧠 AI-Powered World News Sentiment Map"),
    
    dcc.Graph(id='sentiment-map'),

    html.Div(id='country-headlines', style={'marginTop': '20px'})
])

@app.callback(
    Output('sentiment-map', 'figure'),
    Input('sentiment-map', 'clickData')
)
def update_map(clickData):
    fig = px.choropleth(
        country_sentiment,
        locations="country",
        locationmode="country names",
        color="sentiment",
        color_discrete_map={
            "Positive": "green",
            "Neutral": "gray",
            "Negative": "red"
        },
        title="Click on a country to see its top headlines"
    )
    return fig

@app.callback(
    Output('country-headlines', 'children'),
    Input('sentiment-map', 'clickData')
)
def display_headlines(clickData):
    if clickData:
        country = clickData['points'][0]['location']
        headlines = df[df['country'].str.lower() == country.lower()]['headline'].tolist()
        if headlines:
            return html.Div([
                html.H3(f"📰 Top Headlines from {country}"),
                html.Ul([html.Li(h) for h in headlines])
            ])
    return html.Div("Click a country to view headlines")

if __name__ == "__main__":
    app.run(debug=True)