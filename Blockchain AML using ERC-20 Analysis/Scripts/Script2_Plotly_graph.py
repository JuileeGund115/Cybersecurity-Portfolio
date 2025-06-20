import dash
import dash_cytoscape as cyto
from dash import html
import pandas as pd

app = dash.Dash(__name__)

# Function to shorten a string for display
def shorten_string(s, start_chars=6, end_chars=4):
    return s[:start_chars] + '...' + s[-end_chars:]

# Function to create elements from the Excel file
def create_elements_from_excel(file_path):
    df = pd.read_excel(file_path)
    elements = []
    
    nodes = set()

    for _, row in df.iterrows():
        sender = row['Sender Name']
        receiver = row['Receiver Name']
        amount = row['Amount']
        token_symbol = row.get('Token Symbol', 'ETH')
        tx_hash = row['Transaction Hash']
        
        # Shorten the sender, receiver, and transaction hash for display
        short_sender = shorten_string(sender) if sender.startswith('0x') else sender
        short_receiver = shorten_string(receiver) if receiver.startswith('0x') else receiver
        short_tx_hash = shorten_string(tx_hash)
        
        if sender not in nodes:
            elements.append({'data': {'id': sender, 'label': short_sender}})
            nodes.add(sender)
        if receiver not in nodes:
            elements.append({'data': {'id': receiver, 'label': short_receiver}})
            nodes.add(receiver)

        # Create a unique node ID for the transaction hash
        tx_node_id = f'tx_{tx_hash}'

        if tx_node_id not in nodes:
            tx_label = f"{amount} {token_symbol}\n tx:{short_tx_hash}"
            elements.append({'data': {'id': tx_node_id, 'label': tx_label, 'type': 'transaction'}})
            nodes.add(tx_node_id)
        
        # Create unique edge ID based on transaction details
        edge_id = f'{sender}_to_{tx_node_id}_{amount}_{token_symbol}'
        elements.append({
            'data': {
                'id': edge_id, 
                'source': sender, 
                'target': tx_node_id, 
                'label': f'{amount} {token_symbol}',  
                'type': 'transaction_edge',
            }
        })

        edge_id = f'{tx_node_id}_to_{receiver}_{amount}_{token_symbol}'
        elements.append({
            'data': {
                'id': edge_id, 
                'source': tx_node_id, 
                'target': receiver, 
                'label': f'{amount} {token_symbol}',
                'type': 'transaction_edge',
            }
        })
    
    return elements

# Path to the Excel file
excel_file_path = 'transaction_data2.xlsx'

# Create elements from the Excel file
elements = create_elements_from_excel(excel_file_path)

# Define the layout of the Dash app
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'cose'},  
        style={'width': '100%', 'height': '1250px'},
        stylesheet=[
            # Node styles
            {'selector': 'node', 'style': {
                'content': 'data(label)',
                'text-valign': 'top', 
                'text-halign': 'center',
                'color': 'black',
                'background-color': 'darkturquoise',
                'background-opacity': 0.9,
                'width': 8.5,  
                'height': 8.6, 
                'font-size': 7,
                'text-margin-y': '0.5px'
            }},
            # Edge styles with arrows
            {'selector': 'edge[type="transaction_edge"]', 'style': {
                'width': 0.7,  
                'line-color': 'darkgrey', 
                'target-arrow-color': 'darkgrey',  
                'mid-target-arrow-shape': 'triangle',
                'arrow-scale': 0.5,  
                'curve-style': 'bezier', 
                'label': 'data(label)',  
                'font-size': 6,  
                'color': 'black',
                'text-rotation': 'autorotate', 
                'text-offset': '10px',  
                'text-margin-y': '5px',  
            }},
            # Styles for transaction nodes
            {'selector': 'node[type="transaction"]', 'style': {
                'background-color': '#9467bd',
                'shape': 'ellipse',
                'font-size': 7,  
                'text-wrap': 'wrap', 
                'text-max-width': '120px', 
                'text-valign': 'top',  
                'text-halign': 'center',
                'text-margin-y': '0.5px'
            }},
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
