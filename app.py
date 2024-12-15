import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Alluvial Chart (Sankey Diagram) - Bank Transactions")

# Step 1: Upload Data
st.subheader("Upload Your Dataset")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with your transaction data", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load uploaded data
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Step 2: Fill Missing Values
    st.subheader("Preview of Uploaded Data")
    st.write("Make sure your dataset has the following columns: Region, Subregion, Area, Branch, Account Type, Transaction To, Credit, Debit")
    st.dataframe(data)

    # Fill missing Credit and Debit values with 0
    data['Credit'] = data['Credit'].fillna(0)
    data['Debit'] = data['Debit'].fillna(0)

    # Calculate total transaction value
    data['Transaction Value'] = data['Credit'] + data['Debit']

    # Step 3: Create Unique List of Nodes
    nodes = pd.concat([
        data['Region'],
        data['Subregion'],
        data['Area'],
        data['Branch'],
        data['Account Type'],
        data['Transaction To']
    ]).unique()

    # Map nodes to indices for the Sankey diagram
    node_indices = {node: i for i, node in enumerate(nodes)}

    # Step 4: Create Sankey Links
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

    # Step 5: Create Sankey Diagram
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

    # Step 6: Add Title and Display Chart
    fig.update_layout(title_text="Alluvial Chart (Sankey Diagram) - Bank Transactions", font_size=10)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to generate the Sankey diagram.")
