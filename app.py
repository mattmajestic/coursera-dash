import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import os
from dash.dependencies import Input, Output

# Load DataFrame from CSV
df = pd.read_csv('data.csv')

# Assuming your PDF files are stored in 'assets/coursera/' directory
PDF_DIR = 'assets/coursera'
pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Coursera Certificates Overview 🎓', className='text-light mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(f'You have {len(df)} certificates 📜 and {len(pdf_files)} PDF files.', className='text-info mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pdf-dropdown',
                options=[{'label': pdf, 'value': os.path.join(PDF_DIR, pdf)} for pdf in pdf_files],
                style={'color': 'black'},  # For visibility in the dropdown
            ),
            html.Div(id='pdf-display', className='mt-4')
        ], width=6),
        dbc.Col([
            html.H3('Certificates Data Table 📊', className='text-light mb-3'),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
                    'color': 'white',
                    'backgroundColor': '#222',
                    'border': '1px solid #444',
                },
                style_header={
                    'backgroundColor': '#333',
                    'color': 'white',
                    'border': '1px solid #444'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#303030'}
                ]
            )
        ], width=6)
    ])
], fluid=True, style={'marginTop': 20})

@app.callback(
    Output('pdf-display', 'children'),
    [Input('pdf-dropdown', 'value')]
)
def display_pdf(selected_pdf):
    if selected_pdf is not None:
        # Embedding the PDF within an iframe
        return html.Iframe(src=selected_pdf, style={'height': '500px', 'width': '100%'})
    return dbc.Alert("Please select a PDF file to view.", color="secondary")

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
