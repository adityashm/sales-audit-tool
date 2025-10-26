import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import io
import hashlib
import hmac
from difflib import get_close_matches
import time
import json

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
            
            st.button("🚀 Login", on_click=password_entered, type="primary", use_container_width=True)
            
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
        font-weight: 800;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        letter-spacing: 0.3px;
    }
    .metric-card {
        background-color: #f5f7fb;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }
    .stDataFrame, .stTable {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
        .stMetric {
            font-size: 0.9rem;
        }
        [data-testid="column"] {
            min-width: 100% !important;
        }
    }
    
    /* Health check badges */
    .health-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .badge-success { background: #d4edda; color: #155724; }
    .badge-warning { background: #fff3cd; color: #856404; }
    .badge-danger { background: #f8d7da; color: #721c24; }
    
    /* Keyboard shortcuts hint */
    .shortcut-hint {
        font-size: 0.75rem;
        color: #666;
        font-family: monospace;
        background: #f0f0f0;
        padding: 2px 6px;
        border-radius: 3px;
        margin-left: 8px;
    }
    </style>
""", unsafe_allow_html=True)

def audit_material_price_variance(df, column_mapping, *, date_format=None, dayfirst=False):
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
    
    # Ensure numeric for BASIC RATE
    df_renamed['BASIC RATE'] = pd.to_numeric(df_renamed['BASIC RATE'], errors='coerce')
    # Convert date column to datetime
    if date_format:
        df_renamed['SO CREATED ON'] = pd.to_datetime(df_renamed['SO CREATED ON'], format=date_format, errors='coerce')
    else:
        df_renamed['SO CREATED ON'] = pd.to_datetime(df_renamed['SO CREATED ON'], errors='coerce', dayfirst=dayfirst)
    
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

def audit_cross_customer_variance(df, column_mapping, *, date_format=None, dayfirst=False):
    """
    Audits sales to identify cases where on the same date the same material code
    was sold to DIFFERENT customers at DIFFERENT prices.

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

    # Ensure numeric for BASIC RATE
    df_renamed['BASIC RATE'] = pd.to_numeric(df_renamed['BASIC RATE'], errors='coerce')
    # Convert date column to datetime
    if date_format:
        df_renamed['SO CREATED ON'] = pd.to_datetime(df_renamed['SO CREATED ON'], format=date_format, errors='coerce')
    else:
        df_renamed['SO CREATED ON'] = pd.to_datetime(df_renamed['SO CREATED ON'], errors='coerce', dayfirst=dayfirst)

    # Remove rows with missing critical data
    df_clean = df_renamed.dropna(subset=[
        'MATERIAL CODE',
        'SO CREATED ON',
        'SOLD TO PARTY NAME',
        'BASIC RATE'
    ])

    # For each (Material Code, Date), compare prices across different customers
    results = []

    # Aggregate to customer-level first (to avoid within-customer duplicates)
    cust_level = (
        df_clean
        .groupby(['MATERIAL CODE', 'SO CREATED ON', 'SOLD TO PARTY NAME'], as_index=False)
        .agg({
            'BASIC RATE': 'mean',
            'MATERIAL DESCRIPTION': 'first'
        })
        .rename(columns={'BASIC RATE': 'CUSTOMER AVG RATE'})
    )

    for (material_code, doc_date), grp in cust_level.groupby(['MATERIAL CODE', 'SO CREATED ON']):
        # Unique rates across customers
        unique_rates = grp['CUSTOMER AVG RATE'].round(6).unique()
        if len(unique_rates) > 1:
            # Identify min/max rate and corresponding customers
            idx_min = grp['CUSTOMER AVG RATE'].idxmin()
            idx_max = grp['CUSTOMER AVG RATE'].idxmax()
            row_min = grp.loc[idx_min]
            row_max = grp.loc[idx_max]

            min_rate = float(row_min['CUSTOMER AVG RATE'])
            max_rate = float(row_max['CUSTOMER AVG RATE'])

            # Build a compact list of customer -> rate for context (top 5 by deviation)
            sample_customers = (
                grp[['SOLD TO PARTY NAME', 'CUSTOMER AVG RATE']]
                .sort_values('CUSTOMER AVG RATE')
            )

            results.append({
                'Material Code': material_code,
                'Date': pd.to_datetime(doc_date).strftime('%Y-%m-%d'),
                'Material Description': row_min.get('MATERIAL DESCRIPTION', 'N/A'),
                'Min Rate': round(min_rate, 2),
                'Min Customer': row_min['SOLD TO PARTY NAME'],
                'Max Rate': round(max_rate, 2),
                'Max Customer': row_max['SOLD TO PARTY NAME'],
                'Difference': round(max_rate - min_rate, 2),
                'Variance %': round(((max_rate - min_rate) / min_rate) * 100, 2) if min_rate != 0 else 0,
                'Unique Customers': grp['SOLD TO PARTY NAME'].nunique(),
            })

    if results:
        out_df = pd.DataFrame(results).sort_values('Difference', ascending=False)
        return out_df, df_clean
    else:
        return None, df_clean

def create_excel_download(df, metadata=None, quality_issues=None):
    """Create an enhanced multi-sheet Excel file in memory for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main variance sheet
        df.to_excel(writer, index=False, sheet_name='Price Variances')
        
        # Metadata sheet
        if metadata:
            meta_df = pd.DataFrame(list(metadata.items()), columns=['Property', 'Value'])
            meta_df.to_excel(writer, index=False, sheet_name='Metadata')
        
        # Data quality sheet
        if quality_issues:
            quality_data = []
            if quality_issues.get('missing'):
                for col, count in quality_issues['missing'].items():
                    quality_data.append({'Issue Type': 'Missing Values', 'Column': col, 'Count': count})
            if quality_issues.get('duplicates'):
                quality_data.append({'Issue Type': 'Duplicate Rows', 'Column': 'All', 'Count': quality_issues['duplicates']})
            
            if quality_data:
                quality_df = pd.DataFrame(quality_data)
                quality_df.to_excel(writer, index=False, sheet_name='Data Quality')
    
    output.seek(0)
    return output

@st.cache_data(show_spinner=False)
def _read_uploaded_file(name: str, file_bytes: bytes) -> pd.DataFrame:
    """Cached reader for uploaded file content."""
    if name.lower().endswith('.csv'):
        return pd.read_csv(io.BytesIO(file_bytes))
    return pd.read_excel(io.BytesIO(file_bytes))

def analyze_data_quality(df):
    """Analyze data quality and return issues."""
    issues = {
        'missing': {},
        'duplicates': 0,
        'non_numeric_prices': 0,
        'date_issues': 0,
        'customer_inconsistencies': []
    }
    
    # Check missing values
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            issues['missing'][col] = missing_count
    
    # Check duplicates
    issues['duplicates'] = df.duplicated().sum()
    
    return issues

def auto_detect_columns(df_columns):
    """Auto-detect column mappings based on common patterns."""
    column_patterns = {
        'material_description': ['material', 'description', 'product', 'item', 'matl'],
        'date_column': ['date', 'created', 'order date', 'so created', 'transaction'],
        'material_code': ['material code', 'mat code', 'sku', 'product code', 'item code', 'matl code'],
        'customer_name': ['customer', 'party', 'sold to', 'client', 'buyer'],
        'basic_rate': ['rate', 'price', 'basic rate', 'unit price', 'amount']
    }
    
    detected = {}
    for field, patterns in column_patterns.items():
        for col in df_columns:
            col_lower = col.lower()
            matches = get_close_matches(col_lower, patterns, n=1, cutoff=0.6)
            if matches:
                detected[field] = col
                break
    
    return detected

def save_mapping_to_session(column_mapping):
    """Save column mapping to session state."""
    st.session_state['saved_mapping'] = column_mapping
    st.session_state['mapping_timestamp'] = datetime.now().isoformat()

def load_mapping_from_session():
    """Load saved column mapping from session state."""
    return st.session_state.get('saved_mapping', {})

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
            file_bytes = uploaded_file.getvalue()
            df = _read_uploaded_file(uploaded_file.name, file_bytes)
            
            st.session_state.df = df
            st.session_state.uploaded_file = uploaded_file
            
            st.sidebar.success(f"✅ File loaded: {uploaded_file.name}")
            st.sidebar.info(f"📝 Total records: {len(df)}")
            
            # Data Health Check
            st.sidebar.markdown("---")
            with st.sidebar.expander("🏥 Data Health Check", expanded=False):
                quality_issues = analyze_data_quality(df)
                
                # Missing values
                if quality_issues['missing']:
                    st.warning(f"⚠️ Missing values found in {len(quality_issues['missing'])} columns")
                    for col, count in list(quality_issues['missing'].items())[:3]:
                        st.markdown(f"- **{col}**: {count} missing")
                    if len(quality_issues['missing']) > 3:
                        st.markdown(f"... and {len(quality_issues['missing']) - 3} more")
                else:
                    st.success("✅ No missing values")
                
                # Duplicates
                if quality_issues['duplicates'] > 0:
                    st.warning(f"⚠️ {quality_issues['duplicates']} duplicate rows found")
                else:
                    st.success("✅ No duplicate rows")
                
                st.info("💡 Quality report included in Excel download")
            
            # Column mapping section
            st.sidebar.markdown("---")
            st.sidebar.subheader("📋 Column Mapping")
            
            columns = list(df.columns)
            
            # Auto-detect and smart mapping
            col1, col2 = st.sidebar.columns([2, 1])
            with col1:
                if st.button("🔍 Auto-Detect Columns", use_container_width=True):
                    detected = auto_detect_columns(columns)
                    if detected:
                        st.session_state['auto_detected'] = detected
                        st.success(f"Found {len(detected)} matches!")
                        st.rerun()
            
            with col2:
                saved_mapping = load_mapping_from_session()
                if saved_mapping and st.button("📥 Load Saved", use_container_width=True, help="Load previous mapping"):
                    st.session_state['auto_detected'] = saved_mapping
                    st.rerun()
            
            # Get auto-detected or manual mappings
            auto_detected = st.session_state.get('auto_detected', {})
            if auto_detected is None:
                auto_detected = {}
            
            # Create column mappings with auto-detection
            column_mapping = {
                'material_description': st.sidebar.selectbox(
                    "Material Description Column",
                    options=columns,
                    index=columns.index(auto_detected.get('material_description', columns[0])) if auto_detected.get('material_description') in columns else (columns.index('MATERIAL DESCRIPTION') if 'MATERIAL DESCRIPTION' in columns else 0),
                    help="Select the column containing material descriptions"
                ),
                'date_column': st.sidebar.selectbox(
                    "Date Column",
                    options=columns,
                    index=columns.index(auto_detected.get('date_column', columns[0])) if auto_detected.get('date_column') in columns else (columns.index('SO CREATED ON') if 'SO CREATED ON' in columns else 0),
                    help="Select the column containing order/transaction dates"
                ),
                'material_code': st.sidebar.selectbox(
                    "Material Code Column",
                    options=columns,
                    index=columns.index(auto_detected.get('material_code', columns[0])) if auto_detected.get('material_code') in columns else (columns.index('MATERIAL CODE') if 'MATERIAL CODE' in columns else 0),
                    help="Select the column containing material codes/SKUs"
                ),
                'customer_name': st.sidebar.selectbox(
                    "Customer Name Column",
                    options=columns,
                    index=columns.index(auto_detected.get('customer_name', columns[0])) if auto_detected.get('customer_name') in columns else (columns.index('SOLD TO PARTY NAME') if 'SOLD TO PARTY NAME' in columns else 0),
                    help="Select the column containing customer names"
                ),
                'basic_rate': st.sidebar.selectbox(
                    "Price/Rate Column",
                    options=columns,
                    index=columns.index(auto_detected.get('basic_rate', columns[0])) if auto_detected.get('basic_rate') in columns else (columns.index('BASIC RATE') if 'BASIC RATE' in columns else 0),
                    help="Select the column containing prices/rates"
                )
            }
            
            # Save current mapping
            save_mapping_to_session(column_mapping)
            
            # Date parsing options
            st.sidebar.markdown("---")
            with st.sidebar.expander("🗓️ Date parsing options", expanded=False):
                date_format = st.text_input(
                    "Custom date format (optional)", value="",
                    help="Example: %d/%m/%Y or %Y-%m-%d. Leave empty to auto-detect."
                )
                dayfirst = st.checkbox("Day comes first (DD/MM/YYYY)", value=False)

            # Analysis mode selection
            st.sidebar.markdown("---")
            analysis_mode = st.sidebar.radio(
                "Choose Analysis Mode",
                options=(
                    "Within Customer (same customer + material + date)",
                    "Across Customers (same material + date, different customers)"
                ),
                index=0,
                help="Pick whether to check price inconsistencies within the same customer, or across different customers on the same date."
            )

            # Threshold and filters
            st.sidebar.markdown("---")
            with st.sidebar.expander("🎯 Filters & Quick Actions", expanded=True):
                # Initialize default values from session state or use defaults
                default_min_diff = st.session_state.get('quick_filter_diff', 0.0)
                default_min_var = st.session_state.get('quick_filter_var', 0.0)
                
                col1, col2 = st.columns(2)
                with col1:
                    min_diff = st.number_input("Min Difference (₹)", min_value=0.0, value=default_min_diff, step=0.5, key="min_diff_filter")
                with col2:
                    min_var = st.number_input("Min Variance %", min_value=0.0, value=default_min_var, step=0.5, key="min_var_filter")
                
                # Quick filter presets
                st.markdown("**Quick Filters:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔥 High", help="Difference >₹100", use_container_width=True):
                        st.session_state['quick_filter_diff'] = 100.0
                        st.rerun()
                with col2:
                    if st.button("⚡ Medium", help="Difference >₹50", use_container_width=True):
                        st.session_state['quick_filter_diff'] = 50.0
                        st.rerun()
                with col3:
                    if st.button("🔄 Reset", help="Clear all filters", use_container_width=True):
                        st.session_state['quick_filter_diff'] = 0.0
                        st.session_state['quick_filter_var'] = 0.0
                        st.rerun()

            clear = st.sidebar.button("🧹 Clear uploaded data", type="secondary", key="clear_data_btn")
            if clear:
                st.session_state.uploaded_file = None
                st.session_state.df = None
                st.session_state.variance_df = None
                st.session_state.df_clean = None
                st.session_state.analysis_mode = None
                st.session_state.auto_detected = None
                st.rerun()

            st.sidebar.markdown("---")
            
            analyze_button = st.sidebar.button("🔍 Analyze Data", type="primary", use_container_width=True, key="analyze_btn")
            
            # Main content area
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis Results", "📈 Visualizations", "📉 Trends", "📄 Raw Data"])
            
            with tab1:
                # Run analysis on button click
                if analyze_button:
                    # Progress feedback
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔄 Step 1/3: Preparing data...")
                    progress_bar.progress(33)
                    time.sleep(0.3)
                    
                    status_text.text("🔄 Step 2/3: Running analysis...")
                    progress_bar.progress(66)
                    
                    if analysis_mode.startswith("Within"):
                        variance_df, df_clean = audit_material_price_variance(
                            df,
                            column_mapping,
                            date_format=date_format.strip() or None,
                            dayfirst=dayfirst,
                        )
                        st.session_state.analysis_mode = 'within'
                    else:
                        variance_df, df_clean = audit_cross_customer_variance(
                            df,
                            column_mapping,
                            date_format=date_format.strip() or None,
                            dayfirst=dayfirst,
                        )
                        st.session_state.analysis_mode = 'across'
                    
                    status_text.text("🔄 Step 3/3: Finalizing results...")
                    progress_bar.progress(100)
                    time.sleep(0.2)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    if variance_df is not None and not variance_df.empty:
                        # Store ORIGINAL unfiltered results in session state
                        st.session_state.variance_df = variance_df
                        st.session_state.df_clean = df_clean
                        st.session_state.quality_issues = analyze_data_quality(df)
                        st.success("✅ Analysis complete!")
                    else:
                        st.session_state.variance_df = None
                        st.session_state.df_clean = df_clean
                        st.session_state.quality_issues = analyze_data_quality(df)
                
                # Display results (works on first run AND all subsequent reruns with filters)
                if 'variance_df' in st.session_state and st.session_state.variance_df is not None:
                    variance_df = st.session_state.variance_df
                    df_clean = st.session_state.df_clean
                    
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
                    
                    # Variance table with filters
                    st.subheader("🔍 Price Variance Details")
                    
                    # Apply optional filters
                    filtered_df = variance_df.copy()
                    # Parse Date to datetime for range filters
                    try:
                        filtered_df['__DateDT'] = pd.to_datetime(filtered_df['Date'], errors='coerce')
                    except Exception:
                        filtered_df['__DateDT'] = pd.NaT

                    # Filters in collapsible section for cleaner UI
                    with st.expander("🎚️ Advanced Filters", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Date range filter control
                            if filtered_df['__DateDT'].notna().any():
                                min_d = pd.to_datetime(filtered_df['__DateDT'].min()).date()
                                max_d = pd.to_datetime(filtered_df['__DateDT'].max()).date()
                                d1, d2 = st.date_input(
                                    "Filter by date range",
                                    value=(min_d, max_d),
                                    min_value=min_d,
                                    max_value=max_d,
                                )
                                if d1 and d2:
                                    mask = (filtered_df['__DateDT'] >= pd.to_datetime(d1)) & (filtered_df['__DateDT'] <= pd.to_datetime(d2))
                                    filtered_df = filtered_df[mask]
                        
                        with col2:
                            # Material filter
                            mats = sorted(variance_df['Material Code'].dropna().unique().tolist()) if 'Material Code' in variance_df.columns else []
                            if mats:
                                sel_mats = st.multiselect("Filter by material(s)", options=mats, default=[], key="material_filter")
                                if sel_mats:
                                    filtered_df = filtered_df[filtered_df['Material Code'].isin(sel_mats)]

                    # Threshold filters (from sidebar)
                    if min_diff > 0:
                        filtered_df = filtered_df[filtered_df['Difference'] >= float(min_diff)]
                    if min_var > 0:
                        filtered_df = filtered_df[filtered_df['Variance %'] >= float(min_var)]

                    # Clean helper column for display
                    if '__DateDT' in filtered_df.columns:
                        filtered_df = filtered_df.drop(columns=['__DateDT'])

                    # Show filtered results count
                    if len(filtered_df) < len(variance_df):
                        st.info(f"📊 Showing **{len(filtered_df)}** of **{len(variance_df)}** variance cases (filters applied)")
                    else:
                        st.info(f"📊 Showing all **{len(filtered_df)}** variance cases")
                    
                    st.dataframe(filtered_df, use_container_width=True, height=400)
                    
                    # Download section
                    st.markdown("---")
                    st.subheader("💾 Download Results")
                    
                    # Prepare metadata for download
                    metadata = {
                        'Analysis Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Analyzed By': st.session_state.get('current_user', 'Unknown'),
                        'Analysis Mode': st.session_state.get('analysis_mode', 'unknown'),
                        'Total Records': len(df),
                        'Valid Records': len(df_clean),
                        'Variance Cases Found': len(variance_df),
                        'Filtered Results': len(filtered_df),
                        'Min Difference Filter': f"₹{min_diff}" if min_diff > 0 else "None",
                        'Min Variance Filter': f"{min_var}%" if min_var > 0 else "None",
                    }
                    
                    quality_issues = st.session_state.get('quality_issues', {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Enhanced Excel download with metadata
                        excel_file = create_excel_download(filtered_df, metadata=metadata, quality_issues=quality_issues)
                        filter_suffix = f"_min{int(min_diff)}" if min_diff > 0 else ""
                        st.download_button(
                            label="📥 Download Excel Report (Multi-sheet)",
                            data=excel_file,
                            file_name=f"price_variance{filter_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            help="Includes: Variances + Metadata + Data Quality Report"
                        )
                    
                    with col2:
                        # CSV download
                        csv = filtered_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download CSV Report",
                            data=csv,
                            file_name=f"price_variance{filter_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                elif 'variance_df' in st.session_state and st.session_state.variance_df is None:
                    st.success("✅ No price variances detected!")
                    st.info("All materials have consistent basic rates for the same customer on the same date.")
                
                else:
                    st.info("👈 Configure column mappings in the sidebar and click 'Analyze Data' to start.")
            
            with tab2:
                if 'variance_df' in st.session_state and st.session_state.variance_df is not None:
                    variance_df = st.session_state.variance_df
                    mode = st.session_state.get('analysis_mode', 'within')
                    
                    st.subheader("📊 Visual Insights")
                    
                    # Top 10 variances chart (adapt by mode)
                    st.markdown("#### Top 10 Price Variances")
                    if mode == 'within' and 'Customer' in variance_df.columns:
                        fig1 = px.bar(
                            variance_df.head(10),
                            x='Customer',
                            y='Difference',
                            color='Variance %',
                            hover_data=['Material Code', 'Date', 'Max Rate', 'Min Rate'],
                            title="Top 10 Price Differences by Customer",
                            labels={'Difference': 'Price Difference (₹)', 'Variance %': 'Variance (%)'}
                        )
                    else:
                        # Across customers: rank by material/date
                        fig1 = px.bar(
                            variance_df.head(10),
                            x='Material Code',
                            y='Difference',
                            color='Variance %',
                            hover_data=['Date', 'Max Rate', 'Max Customer', 'Min Rate', 'Min Customer'] if set(['Max Customer','Min Customer']).issubset(variance_df.columns) else ['Date','Max Rate','Min Rate'],
                            title="Top 10 Material-Date Price Differences (Across Customers)",
                            labels={'Difference': 'Price Difference (₹)', 'Variance %': 'Variance (%)', 'Material Code': 'Material'}
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
                    
                    # Customer-wise or Material-wise variance count depending on mode
                    if mode == 'within' and 'Customer' in variance_df.columns:
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
                    else:
                        st.markdown("#### Top Materials by Variance Count (Across Customers)")
                        mat_counts = variance_df['Material Code'].value_counts().head(10)
                        fig4 = px.bar(
                            x=mat_counts.index,
                            y=mat_counts.values,
                            title="Top 10 Materials with Cross-Customer Price Variances",
                            labels={'x': 'Material Code', 'y': 'Number of Variances'}
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
                # Trend Analysis Tab
                if 'variance_df' in st.session_state and st.session_state.variance_df is not None:
                    variance_df = st.session_state.variance_df
                    
                    st.subheader("📉 Variance Trends Over Time")
                    
                    # Parse dates for trend analysis
                    try:
                        trend_df = variance_df.copy()
                        trend_df['DateParsed'] = pd.to_datetime(trend_df['Date'], errors='coerce')
                        trend_df = trend_df[trend_df['DateParsed'].notna()]
                        
                        if len(trend_df) > 0:
                            # Monthly aggregation
                            trend_df['YearMonth'] = trend_df['DateParsed'].dt.to_period('M').astype(str)
                            
                            monthly_stats = trend_df.groupby('YearMonth').agg({
                                'Difference': ['count', 'sum', 'mean', 'max'],
                                'Variance %': 'mean'
                            }).reset_index()
                            
                            monthly_stats.columns = ['Month', 'Variance_Count', 'Total_Difference', 'Avg_Difference', 'Max_Difference', 'Avg_Variance_Pct']
                            
                            # Trend line chart
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### Variance Count by Month")
                                fig1 = px.line(
                                    monthly_stats,
                                    x='Month',
                                    y='Variance_Count',
                                    markers=True,
                                    title="Number of Variance Cases Over Time"
                                )
                                fig1.update_traces(line_color='#1f77b4', line_width=3)
                                st.plotly_chart(fig1, use_container_width=True)
                            
                            with col2:
                                st.markdown("#### Average Difference by Month")
                                fig2 = px.line(
                                    monthly_stats,
                                    x='Month',
                                    y='Avg_Difference',
                                    markers=True,
                                    title="Average Price Difference (₹) Over Time"
                                )
                                fig2.update_traces(line_color='#ff7f0e', line_width=3)
                                st.plotly_chart(fig2, use_container_width=True)
                            
                            # Combined view
                            st.markdown("#### Comprehensive Monthly Trend")
                            fig3 = go.Figure()
                            
                            fig3.add_trace(go.Bar(
                                x=monthly_stats['Month'],
                                y=monthly_stats['Total_Difference'],
                                name='Total Difference (₹)',
                                yaxis='y',
                                marker_color='lightblue'
                            ))
                            
                            fig3.add_trace(go.Scatter(
                                x=monthly_stats['Month'],
                                y=monthly_stats['Variance_Count'],
                                name='Variance Count',
                                yaxis='y2',
                                mode='lines+markers',
                                line=dict(color='red', width=3)
                            ))
                            
                            fig3.update_layout(
                                title='Monthly Variance: Total Difference vs Count',
                                yaxis=dict(title='Total Difference (₹)'),
                                yaxis2=dict(title='Variance Count', overlaying='y', side='right'),
                                hovermode='x unified',
                                height=400
                            )
                            
                            st.plotly_chart(fig3, use_container_width=True)
                            
                            # Insights
                            st.markdown("#### 📊 Key Insights")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                trend_direction = "📈 Increasing" if monthly_stats['Variance_Count'].iloc[-1] > monthly_stats['Variance_Count'].iloc[0] else "📉 Decreasing"
                                st.metric("Trend Direction", trend_direction)
                            
                            with col2:
                                peak_month = monthly_stats.loc[monthly_stats['Variance_Count'].idxmax(), 'Month']
                                st.metric("Peak Month", peak_month)
                            
                            with col3:
                                avg_monthly = monthly_stats['Variance_Count'].mean()
                                st.metric("Avg Monthly Cases", f"{avg_monthly:.1f}")
                            
                            # Monthly data table
                            st.markdown("#### Monthly Summary Table")
                            st.dataframe(monthly_stats.style.format({
                                'Variance_Count': '{:.0f}',
                                'Total_Difference': '₹{:.2f}',
                                'Avg_Difference': '₹{:.2f}',
                                'Max_Difference': '₹{:.2f}',
                                'Avg_Variance_Pct': '{:.2f}%'
                            }), use_container_width=True)
                        
                        else:
                            st.warning("⚠️ No valid dates found for trend analysis")
                    
                    except Exception as e:
                        st.error(f"Error generating trends: {str(e)}")
                        st.info("💡 Ensure your date column contains valid dates")
                
                else:
                    st.info("👈 Run the analysis first to see trends.")
            
            with tab4:
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
