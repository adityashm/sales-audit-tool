import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import hashlib
import hmac

# Page configuration
st.set_page_config(
    page_title="Sales Price Variance Audit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication configuration
# Try to load from Streamlit secrets (for production), otherwise use default
try:
    USERS = dict(st.secrets["passwords"])
except (FileNotFoundError, KeyError):
    # Default credentials for local development
    USERS = {
        "admin": "admin123",  # Username: admin, Password: admin123
        "auditor": "audit@2025",  # Username: auditor, Password: audit@2025
        "manager": "manager123"  # Username: manager, Password: manager123
    }

def check_password():
    """Returns `True` if the user has entered correct credentials."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state["username"]
        password = st.session_state["password"]
        
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["current_user"] = username
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["authenticated"] = False
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Show login form if not authenticated
    if not st.session_state["authenticated"]:
        st.markdown('<p class="main-header">🔐 Sales Price Variance Audit Tool</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Center the login form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔑 Login Required")
            st.markdown("Please enter your credentials to access the application.")
            
            st.text_input("Username", key="username", placeholder="Enter username")
            st.text_input("Password", type="password", key="password", placeholder="Enter password")
            
            st.button("🚀 Login", on_click=password_entered, use_container_width=True, type="primary")
            
            if st.session_state.get("authenticated") == False and "username" in st.session_state:
                st.error("😕 Invalid username or password. Please try again.")
            
            # Show demo credentials (remove in production)
            with st.expander("📋 Demo Credentials"):
                st.info("""
                **Available Users:**
                - Username: `admin` | Password: `admin123`
                - Username: `auditor` | Password: `audit@2025`
                - Username: `manager` | Password: `manager123`
                
                ⚠️ **Note:** Change these credentials before deploying to production!
                """)
        
        return False
    else:
        # Show logout button in sidebar
        with st.sidebar:
            st.success(f"✅ Logged in as: **{st.session_state['current_user']}**")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state["authenticated"] = False
                st.session_state["current_user"] = None
                st.rerun()
        
        return True

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def audit_material_price_variance(df, column_mapping):
    """
    Audits material sales to identify when same customer bought same material 
    on same date at different basic rates.
    
    Parameters:
    df: Input DataFrame
    column_mapping: Dictionary mapping required columns to actual column names
    """
    
    # Rename columns based on mapping
    df_renamed = df.rename(columns={
        column_mapping['material_description']: 'MATERIAL DESCRIPTION',
        column_mapping['date_column']: 'SO CREATED ON',
        column_mapping['material_code']: 'MATERIAL CODE',
        column_mapping['customer_name']: 'SOLD TO PARTY NAME',
        column_mapping['basic_rate']: 'BASIC RATE'
    })
    
    # Convert date column to datetime
    df_renamed['SO CREATED ON'] = pd.to_datetime(df_renamed['SO CREATED ON'], errors='coerce')
    
    # Remove rows with missing critical data
    df_clean = df_renamed.dropna(subset=[
        'MATERIAL CODE',
        'SO CREATED ON',
        'SOLD TO PARTY NAME',
        'BASIC RATE'
    ])
    
    # Group by customer, material code, and date
    grouped = df_clean.groupby(['SOLD TO PARTY NAME', 'MATERIAL CODE', 'SO CREATED ON'])
    
    variance_groups = []
    
    for (party_name, material_code, doc_date), group in grouped:
        unique_rates = group['BASIC RATE'].unique()
        
        if len(unique_rates) > 1:
            max_rate = group['BASIC RATE'].max()
            min_rate = group['BASIC RATE'].min()
            
            variance_groups.append({
                'Customer': party_name,
                'Material Code': material_code,
                'Date': doc_date.strftime('%Y-%m-%d'),
                'Material Description': group['MATERIAL DESCRIPTION'].iloc[0] if 'MATERIAL DESCRIPTION' in group.columns else 'N/A',
                'Max Rate': max_rate,
                'Min Rate': min_rate,
                'Difference': round(max_rate - min_rate, 2),
                'Variance %': round(((max_rate - min_rate) / min_rate) * 100, 2) if min_rate != 0 else 0
            })
    
    if variance_groups:
        variance_df = pd.DataFrame(variance_groups)
        variance_df = variance_df.sort_values('Difference', ascending=False)
        return variance_df, df_clean
    else:
        return None, df_clean

def create_excel_download(df):
    """Create an Excel file in memory for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Price Variances')
    output.seek(0)
    return output

def main():
    # Check authentication first
    if not check_password():
        return
    
    # Header
    st.markdown('<p class="main-header">📊 Sales Price Variance Audit Tool</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    st.sidebar.markdown("Map your data columns to the required fields:")
    
    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload your data file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a CSV or Excel file with your sales data"
    )
    
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.df = df
            st.session_state.uploaded_file = uploaded_file
            
            st.sidebar.success(f"✅ File loaded: {uploaded_file.name}")
            st.sidebar.info(f"📝 Total records: {len(df)}")
            
            # Column mapping section
            st.sidebar.markdown("---")
            st.sidebar.subheader("📋 Column Mapping")
            
            columns = list(df.columns)
            
            # Create column mappings
            column_mapping = {
                'material_description': st.sidebar.selectbox(
                    "Material Description Column",
                    options=columns,
                    index=columns.index('MATERIAL DESCRIPTION') if 'MATERIAL DESCRIPTION' in columns else 0,
                    help="Select the column containing material descriptions"
                ),
                'date_column': st.sidebar.selectbox(
                    "Date Column",
                    options=columns,
                    index=columns.index('SO CREATED ON') if 'SO CREATED ON' in columns else 0,
                    help="Select the column containing order/transaction dates"
                ),
                'material_code': st.sidebar.selectbox(
                    "Material Code Column",
                    options=columns,
                    index=columns.index('MATERIAL CODE') if 'MATERIAL CODE' in columns else 0,
                    help="Select the column containing material codes/SKUs"
                ),
                'customer_name': st.sidebar.selectbox(
                    "Customer Name Column",
                    options=columns,
                    index=columns.index('SOLD TO PARTY NAME') if 'SOLD TO PARTY NAME' in columns else 0,
                    help="Select the column containing customer names"
                ),
                'basic_rate': st.sidebar.selectbox(
                    "Price/Rate Column",
                    options=columns,
                    index=columns.index('BASIC RATE') if 'BASIC RATE' in columns else 0,
                    help="Select the column containing prices/rates"
                )
            }
            
            st.sidebar.markdown("---")
            analyze_button = st.sidebar.button("🔍 Analyze Data", type="primary", use_container_width=True)
            
            # Main content area
            tab1, tab2, tab3 = st.tabs(["📊 Analysis Results", "📈 Visualizations", "📄 Raw Data Preview"])
            
            with tab1:
                if analyze_button:
                    with st.spinner("Analyzing price variances..."):
                        variance_df, df_clean = audit_material_price_variance(df, column_mapping)
                        
                        if variance_df is not None and not variance_df.empty:
                            # Summary metrics
                            st.subheader("📈 Summary Statistics")
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric(
                                    "Total Variance Cases",
                                    len(variance_df),
                                    help="Number of cases where price differences were detected"
                                )
                            
                            with col2:
                                st.metric(
                                    "Avg Price Difference",
                                    f"₹{variance_df['Difference'].mean():.2f}",
                                    help="Average price difference across all variance cases"
                                )
                            
                            with col3:
                                st.metric(
                                    "Max Price Difference",
                                    f"₹{variance_df['Difference'].max():.2f}",
                                    help="Largest price difference found"
                                )
                            
                            with col4:
                                st.metric(
                                    "Total Records Analyzed",
                                    len(df_clean),
                                    help="Number of valid records after cleaning"
                                )
                            
                            st.markdown("---")
                            
                            # Variance table
                            st.subheader("🔍 Price Variance Details")
                            st.dataframe(
                                variance_df,
                                use_container_width=True,
                                height=400
                            )
                            
                            # Download section
                            st.markdown("---")
                            st.subheader("💾 Download Results")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Excel download
                                excel_file = create_excel_download(variance_df)
                                st.download_button(
                                    label="📥 Download Excel Report",
                                    data=excel_file,
                                    file_name=f"price_variance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col2:
                                # CSV download
                                csv = variance_df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="📥 Download CSV Report",
                                    data=csv,
                                    file_name=f"price_variance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            # Store in session state for visualization tab
                            st.session_state.variance_df = variance_df
                            st.session_state.df_clean = df_clean
                            
                        else:
                            st.success("✅ No price variances detected!")
                            st.info("All materials have consistent basic rates for the same customer on the same date.")
                
                else:
                    st.info("👈 Configure column mappings in the sidebar and click 'Analyze Data' to start.")
            
            with tab2:
                if 'variance_df' in st.session_state and st.session_state.variance_df is not None:
                    variance_df = st.session_state.variance_df
                    
                    st.subheader("📊 Visual Insights")
                    
                    # Top 10 variances bar chart
                    st.markdown("#### Top 10 Price Variances")
                    fig1 = px.bar(
                        variance_df.head(10),
                        x='Customer',
                        y='Difference',
                        color='Variance %',
                        hover_data=['Material Code', 'Date', 'Max Rate', 'Min Rate'],
                        title="Top 10 Price Differences by Customer",
                        labels={'Difference': 'Price Difference (₹)', 'Variance %': 'Variance (%)'}
                    )
                    fig1.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig1, use_container_width=True)
                    
                    # Distribution of price differences
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Distribution of Price Differences")
                        fig2 = px.histogram(
                            variance_df,
                            x='Difference',
                            nbins=30,
                            title="Price Difference Distribution",
                            labels={'Difference': 'Price Difference (₹)'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Variance Percentage Distribution")
                        fig3 = px.box(
                            variance_df,
                            y='Variance %',
                            title="Variance Percentage Box Plot",
                            labels={'Variance %': 'Variance (%)'}
                        )
                        st.plotly_chart(fig3, use_container_width=True)
                    
                    # Customer-wise variance count
                    st.markdown("#### Top Customers by Variance Count")
                    customer_counts = variance_df['Customer'].value_counts().head(10)
                    fig4 = px.bar(
                        x=customer_counts.index,
                        y=customer_counts.values,
                        title="Top 10 Customers with Most Price Variances",
                        labels={'x': 'Customer', 'y': 'Number of Variances'}
                    )
                    fig4.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig4, use_container_width=True)
                    
                    # Material-wise variance
                    st.markdown("#### Top Materials by Variance Count")
                    material_counts = variance_df['Material Code'].value_counts().head(10)
                    fig5 = px.pie(
                        values=material_counts.values,
                        names=material_counts.index,
                        title="Top 10 Materials with Most Price Variances"
                    )
                    st.plotly_chart(fig5, use_container_width=True)
                    
                else:
                    st.info("👈 Run the analysis first to see visualizations.")
            
            with tab3:
                st.subheader("📄 Raw Data Preview")
                st.dataframe(df.head(100), use_container_width=True)
                st.info(f"Showing first 100 rows of {len(df)} total records.")
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.exception(e)
    
    else:
        # Welcome screen
        st.markdown("""
        ### Welcome to the Sales Price Variance Audit Tool! 👋
        
        This tool helps you identify pricing inconsistencies in your sales data by detecting cases where:
        - **Same customer** 🧑‍💼
        - **Same material** 📦
        - **Same date** 📅
        - **Different prices** 💰
        
        #### How to use:
        1. **Upload your data file** (CSV or Excel) using the sidebar
        2. **Map your columns** to match the required fields
        3. **Click 'Analyze Data'** to run the audit
        4. **View insights** through interactive charts and tables
        5. **Download the report** in Excel or CSV format
        
        #### Required Data Columns:
        - Material Description
        - Date Column (Order/Transaction date)
        - Material Code/SKU
        - Customer Name
        - Price/Basic Rate
        
        ---
        
        **💡 Tip:** Make sure your data has all the required columns before uploading!
        """)
        
        # Example data structure
        with st.expander("📋 View Example Data Structure"):
            example_df = pd.DataFrame({
                'MATERIAL DESCRIPTION': ['Product A', 'Product B', 'Product C'],
                'SO CREATED ON': ['2025-01-15', '2025-01-15', '2025-01-16'],
                'MATERIAL CODE': ['MAT001', 'MAT002', 'MAT003'],
                'SOLD TO PARTY NAME': ['Customer X', 'Customer Y', 'Customer Z'],
                'BASIC RATE': [100.00, 150.00, 200.00]
            })
            st.dataframe(example_df, use_container_width=True)

if __name__ == "__main__":
    main()
