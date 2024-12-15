import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Real-Time Editable Alluvial Chart (Sankey Diagram)")

# Step 1: Define Dummy Data
def get_dummy_data():
    return pd.DataFrame({
        'Region': ['Region A', 'Region A', 'Region B', 'Region B'],
        'Subregion': ['Subregion A1', 'Subregion A2', 'Subregion B1', 'Subregion B2'],
        'Area': ['Area A1', 'Area A2', 'Area B1', 'Area B2'],
        'Branch': ['Branch A1', 'Branch A2', 'Branch B1', 'Branch B2'],
        'Account Type': ['Savings', 'Current', 'Business', 'Savings'],
        'Transaction To': ['Bank X', 'Bank Y', 'Bank Z', 'Bank X'],
        'Credit': [100000, 150000, 0, 250000],
        'Debit': [0, 0, 200000, 0]
    })

# Step 2: Allow Users to Edit Dummy Data
st.subheader("Editable Data")
data = get_dummy_data()
edited_data = st.experimental_data_editor(data, use_container_width=True, num_rows="dynamic")

# Step 3: Process the Edited Data for Sankey Diagram
edited_data['Credit'] = edited_data['Credit'].fillna(0)
edited_data['Debit'] = edited_data['Debit'].fillna(0)
edited_data['Transaction Value'] = edited_data['Credit'] + edited_data['Debit']

# Normalize transaction values to reduce line thickness
edited_data['Transaction Value (Normalized)'] = edited_data['Transaction Value'] / 1000  # Scale down by dividing by 1000

# Step 4: Validate Columns
required_columns = ['Region', 'Subregion', 'Area', 'Branch', 'Account Type', 'Transaction To', 'Transaction Value (Normalized)']
missing_columns = [col for col in required_columns if col not in edited_data.columns]

if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}")
else:
    # Create unique nodes
    nodes = pd.concat([
        edited_data['Region'],
        edited_data['Subregion'],
        edited_data['Area'],
        edited_data['Branch'],
        edited_data['Account Type'],
        edited_data['Transaction To']
    ]).unique()

    # Map nodes to indices for the Sankey diagram
    node_indices = {node: i for i, node in enumerate(nodes)}

    # Create Sankey links
    links = {'source': [], 'target': [], 'value': [], 'color': []}
    colors = {
        'Bank X': 'blue',
        'Bank Y': 'red',
        'Bank Z': 'green',
        'Region A': 'purple',
        'Region B': 'orange'
    }

    for _, row in edited_data.iterrows():
        # Region -> Subregion
        links['source'].append(node_indices[row['Region']])
        links['target'].append(node_indices[row['Subregion']])
        links['value'].append(row['Transaction Value (Normalized)'])
        links['color'].append(colors.get(row['Transaction To'], 'gray'))

        # Subregion -> Area
        links['source'].append(node_indices[row['Subregion']])
        links['target'].append(node_indices[row['Area']])
        links['value'].append(row['Transaction Value (Normalized)'])
        links['color'].append(colors.get(row['Transaction To'], 'gray'))

        # Area -> Branch
        links['source'].append(node_indices[row['Area']])
        links['target'].append(node_indices[row['Branch']])
        links['value'].append(row['Transaction Value (Normalized)'])
        links['color'].append(colors.get(row['Transaction To'], 'gray'))

        # Branch -> Account Type
        links['source'].append(node_indices[row['Branch']])
        links['target'].append(node_indices[row['Account Type']])
        links['value'].append(row['Transaction Value (Normalized)'])
        links['color'].append(colors.get(row['Transaction To'], 'gray'))

        # Account Type -> Transaction Destination
        links['source'].append(node_indices[row['Account Type']])
        links['target'].append(node_indices[row['Transaction To']])
        links['value'].append(row['Transaction Value (Normalized)'])
        links['color'].append(colors.get(row['Transaction To'], 'gray'))

    # Step 5: Create Sankey Diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=30,  # Increased padding for better spacing
            thickness=20,
            line=dict(color="black", width=0.5),
            label=list(nodes),
        ),
        link=dict(
            source=links['source'],
            target=links['target'],
            value=links['value'],
            color=links['color'],  # Assign colors to links
            opacity=0.6  # Reduced opacity for better visibility
        )
    ))

    # Step 6: Display the Chart in Streamlit
    st.subheader("Alluvial Chart (Sankey Diagram) with Reduced Line Thickness")
    st.plotly_chart(fig, use_container_width=True)
