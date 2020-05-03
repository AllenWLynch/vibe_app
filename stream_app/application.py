
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq 
import plotly.graph_objects as go
import random

app = dash.Dash(__name__)

COLORS = {
    'negative' : '#ef8a62',
    'neutral' : '#f7f7f7',
    'positive' : '#00acee',
}

#00A1E4
COLORS = {
    'positive' : '#00A1E4',
    'negative' : '#ee6352',
    'neutral' : '#f7f7f7',
}

SIDEBAR = html.Div(className='sidenav', children = [
    html.H1("Vibe", style = {'color':COLORS['positive'],'margin-bottom':'0px'}),
    html.H6("How's Twitter Feeling?", style = {'margin-top':'0px'}),
    html.Hr(),
    html.Div(style = {'text-align':'left'}, children = [
        html.P(['''Investigate daily geographical, hashtag, and sentiment trends in real time. This dashboard is backed by an 
                advanced sentiment classifier and fed by a Spark pipeline connected to the Twitter sample stream.
                Check it out ''',
                html.A('here.', href = 'https://github.com/AllenWLynch/spark_twitter_sentiment_stream', target = '_blank')]),
        html.Br(),
        html.P('This pipeline is classifying:'),
        html.Div(className = 'row', style = {'margin' : '10px'}, children = [
            html.Div(html.H1('9750', style = {'color' : COLORS['positive'], 'margin-bottom' : '0px'}), className = 'column', style = {'text-align' : 'right'}),
            html.Div(html.P('Tweets/min', style = {'margin' : '5px'}), className = 'column'),
        ]),
        html.P('while only interacting with 1% of all Twitter volumne.', style = {'margin-top' : '0px'})
    ]),
    html.Hr(),
])

INTERVAL_SLIDER = dcc.Slider(
    min=1,
    max=60,
    step=None,
    marks={
        1: '1 min',
        10: '10 mins',
        30: '30 mins',
        60: 'Hourly',
    },
    value=10,
    updatemode='mouseup'
) 

HASHTAG_PLOT = go.Figure(go.Bar(
        y = ['#coronavirus', '#hastag','#zoomuniversity','#greatbritishbakeoff','#dogs','#witcher', '#twitterstream'],
        x = [24,14,56,32,19,6,17],
        orientation = 'h',
        marker_color = COLORS['positive']
))
HASHTAG_PLOT.update_layout(
            margin = {'l': 0, 'b': 0, 't': 0, 'r': 0},
            paper_bgcolor = '#fff',
            plot_bgcolor = '#fff',
            xaxis_gridcolor = '#DCDCDC',
        )

TOGGLE_SWITCH = html.Div(daq.ToggleSwitch(id = 'toggle', value = False), style = {'width' : '100%', 'display' : 'inline-block'})

OPTIONS_BOX = html.Div(className = 'row', style = {'margin' : '10px', 'margin-top' : '20px'}, children = [
                html.Div(style = {'float' : 'left', 'width' : '40%'}, children = [
                    html.Div(className = 'infobox', style = {'margin' : '0px', 'height' : '100px', 'border-right' : 'none'}, children = [
                        html.Div('Interval', className = 'header', style = {'margin-top' : '1px'}),
                        html.Div(INTERVAL_SLIDER, className = 'body'),
                    ]),
                ]),
                html.Div(style = {'float' : 'left', 'width' : '20%'}, children = [
                    html.Div(className = 'infobox', style = {'margin' : '0px', 'height' : '100px'}, children = [
                        html.Div('Normalize Activity', className = 'header', style = {'margin-top' : '1px'}),
                        html.Div(TOGGLE_SWITCH, style = {'text-align':'center'}, className = 'body')
                    ]),
                ]),
                html.Div(style = {'float' : 'left', 'width' : '40%'}, children = [
                    html.Div(className = 'infobox', style = {'margin' : '0px', 'height' : '100px', 'border-left' : 'none'}, children = [
                        html.Div('Filters', className = 'header', style = {'margin-top' : '1px'}),
                        html.Div(dcc.Dropdown(id = 'filters'), className = 'body'),
                    ]),
                ]),
            ])

GEO_PLOT = go.Figure(go.Scattergeo())

GEO_PLOT.update_layout(
    geo_scope = 'usa',
    margin = {'l': 0, 'b': 0, 't': 0, 'r': 0},
)

def random_walk(prev, var):
    return max(0, prev + random.normalvariate(0, var))

def generate_random_walk(initial_val, length, var):
    walk = [initial_val]
    for i in range(length - 1):
        walk.append(random_walk(walk[-1], var))
    return walk

random.seed(5000)

time_x = list(range(24))
num_neg = [-1 * r for r in generate_random_walk(24, 24, 4)]
num_pos = generate_random_walk(24, 24, 4)

RIVER_PLOT = go.Figure()

RIVER_PLOT.add_trace(go.Scatter(
    x = time_x,
    y = num_pos,
    mode = 'lines',
    line = dict(width=0.5, color=COLORS['positive']),
    stackgroup='two',
    name = 'Positive',
))

RIVER_PLOT.add_trace(go.Scatter(
    x = time_x,
    y = num_neg,
    mode = 'lines',
    line = dict(width=0.5, color=COLORS['negative']),
    stackgroup='one',
    name = 'Negative',
))

RIVER_PLOT.update_layout(
    showlegend = True,
    plot_bgcolor = '#fff',
    margin = {'l': 0, 'b': 0, 't': 0, 'r': 0},
    yaxis = dict(
        title = '# of Tweets',
        linecolor = '#DCDCDC',
        ticks = 'outside',
        tickcolor= '#DCDCDC',
    ),
    xaxis = dict(
        showline = True,
        linecolor = '#DCDCDC',
        ticks = 'outside',
        tickcolor = '#DCDCDC',
        title = 'Time',
    ),
    legend=dict(
        x=0.02,
        y=1,
        traceorder="reversed",
        bgcolor="#fff",
        bordercolor="#DCDCDC",
        borderwidth=1,
        orientation="h",
    ),
    font_family = 'Arial',
    barmode = 'relative',
)

app.layout = html.Div(children=[
    SIDEBAR, 
    html.Div(className='main', children = [
        
        #html.Div(style = {'margin-top' : '20px', 'float' : 'left','width' : '85%' }, children = [
        dcc.Graph(
            id='river_plot',
            figure = RIVER_PLOT,
            style = {'height' : '50vh', 'margin' : '20px'}
        ),
        OPTIONS_BOX,
        html.Div(className = 'row', children = [
            html.Div(className = 'column', children = [
                html.Div(className = 'infobox', children = [
                    html.Div('Geotags', className = 'header'),
                    html.Div(dcc.Graph(id = 'geo_plot', figure = GEO_PLOT, style = {'height' : '45vh'}), className = 'body'),
                ]),
            ]),
            html.Div(className = 'column', children = [
                html.Div(className = 'infobox', children = [
                    html.Div('Hashtags', className = 'header'),
                    html.Div(dcc.Graph(id = 'hashtag_plot', figure = HASHTAG_PLOT, style = {'height' : '45vh'}), className = 'body'),
                ]),
            ]),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)