import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Improved Dynamic Alluvial Chart (Sankey Diagram)")

# Step 1: Define Editable Dummy Data
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

# Step 2: Editable Data
st.subheader("Edit the Data")
data = get_dummy_data()
edited_data = st.data_editor(data, use_container_width=True, num_rows="dynamic")

# Step 3: Validate Edited Data
if edited_data.empty:
    st.error("No data available. Please add rows to the table.")
else:
    # Step 4: Process the Data
    edited_data['Credit'] = edited_data['Credit'].fillna(0)
    edited_data['Debit'] = edited_data['Debit'].fillna(0)
    edited_data['Transaction Value'] = edited_data['Credit'] + edited_data['Debit']

    # Normalize transaction values for better visibility
    edited_data['Transaction Value (Normalized)'] = (
        edited_data['Transaction Value'] / edited_data['Transaction Value'].max() * 100
    )

    # Create nodes and links for the Sankey diagram
    nodes = pd.concat([
        edited_data['Region'],
        edited_data['Subregion'],
        edited_data['Area'],
        edited_data['Branch'],
        edited_data['Account Type'],
        edited_data['Transaction To']
    ]).unique()

    node_indices = {node: i for i, node in enumerate(nodes)}
    links = {'source': [], 'target': [], 'value': [], 'color': []}
    colors = {'Bank X': 'blue', 'Bank Y': 'red', 'Bank Z': 'green'}

    for _, row in edited_data.iterrows():
        links['source'].extend([
            node_indices[row['Region']],
            node_indices[row['Subregion']],
            node_indices[row['Area']],
            node_indices[row['Branch']],
            node_indices[row['Account Type']]
        ])
        links['target'].extend([
            node_indices[row['Subregion']],
            node_indices[row['Area']],
            node_indices[row['Branch']],
            node_indices[row['Account Type']],
            node_indices[row['Transaction To']]
        ])
        links['value'].extend([row['Transaction Value (Normalized)']] * 5)
        links['color'].extend([colors.get(row['Transaction To'], 'gray')] * 5)

    # Validate data integrity for Sankey diagram
    if len(links['source']) == len(links['target']) == len(links['value']):
        # Step 5: Create Sankey Diagram
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=50,  # Increased padding for more space between nodes
                thickness=10,  # Reduced node thickness
                line=dict(color="black", width=0.5),
                label=list(nodes),
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value'],
                color=links['color'],
            )
        ))

        # Step 6: Display the Chart
        st.subheader("Improved Alluvial Chart (Sankey Diagram)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Mismatch in source, target, and value lengths. Check your data.")
