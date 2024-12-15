import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Real-Time Alluvial Chart for Bank Transactions")

# Step 1: Dummy Data for Default Use
def get_dummy_data():
    return pd.DataFrame({
        'Region': ['Region A', 'Region A', 'Region B', 'Region B'],
        'Subregion': ['Subregion A1', 'Subregion A2', 'Subregion B1', 'Subregion B2'],
        'Area': ['Area A1', 'Area A2', 'Area B1', 'Area B2'],
        'Branch': ['Branch A1', 'Branch A2', 'Branch B1', 'Branch B2'],
        'Account Type': ['Savings', 'Current', 'Business', 'Savings'],
        'Transaction To': ['Bank X', 'Bank Y', 'Bank Z', 'Bank X'],
        'Credit': [100000, 150000, 200000, 250000],
        'Debit': [50000, 70000, 120000, 90000]
    })

# Step 2: File Upload for User Data
uploaded_file = st.file_uploader("Upload your data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Load the uploaded file
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
else:
    # Use dummy data if no file is uploaded
    st.info("Using default dummy data. Upload a file to use your own data.")
    data = get_dummy_data()

# Display the data
st.subheader("Uploaded Data")
st.dataframe(data)

# Step 3: Process Data for Sankey Diagram
data['Credit'] = data['Credit'].fillna(0)
data['Debit'] = data['Debit'].fillna(0)
data['Transaction Value'] = data['Credit'] + data['Debit']

# Create unique nodes
nodes = pd.concat([
    data['Region'],
    data['Subregion'],
    data['Area'],
    data['Branch'],
    data['Account Type'],
    data['Transaction To']
]).unique()

# Map nodes to indices
node_indices = {node: i for i, node in enumerate(nodes)}

# Create Sankey links
links = {'source': [], 'target': [], 'value': []}

for _, row in data.iterrows():
    # Region -> Subregion
    links['source'].append(node_indices[row['Region']])
    links['target'].append(node_indices[row['Subregion']])
    links['value'].append(row['Transaction Value'])

    # Subregion -> Area
    links['source'].append(node_indices[row['Subregion']])
    links['target'].append(node_indices[row['Area']])
    links['value'].append(row['Transaction Value'])

    # Area -> Branch
    links['source'].append(node_indices[row['Area']])
    links['target'].append(node_indices[row['Branch']])
    links['value'].append(row['Transaction Value'])

    # Branch -> Account Type
    links['source'].append(node_indices[row['Branch']])
    links['target'].append(node_indices[row['Account Type']])
    links['value'].append(row['Transaction Value'])

    # Account Type -> Transaction Destination
    links['source'].append(node_indices[row['Account Type']])
    links['target'].append(node_indices[row['Transaction To']])
    links['value'].append(row['Transaction Value'])

# Step 4: Create Sankey Diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=list(nodes),
    ),
    link=dict(
        source=links['source'],
        target=links['target'],
        value=links['value'],
    )
))

# Step 5: Display the Chart in Streamlit
st.subheader("Alluvial Chart (Sankey Diagram)")
st.plotly_chart(fig, use_container_width=True)
