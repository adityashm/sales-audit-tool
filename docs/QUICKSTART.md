# Quick Start Guide 🚀

## Running Locally (Windows)

### Option 1: Using the Batch File (Easiest)
1. Double-click `run_app.bat`
2. Browser will open automatically at `http://localhost:8501`

### Option 2: Using Command Line
1. Open PowerShell or Command Prompt
2. Navigate to project folder:
   ```
   cd "c:\Users\aditya\Downloads\ayush  project\final"
   ```
3. Run:
   ```
   python -m streamlit run src/app.py
   ```

### Option 3: Using VS Code
1. Open terminal in VS Code (Ctrl + `)
2. Run:
   ```
   python -m streamlit run src/app.py
   ```

---

## First Time Use

### 1. Test with Sample Data
- Use the included `sample_data.csv` file
- This has pre-configured column names
- Upload it to see how the tool works

### 2. Upload Your Own Data
- Make sure your file has:
  - Customer names
  - Material codes
  - Dates
  - Prices
  - Material descriptions

### 3. Map Your Columns
- In the sidebar, select which column corresponds to each required field
- The tool is flexible - your column names don't need to match exactly

---

## How to Use the App

### Step 1: Upload File 📤
- Click "Browse files" in sidebar
- Select CSV or Excel file
- File info will appear

### Step 2: Configure Columns 🔧
- Map each dropdown to your data columns:
  - **Material Description** → Your product name column
  - **Date Column** → Your order/transaction date column
  - **Material Code** → Your product code/SKU column
  - **Customer Name** → Your customer name column
  - **Price/Rate Column** → Your price column

### Step 3: Analyze 🔍
- Click "🔍 Analyze Data" button
- Wait for processing (usually <5 seconds)
- Results appear in main area

### Step 4: Review Results 📊
- **Analysis Results Tab**: See variance table and statistics
- **Visualizations Tab**: View interactive charts
- **Raw Data Tab**: Check your uploaded data

### Step 5: Download Report 💾
- Choose Excel or CSV format
- Click download button
- Report saves to your Downloads folder

---

## Understanding the Results

### What Does "Price Variance" Mean?
The tool finds cases where:
- **Same customer** bought
- **Same material** on the
- **Same date** at
- **Different prices**

This helps identify:
- ✅ Pricing errors
- ✅ Unauthorized discounts  
- ✅ System glitches
- ✅ Fraud attempts
- ✅ Inconsistent pricing

### Key Metrics
- **Total Variance Cases**: Number of issues found
- **Avg Price Difference**: Average difference in prices
- **Max Price Difference**: Largest price gap found

### Variance Table Columns
- **Customer**: Who made the purchase
- **Material Code**: What was purchased
- **Date**: When it was purchased
- **Max Rate**: Highest price charged
- **Min Rate**: Lowest price charged
- **Difference**: Price gap (Max - Min)
- **Variance %**: Percentage difference

---

## Tips for Best Results 💡

### Data Quality
- ✅ Remove test data before uploading
- ✅ Ensure dates are in proper format (YYYY-MM-DD or DD/MM/YYYY)
- ✅ Check for missing values in key columns
- ✅ Use consistent customer names (avoid duplicates like "ABC Inc" and "ABC Inc.")

### Column Mapping
- ⚠️ Double-check each mapping before analyzing
- ⚠️ If wrong columns are selected, results will be incorrect
- ⚠️ You can change mappings and re-analyze anytime

### File Size
- ✅ Works best with files under 50MB
- ✅ For larger files, consider filtering data by date range first
- ✅ Excel files may load slower than CSV

---

## Common Issues & Solutions 🔧

### "Missing required columns"
**Problem**: Selected columns don't exist in your data
**Solution**: Re-check column mappings in sidebar

### "No variances detected"
**Problem**: No price differences found
**Solution**: This is actually good news! It means pricing is consistent

### "Error reading file"
**Problem**: File format not supported or corrupted
**Solution**: 
- Save Excel as .xlsx (not .xls)
- For CSV, use UTF-8 encoding
- Try opening file in Excel first to verify it's not corrupted

### App loads slowly
**Problem**: Large file or many records
**Solution**:
- Filter data to recent dates only
- Convert Excel to CSV for faster loading
- Remove unnecessary columns before upload

### Charts not showing
**Problem**: No variance data or browser issue
**Solution**:
- Make sure "Analyze Data" was clicked
- Try refreshing the page (F5)
- Check if any data was actually loaded

---

## Sample Use Cases 📋

### Use Case 1: Monthly Audit
1. Export sales data for the month
2. Upload to tool
3. Review variances
4. Send report to management
5. Investigate flagged transactions

### Use Case 2: Real-time Monitoring
1. Export today's sales
2. Run analysis before end of day
3. Fix any issues immediately
4. Repeat daily

### Use Case 3: Historical Analysis
1. Upload 6-12 months of data
2. Identify patterns
3. Find repeat offenders (customers or products)
4. Implement preventive measures

---

## Keyboard Shortcuts ⌨️

- `Ctrl + R` - Refresh the app
- `F11` - Full screen mode
- `Ctrl + F` - Search within page
- `Ctrl + Plus/Minus` - Zoom in/out

---

## Next Steps After Local Testing

Once you're comfortable with the tool locally:

1. **Deploy to Cloud** (see DEPLOYMENT_GUIDE.md)
   - Share with entire team
   - Access from anywhere
   - No installation needed for users

2. **Customize Further**
   - Add company logo
   - Change color scheme
   - Add more analysis types

3. **Automate**
   - Schedule daily uploads
   - Email reports automatically
   - Integrate with your ERP system

---

## Getting Help 🆘

### Check These First
1. README.md - General information
2. DEPLOYMENT_GUIDE.md - Hosting instructions
3. This file - Quick start guide

### Still Need Help?
- Check the example data structure
- Verify all dependencies are installed
- Try with sample_data.csv first

---

## System Requirements 💻

### Minimum
- Windows 10 or later / macOS / Linux
- Python 3.8+
- 2GB RAM
- Modern web browser (Chrome, Firefox, Edge)

### Recommended
- Python 3.11+
- 4GB+ RAM
- Good internet connection (for deployment)
- Large monitor (better for viewing charts)

---

## File Structure 📁

```
project/
├── src/
│   ├── app.py              # Main Streamlit application
│   └── sales.py            # Original analysis script
├── data/
│   └── sample_data.csv     # Example data for testing
├── requirements.txt        # Python dependencies
├── run_app.bat             # Windows launcher
├── docs/
│   ├── README.md           # Project overview
│   └── DEPLOYMENT_GUIDE.md # Hosting instructions
├── QUICKSTART.md          # This file
├── .gitignore             # Git ignore rules
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

---

**Ready to start? Double-click `run_app.bat` or run `python -m streamlit run app.py`!** 🎉
