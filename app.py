import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Enhanced Real-Time Alluvial Chart for Bank Transactions")

# Step 1: File Upload for User Data
uploaded_file = st.file_uploader("Upload your data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Load the uploaded file
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Display the uploaded data
    st.subheader("Uploaded Data")
    st.dataframe(data)

    # Step 2: Process Data for Sankey Diagram
    # Fill missing values
    data['Credit'] = data['Credit'].fillna(0)
    data['Debit'] = data['Debit'].fillna(0)
    data['Transaction Value'] = data['Credit'] + data['Debit']

    # Validate required columns
    required_columns = ['Region', 'Subregion', 'Area', 'Branch', 'Account Type', 'Transaction To', 'Transaction Value']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
    else:
        # Create unique nodes
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

        # Create Sankey links
        links = {'source': [], 'target': [], 'value': [], 'color': []}
        colors = {
            'Mezan': 'blue',
            'MCB': 'green',
            'Lahore4': 'red',
            'Lahore3': 'purple'
        }

        for _, row in data.iterrows():
            # Region -> Subregion
            links['source'].append(node_indices[row['Region']])
            links['target'].append(node_indices[row['Subregion']])
            links['value'].append(row['Transaction Value'])
            links['color'].append(colors.get(row['Transaction To'], 'gray'))

            # Subregion -> Area
            links['source'].append(node_indices[row['Subregion']])
            links['target'].append(node_indices[row['Area']])
            links['value'].append(row['Transaction Value'])
            links['color'].append(colors.get(row['Transaction To'], 'gray'))

            # Area -> Branch
            links['source'].append(node_indices[row['Area']])
            links['target'].append(node_indices[row['Branch']])
            links['value'].append(row['Transaction Value'])
            links['color'].append(colors.get(row['Transaction To'], 'gray'))

            # Branch -> Account Type
            links['source'].append(node_indices[row['Branch']])
            links['target'].append(node_indices[row['Account Type']])
            links['value'].append(row['Transaction Value'])
            links['color'].append(colors.get(row['Transaction To'], 'gray'))

            # Account Type -> Transaction Destination
            links['source'].append(node_indices[row['Account Type']])
            links['target'].append(node_indices[row['Transaction To']])
            links['value'].append(row['Transaction Value'])
            links['color'].append(colors.get(row['Transaction To'], 'gray'))

        # Step 3: Create Sankey Diagram
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
            )
        ))

        # Step 4: Display the Chart in Streamlit
        st.subheader("Enhanced Alluvial Chart (Sankey Diagram)")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Upload a file to generate the Alluvial Chart.")
