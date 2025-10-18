# Sales Price Variance Audit Tool 📊

A powerful, secure Streamlit web application for auditing sales data to identify price inconsistencies when the same customer purchases the same material on the same date at different rates.

## Features ✨

- 🔐 **Secure Authentication**: Password-protected access with multiple user support
- 🔄 **Flexible Column Mapping**: Map your data columns to required fields
- 📤 **File Upload**: Support for CSV and Excel files
- 📊 **Interactive Visualizations**: Multiple charts and graphs for data insights
- 💾 **Export Results**: Download reports in Excel or CSV format
- 🎨 **User-Friendly Interface**: Clean and intuitive design
- 📈 **Real-time Analysis**: Instant variance detection and reporting
- ☁️ **Cloud-Ready**: Deploy to Streamlit Cloud in minutes

## Installation 🛠️

### Local Setup

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m streamlit run app.py
```

4. Open your browser and navigate to:
```
http://localhost:8501
```

### Quick Start (Windows)
Double-click `run_app.bat` to start the application automatically!

## Authentication 🔐

The app includes secure password-based authentication.

**Default Credentials (Development Only):**
- Username: `admin` | Password: `admin123`
- Username: `auditor` | Password: `audit@2025`
- Username: `manager` | Password: `manager123`

⚠️ **IMPORTANT:** Change these passwords before deploying to production!

See **[AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md)** for:
- How to configure users
- Password best practices
- Security guidelines
- Role-based access (coming soon)

## Usage 📝

### Step 1: Login
- Enter your username and password
- Click "Login" button

### Step 2: Upload Your Data
- Click on the file uploader in the sidebar
- Upload a CSV or Excel file containing your sales data

### Step 3: Map Your Columns
The tool requires the following columns (map them to your actual column names):
- **Material Description**: Product/material name or description
- **Date Column**: Order or transaction date
- **Material Code**: Product code/SKU
- **Customer Name**: Customer or party name
- **Price/Rate Column**: Basic rate or selling price

### Step 4: Analyze
- Click the "🔍 Analyze Data" button
- View summary statistics and variance details
- Explore interactive visualizations

### Step 5: Download Results
- Download the variance report in Excel or CSV format
- Share insights with your team

## Data Requirements 📋

Your data file should contain:
- Customer/Party information
- Material codes and descriptions
- Transaction dates
- Pricing information

Example structure:
```
| MATERIAL DESCRIPTION | SO CREATED ON | MATERIAL CODE | SOLD TO PARTY NAME | BASIC RATE |
|---------------------|---------------|---------------|-------------------|------------|
| Product A           | 2025-01-15    | MAT001        | Customer X        | 100.00     |
| Product A           | 2025-01-15    | MAT001        | Customer X        | 105.00     |
```

## Deployment 🚀

**Complete deployment guides available:**

### 📘 [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)
Step-by-step guide to deploy on Streamlit Cloud (FREE)
- Authentication setup
- Secrets configuration
- Custom domains
- Monitoring

### 🐙 [GITHUB_SETUP.md](GITHUB_SETUP.md)
Complete guide to push your code to GitHub
- Git installation
- Repository creation
- Push commands
- Best practices

### 📚 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
Multiple deployment options:
- Streamlit Cloud (Recommended)
- Heroku
- Railway
- Google Cloud Run
- Azure
- DigitalOcean
- Self-hosting

**Quick Deploy to Streamlit Cloud:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Configure secrets (passwords)
5. Deploy! (2 minutes)

Your app will be at: `https://your-app-name.streamlit.app`

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/Azure/GCP

Use Docker for containerized deployment:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build and deploy:
```bash
docker build -t sales-audit-app .
docker run -p 8501:8501 sales-audit-app
```

## Documentation 📚

Complete guides available in this repository:

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Quick start guide for first-time users |
| **[AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md)** | Security and user management |
| **[GITHUB_SETUP.md](GITHUB_SETUP.md)** | Push your code to GitHub |
| **[STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)** | Deploy to Streamlit Cloud |
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | All deployment options |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and solutions |

## Features Breakdown 🎯

### Analysis Tab
- Summary statistics (total cases, average difference, max difference)
- Detailed variance table with sorting and filtering
- Download options for Excel and CSV

### Visualizations Tab
- Top 10 price variances bar chart
- Price difference distribution histogram
- Variance percentage box plot
- Customer-wise variance count
- Material-wise variance pie chart

### Raw Data Tab
- Preview of uploaded data
- First 100 rows display

## Technical Details 🔧

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **OpenPyXL**: Excel file handling

### Logic
The tool identifies variance cases where:
```
Same Customer + Same Material Code + Same Date = Different Prices
```

## Troubleshooting 🔍

For detailed troubleshooting, see **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### Quick Fixes

1. **403 Error on File Upload**:
   - Clear browser cache (Ctrl+Shift+R)
   - Try incognito mode
   - Check TROUBLESHOOTING.md

2. **Can't Login**:
   - Verify credentials in secrets.toml
   - Check AUTHENTICATION_GUIDE.md

3. **Column Mapping Issues**:
   - Verify column names match
   - Check Raw Data Preview tab

4. **App Won't Start**:
   - Install all dependencies: `pip install -r requirements.txt`
   - Try: `python -m streamlit run app.py`

## Project Structure 📁

```
sales-audit-tool/
├── app.py                          # Main application (with authentication)
├── sales.py                        # Original script
├── requirements.txt                # Python dependencies
├── sample_data.csv                 # Example data
├── run_app.bat                     # Windows launcher
├── README.md                       # This file
├── QUICKSTART.md                   # Quick start guide
├── AUTHENTICATION_GUIDE.md         # Security guide
├── GITHUB_SETUP.md                 # GitHub setup
├── STREAMLIT_DEPLOYMENT.md         # Streamlit Cloud deployment
├── DEPLOYMENT_GUIDE.md             # All deployment options
├── TROUBLESHOOTING.md              # Problem solving
├── .gitignore                      # Git ignore rules
└── .streamlit/
    ├── config.toml                 # Streamlit configuration
    └── secrets.toml                # Passwords (NOT in Git)
```

## Security �️

- ✅ Password-protected access
- ✅ Secrets management via Streamlit
- ✅ No credentials in code
- ✅ Session-based authentication
- ✅ HTTPS on deployment

**See [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) for security best practices.**

## License 📄

This project is open source and available for educational and commercial use.

## Version History 📌

- **v2.0.0** (2025-10-18): Authentication Release
  - Added password-based authentication
  - Multi-user support
  - Secrets management
  - Enhanced security
  - Comprehensive documentation

- **v1.0.0** (2025-10-18): Initial release
  - File upload and column mapping
  - Price variance analysis
  - Interactive visualizations
  - Excel/CSV export
  - Streamlit Cloud ready

---

**Made with ❤️ using Streamlit**
