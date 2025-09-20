import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os

from ai_agent import DocumentProcessor, create_sample_documents


# Initialize AI agent
agent = DocumentProcessor()

# Create sample documents on startup
sample_dir = create_sample_documents()

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🤖 AI Document Processing Agent", style={'textAlign': 'center', 'color': '#2E8B57'}),
    
    html.Div([
        html.H3("📄 Document Input"),
        dcc.Textarea(
            id='document-input',
            placeholder='Paste your document content here or use one of the sample documents below...',
            style={'width': '100%', 'height': 200, 'marginBottom': '10px'},
            value=''
        ),
        
        html.Div([
            html.H4("Sample Documents:"),
            html.Button("Project Setup", id="btn-sample1", className="sample-btn", style={'margin': '5px'}),
            html.Button("Data Pipeline", id="btn-sample2", className="sample-btn", style={'margin': '5px'}),
            html.Button("Maintenance", id="btn-sample3", className="sample-btn", style={'margin': '5px'}),
        ], style={'marginBottom': '20px'}),
        
        html.Button("🚀 Process Document", id="process-btn", 
                   style={'backgroundColor': '#2E8B57', 'color': 'white', 'padding': '10px 20px', 
                         'border': 'none', 'borderRadius': '5px', 'fontSize': '16px'}),
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
    
    html.Div([
        html.H3("📊 Processing Results"),
        html.Div(id='processing-status', style={'marginBottom': '20px'}),
        html.Div(id='execution-summary', style={'marginBottom': '20px'}),
        dcc.Graph(id='process-chart'),
        html.Div(id='detailed-results')
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
    
], style={'fontFamily': 'Arial, sans-serif'})


@app.callback(
    Output('document-input', 'value'),
    [Input('btn-sample1', 'n_clicks'),
     Input('btn-sample2', 'n_clicks'),
     Input('btn-sample3', 'n_clicks')],
    prevent_initial_call=True
)
def load_sample_document(btn1, btn2, btn3):
    """Load sample documents into the text area."""
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    sample_files = {
        'btn-sample1': 'project_setup.txt',
        'btn-sample2': 'data_pipeline.txt', 
        'btn-sample3': 'maintenance_procedure.txt'
    }
    
    if button_id in sample_files:
        filepath = os.path.join(sample_dir, sample_files[button_id])
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except:
            return "Error loading sample document"
    
    return dash.no_update


@app.callback(
    [Output('processing-status', 'children'),
     Output('execution-summary', 'children'),
     Output('process-chart', 'figure'),
     Output('detailed-results', 'children')],
    [Input('process-btn', 'n_clicks')],
    [State('document-input', 'value')],
    prevent_initial_call=True
)
def process_document(n_clicks, document_text):
    """Process the document and display results."""
    if not document_text or not document_text.strip():
        return (
            html.Div("⚠️ Please enter some document text to process", 
                    style={'color': 'orange', 'fontWeight': 'bold'}),
            "", {}, ""
        )
    
    # Process the document
    results = agent.process_document(document_text)
    
    # Status display
    status_div = html.Div([
        html.H4("✅ Processing Complete!", style={'color': 'green'}),
        html.P(f"📄 Document length: {results['document_length']} characters"),
        html.P(f"🔍 Instructions found: {results['instructions_found']}"),
        html.P(f"📅 Processed at: {results['processed_at']}")
    ], style={'backgroundColor': '#f0f8f0', 'padding': '15px', 'borderRadius': '5px'})
    
    # Execution summary
    summary = results['execution_summary']
    summary_div = html.Div([
        html.H4("📈 Execution Summary"),
        html.Div([
            html.Div([
                html.H5(f"{summary['total']}", style={'margin': '0', 'fontSize': '24px', 'color': '#333'}),
                html.P("Total", style={'margin': '0', 'color': '#666'})
            ], style={'textAlign': 'center', 'backgroundColor': '#e6f3ff', 'padding': '10px', 'borderRadius': '5px', 'width': '30%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.H5(f"{summary['successful']}", style={'margin': '0', 'fontSize': '24px', 'color': 'green'}),
                html.P("Successful", style={'margin': '0', 'color': '#666'})
            ], style={'textAlign': 'center', 'backgroundColor': '#e6ffe6', 'padding': '10px', 'borderRadius': '5px', 'width': '30%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.H5(f"{summary['failed']}", style={'margin': '0', 'fontSize': '24px', 'color': 'red'}),
                html.P("Failed", style={'margin': '0', 'color': '#666'})
            ], style={'textAlign': 'center', 'backgroundColor': '#ffe6e6', 'padding': '10px', 'borderRadius': '5px', 'width': '30%', 'display': 'inline-block', 'margin': '1%'}),
        ])
    ])
    
    # Process type chart
    if summary['processes']:
        process_data = []
        for process_type, stats in summary['processes'].items():
            process_data.append({
                'Process Type': process_type.replace('_', ' ').title(),
                'Successful': stats['successful'],
                'Failed': stats['failed']
            })
        
        df_chart = pd.DataFrame(process_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Successful',
            x=df_chart['Process Type'],
            y=df_chart['Successful'],
            marker_color='green'
        ))
        fig.add_trace(go.Bar(
            name='Failed',
            x=df_chart['Process Type'],
            y=df_chart['Failed'],
            marker_color='red'
        ))
        
        fig.update_layout(
            title='Execution Results by Process Type',
            barmode='stack',
            xaxis_title='Process Type',
            yaxis_title='Number of Instructions'
        )
    else:
        fig = {}
    
    # Detailed results
    detailed_div = html.Div([
        html.H4("🔍 Detailed Execution Results"),
        html.Div([
            html.Div([
                html.H5(f"🔹 {result['process_type'].replace('_', ' ').title()}", 
                        style={'color': '#2E8B57', 'marginBottom': '5px'}),
                html.P(f"📝 {result['instruction']}", style={'marginBottom': '5px'}),
                html.P([
                    html.Span("Status: ", style={'fontWeight': 'bold'}),
                    html.Span(f"{'✅' if result['success'] else '❌'} {result['status']}", 
                             style={'color': 'green' if result['success'] else 'red'}),
                    html.Span(f" ({result['duration_ms']}ms)", style={'color': '#666', 'fontSize': '12px'})
                ], style={'marginBottom': '0'})
            ], style={'backgroundColor': '#f9f9f9', 'padding': '10px', 'marginBottom': '10px', 'borderRadius': '5px'})
            for result in results['execution_results']
        ])
    ])
    
    return status_div, summary_div, fig, detailed_div


if __name__ == "__main__":
    print("🤖 Starting AI Document Processing Agent Dashboard...")
    print(f"📁 Sample documents available at: {sample_dir}")
    print("🌐 Open http://127.0.0.1:8050/ in your browser")
    app.run(debug=True)