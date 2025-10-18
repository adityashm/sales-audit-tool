# Troubleshooting Guide 🔧

## Common Errors and Solutions

### ❌ Error: AxiosError - Request failed with status code 403

**Symptoms:**
- Cannot upload files
- Error message: `'_xsrf' argument missing from POST`
- 403 errors in browser console

**Cause:**
This is a CSRF (Cross-Site Request Forgery) protection issue in Streamlit. When `enableXsrfProtection=true` and `enableCORS=false` are set together, it creates a conflict.

**Solution:**
1. Remove or comment out both `enableXsrfProtection` and `enableCORS` from `.streamlit/config.toml`
2. Let Streamlit use default security settings
3. Restart the app

**Fixed Config File (`.streamlit/config.toml`):**
```toml
[theme]
primaryColor="#1f77b4"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"

[server]
headless = true
port = 8501
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

**To Restart:**
```bash
# Stop the running app (Ctrl+C in terminal)
# Then run:
python -m streamlit run app.py
```

---

### ❌ Error: Command 'streamlit' is not recognized

**Symptoms:**
```
streamlit : The term 'streamlit' is not recognized
```

**Solution:**
Use Python module syntax instead:
```bash
python -m streamlit run app.py
```

---

### ❌ Error: Module not found (pandas, streamlit, etc.)

**Symptoms:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
Install required packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas openpyxl plotly
```

---

### ❌ Error: Cannot build pandas (compilation error)

**Symptoms:**
- Long error about C++ compiler
- "Could not find Visual Studio"
- Build dependencies failed

**Solution:**
Use pre-built wheels (don't specify exact versions):
```bash
pip install streamlit pandas openpyxl plotly
```

Instead of:
```bash
pip install pandas==2.1.4  # ❌ This may require compilation
```

---

### ❌ Error: Port 8501 already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solution 1 - Kill existing process:**
```bash
# Windows PowerShell:
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *streamlit*"

# Or find and kill the process:
netstat -ano | findstr :8501
taskkill /PID <process_id> /F
```

**Solution 2 - Use different port:**
```bash
python -m streamlit run app.py --server.port=8502
```

---

### ❌ Error: File upload not working

**Symptoms:**
- Upload button doesn't respond
- File doesn't appear after selection
- 403 or 500 errors

**Solutions:**

1. **Check file size:**
   - Default max: 200MB
   - Increase in config.toml: `maxUploadSize = 500`

2. **Check file format:**
   - Supported: `.csv`, `.xlsx`, `.xls`
   - Not supported: `.xlsb`, `.ods`, other formats

3. **Check browser:**
   - Clear browser cache
   - Try incognito/private mode
   - Try different browser

4. **Check XSRF protection:**
   - See 403 error solution above

---

### ❌ Error: Charts not displaying

**Symptoms:**
- Blank spaces where charts should be
- "Plotly is not defined" error

**Solutions:**

1. **Install Plotly:**
```bash
pip install plotly
```

2. **Clear cache and restart:**
```bash
python -m streamlit run app.py --server.runOnSave=true
```

3. **Check browser console:**
   - Press F12 in browser
   - Look for JavaScript errors
   - Try disabling browser extensions

---

### ❌ Error: Data not loading from Excel

**Symptoms:**
- "Error reading file"
- Excel files don't upload
- openpyxl errors

**Solutions:**

1. **Install openpyxl:**
```bash
pip install openpyxl
```

2. **Convert to CSV:**
   - Open Excel file
   - Save As → CSV (UTF-8)
   - Upload CSV instead

3. **Check Excel format:**
   - Use `.xlsx` not `.xls`
   - Avoid macros (.xlsm)
   - Remove password protection

---

### ❌ Warning: use_container_width deprecated

**Symptoms:**
```
Please replace `use_container_width` with `width`
```

**Solution:**
This is just a deprecation warning. The app still works. To fix:

Find in `app.py`:
```python
st.dataframe(df, use_container_width=True)
```

Replace with:
```python
st.dataframe(df, width='stretch')
```

---

### ❌ Error: Column mapping incorrect

**Symptoms:**
- "Missing required columns" error
- Analysis shows wrong results
- No variances found when there should be

**Solutions:**

1. **Verify column names:**
   - Check "Raw Data Preview" tab
   - Ensure exact spelling matches
   - Check for spaces/special characters

2. **Re-map columns:**
   - Double-check each dropdown
   - Ensure correct column selected
   - Click "Analyze Data" again

3. **Check data quality:**
   - Ensure no empty columns
   - Check date format (YYYY-MM-DD recommended)
   - Verify numeric prices (no currency symbols)

---

### ❌ Error: No variances detected (but should be some)

**Symptoms:**
- Message: "No price variances detected"
- But you know there are differences

**Possible Causes & Solutions:**

1. **Column mapping wrong:**
   - Verify material code, customer, date columns
   - Check "Raw Data Preview" tab

2. **Date format issues:**
   - Dates might not be parsing correctly
   - Try converting dates to YYYY-MM-DD format in Excel

3. **Customer name variations:**
   - "ABC Inc" vs "ABC Inc." vs "ABC INC"
   - Clean data first to standardize names

4. **Material code variations:**
   - "MAT001" vs "mat001" vs "MAT-001"
   - Standardize codes before upload

---

### ❌ Error: App is slow or freezing

**Symptoms:**
- Long loading times
- Browser becomes unresponsive
- "Script is taking too long" warning

**Solutions:**

1. **Reduce file size:**
   - Filter data by date range
   - Remove unnecessary columns
   - Split large files into smaller ones

2. **Use CSV instead of Excel:**
   - CSV loads much faster
   - Convert in Excel: Save As → CSV

3. **Increase timeout:**
   - Click "Continue running" when warned
   - Or add to config.toml:
   ```toml
   [server]
   maxMessageSize = 500
   ```

4. **Clear browser cache:**
   - Full restart recommended
   - Close other browser tabs

---

### ❌ Error: Download not working

**Symptoms:**
- Download button doesn't respond
- Downloaded file is empty or corrupted
- Browser blocks download

**Solutions:**

1. **Check browser settings:**
   - Allow downloads from localhost
   - Check blocked downloads in browser

2. **Try different format:**
   - If Excel fails, try CSV
   - If CSV fails, try Excel

3. **Check data exists:**
   - Ensure analysis ran successfully
   - Check if variance table has data

4. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R
   - Try incognito mode

---

### ❌ Error: localhost:8501 not loading

**Symptoms:**
- "This site can't be reached"
- Connection refused
- Page timeout

**Solutions:**

1. **Check if app is running:**
   - Look at terminal/command prompt
   - Should see "You can now view your Streamlit app"

2. **Try network URL instead:**
   - Use the "Network URL" shown in terminal
   - Example: http://192.168.1.20:8501

3. **Check firewall:**
   - Windows Firewall might block
   - Allow Python through firewall

4. **Restart app:**
   - Press Ctrl+C in terminal
   - Run command again

---

## Quick Fixes Checklist ✅

Before asking for help, try these:

- [ ] Restart the Streamlit app
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Try incognito/private browsing mode
- [ ] Check terminal for error messages
- [ ] Verify all packages are installed: `pip list | grep -E "streamlit|pandas|plotly|openpyxl"`
- [ ] Try with sample_data.csv first
- [ ] Update packages: `pip install --upgrade streamlit pandas plotly openpyxl`
- [ ] Check Python version: `python --version` (should be 3.8+)
- [ ] Restart computer (sometimes helps with ports)

---

## Getting Detailed Error Information

### View Terminal Logs
```bash
python -m streamlit run app.py --logger.level=debug
```

### View Browser Console
1. Press `F12` in browser
2. Click "Console" tab
3. Look for red error messages
4. Screenshot and share if asking for help

### Check Streamlit Logs
```bash
# Windows:
%USERPROFILE%\.streamlit\logs\

# View latest log:
type %USERPROFILE%\.streamlit\logs\latest.log
```

---

## Still Having Issues?

### Collect This Information:

1. **Python Version:**
   ```bash
   python --version
   ```

2. **Installed Packages:**
   ```bash
   pip list
   ```

3. **Full Error Message:**
   - Copy entire error from terminal
   - Include stack trace

4. **Browser Console:**
   - Take screenshot of F12 console

5. **Steps to Reproduce:**
   - What you did
   - What happened
   - What you expected

---

## Performance Tips 🚀

### For Faster Loading:
1. Use CSV instead of Excel
2. Remove unnecessary columns before upload
3. Filter data by date range
4. Use `@st.cache_data` decorator (for developers)

### For Better User Experience:
1. Close other applications
2. Use modern browser (Chrome, Firefox, Edge)
3. Ensure stable internet (for cloud deployment)
4. Use local deployment for large files

---

## Prevention Tips 💡

### Before Uploading:
- Clean your data in Excel first
- Standardize customer names
- Ensure dates are formatted consistently
- Remove duplicate rows
- Check for missing values

### Regular Maintenance:
- Update packages monthly
- Clear browser cache weekly
- Keep Python updated
- Backup important reports

---

## Contact & Support 📧

If none of these solutions work:

1. Check the GitHub Issues (if using GitHub)
2. Review Streamlit documentation: https://docs.streamlit.io
3. Check Pandas documentation for data issues
4. Review project README.md and QUICKSTART.md

**Remember:** Most issues are related to configuration, file format, or browser cache! 🎯
