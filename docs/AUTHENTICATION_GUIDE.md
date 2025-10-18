# Authentication & Security Guide 🔐

## Overview

Your Sales Price Variance Audit Tool now includes secure password-based authentication to protect sensitive financial data.

---

## Features

✅ **Secure Login System**
- Username and password authentication
- Password masking
- Session management
- Automatic logout option

✅ **Multiple User Support**
- Admin accounts
- Auditor accounts
- Manager accounts
- Easy to add more users

✅ **Production-Ready**
- Secrets management via Streamlit
- Passwords not stored in code
- Secure credential handling

---

## Default Credentials (Local Development)

**⚠️ CHANGE THESE BEFORE DEPLOYMENT!**

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |
| `auditor` | `audit@2025` | Auditor |
| `manager` | `manager123` | Manager |

---

## How Authentication Works

### 1. Login Screen
- Users see login form on first access
- Enter username and password
- Click "Login" button

### 2. Session Management
- Credentials verified against user database
- Session created on successful login
- Session persists during browser session

### 3. Logout
- "Logout" button in sidebar
- Clears session
- Returns to login screen

### 4. Security Features
- Passwords never displayed
- No password storage in browser
- Session expires on browser close

---

## Configuring Users

### Method 1: Local Development (app.py)

For testing locally, users are defined in `app.py`:

```python
USERS = {
    "admin": "admin123",
    "auditor": "audit@2025",
    "manager": "manager123"
}
```

**To add more users:**
```python
USERS = {
    "admin": "admin123",
    "john_doe": "JohnSecure@2025",
    "jane_smith": "Jane#Strong123",
    "auditor1": "Audit$Pass456"
}
```

### Method 2: Production (Streamlit Secrets)

For deployed apps, use `.streamlit/secrets.toml`:

**Local file (`.streamlit/secrets.toml`):**
```toml
[passwords]
admin = "SuperSecure@Admin123!"
auditor = "Audit#Strong456$"
manager = "Manager&Pass789^"
john_doe = "JohnDoe#2025!"
jane_smith = "Jane$Secure789"
```

**Streamlit Cloud:**
1. Go to app settings
2. Click "Secrets"
3. Add:
```toml
[passwords]
admin = "YourStrongPassword123!"
auditor = "AnotherSecurePass456!"
manager = "Manager@Secure789"
```

---

## Password Requirements

### For Production, Use Strong Passwords:

**✅ Good Password:**
- At least 12 characters
- Mix of uppercase and lowercase
- Include numbers
- Include special characters
- Example: `aD#9mK$2pL@8nQ!5`

**❌ Bad Password:**
- Short (< 8 characters)
- Common words (password, admin, 12345)
- No special characters
- Example: `admin123`

### Password Generators:
- Use built-in browser password generator
- Or online: https://passwordsgenerator.net
- Generate 16+ character passwords

---

## Managing Users

### Adding New Users

**Step 1: Update Secrets**

For Streamlit Cloud:
1. Go to app settings → Secrets
2. Add new user:
```toml
[passwords]
existing_user = "existing_pass"
new_user = "NewUserPassword123!"
```

For Local:
Update `.streamlit/secrets.toml`:
```toml
[passwords]
new_user = "NewUserPassword123!"
```

**Step 2: Share Credentials Securely**
- Send username and password separately
- Use encrypted email or password manager
- Never share in plain text
- Change password after first login (future feature)

### Removing Users

**Simply delete from secrets:**
```toml
[passwords]
# user_to_remove = "password"  # Commented out or deleted
active_user = "password"
```

### Changing Passwords

**Update the password in secrets:**
```toml
[passwords]
username = "NewPassword123!"  # Updated
```

**Notify user:**
- Email new password securely
- Ask them to change it (future feature)

---

## User Roles & Permissions

### Current Implementation
All authenticated users have full access to:
- Upload files
- Analyze data
- View results
- Download reports

### Future Enhancements (To Implement)

**Admin Role:**
```python
ADMINS = ["admin", "john_doe"]

if st.session_state['current_user'] in ADMINS:
    # Show admin features
    st.sidebar.button("Manage Users")
    st.sidebar.button("View All Reports")
```

**Read-Only Role:**
```python
READ_ONLY_USERS = ["viewer1", "viewer2"]

if st.session_state['current_user'] not in READ_ONLY_USERS:
    # Show upload functionality
    uploaded_file = st.file_uploader(...)
else:
    st.info("You have read-only access")
```

**Auditor Role:**
```python
AUDITORS = ["auditor", "auditor1"]

if st.session_state['current_user'] in AUDITORS:
    # Show audit-specific features
    st.sidebar.button("Generate Audit Report")
    st.sidebar.button("Export Audit Trail")
```

---

## Security Best Practices

### 1. Password Management

**DO:**
- ✅ Use unique passwords for each user
- ✅ Use password manager (1Password, LastPass, Bitwarden)
- ✅ Rotate passwords every 90 days
- ✅ Use 16+ character passwords
- ✅ Mix uppercase, lowercase, numbers, symbols

**DON'T:**
- ❌ Reuse passwords across systems
- ❌ Share passwords in plain text
- ❌ Store passwords in Excel/Word
- ❌ Use dictionary words
- ❌ Use personal information (birthdays, names)

### 2. Access Control

**DO:**
- ✅ Remove access when users leave
- ✅ Review user list monthly
- ✅ Use least privilege principle
- ✅ Log access (future feature)
- ✅ Monitor suspicious activity

**DON'T:**
- ❌ Share admin credentials
- ❌ Use generic accounts
- ❌ Leave inactive accounts active
- ❌ Give everyone admin access

### 3. Deployment Security

**DO:**
- ✅ Use Streamlit Cloud secrets
- ✅ Enable GitHub 2FA
- ✅ Use private GitHub repository
- ✅ Keep dependencies updated
- ✅ Monitor logs regularly

**DON'T:**
- ❌ Commit secrets to GitHub
- ❌ Use default passwords in production
- ❌ Share deployment credentials
- ❌ Ignore security warnings

---

## Testing Authentication

### Local Testing

1. **Start app:**
```powershell
python -m streamlit run app.py
```

2. **Test each user:**
- Try logging in with each username
- Verify login works
- Check logout functionality

3. **Test wrong credentials:**
- Try invalid username
- Try wrong password
- Verify error message appears

### Production Testing

After deployment:

1. **Test from different devices:**
   - Desktop browser
   - Mobile browser
   - Different networks

2. **Test session persistence:**
   - Login
   - Refresh page
   - Verify still logged in

3. **Test logout:**
   - Click logout
   - Verify redirected to login
   - Try accessing without login

---

## Troubleshooting Authentication

### ❌ Can't Login (Correct Credentials)

**Check:**
1. Secrets configured in Streamlit Cloud?
2. Format correct (TOML)?
3. No extra spaces in username/password?
4. Quotes around passwords?

**Solution:**
```toml
# ❌ Wrong
[passwords]
admin = admin123

# ✅ Correct
[passwords]
admin = "admin123"
```

### ❌ Login Screen Not Showing

**Check:**
1. Is `check_password()` called in `main()`?
2. Any errors in console (F12)?
3. App running without errors?

**Verify in app.py:**
```python
def main():
    if not check_password():
        return  # This is important!
    # Rest of app...
```

### ❌ Logged Out After Each Action

**Check:**
1. Session state initialized?
2. Using `st.rerun()` instead of `st.experimental_rerun()`?

**Solution:**
Update Streamlit to latest version:
```powershell
pip install --upgrade streamlit
```

### ❌ Secrets Not Loading

**Local:**
1. Check file path: `.streamlit/secrets.toml`
2. Check TOML syntax
3. Restart Streamlit

**Cloud:**
1. Go to Settings → Secrets
2. Verify secrets saved
3. Reboot app

---

## Advanced Features (Future Implementation)

### 1. Password Hashing

Instead of storing plain passwords:

```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Store hashed passwords
USERS = {
    "admin": "hashed_password_here"
}

# Verify login
if hash_password(entered_password) == USERS[username]:
    # Login successful
```

### 2. Session Timeout

Auto-logout after inactivity:

```python
import time

# Store last activity time
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()

# Check timeout (30 minutes)
if time.time() - st.session_state.last_activity > 1800:
    st.session_state.authenticated = False
    st.rerun()

# Update activity time
st.session_state.last_activity = time.time()
```

### 3. Login Attempts Limit

Prevent brute force:

```python
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0

if st.session_state.login_attempts >= 3:
    st.error("Too many failed attempts. Please wait 5 minutes.")
    return

# On failed login
st.session_state.login_attempts += 1

# On successful login
st.session_state.login_attempts = 0
```

### 4. Audit Logging

Track who did what:

```python
import datetime

def log_action(user, action):
    with open('audit.log', 'a') as f:
        timestamp = datetime.datetime.now()
        f.write(f"{timestamp} | {user} | {action}\n")

# Log activities
log_action(st.session_state.current_user, "Uploaded file")
log_action(st.session_state.current_user, "Downloaded report")
```

### 5. Multi-Factor Authentication (MFA)

Email verification code:

```python
import random
import smtplib

def send_verification_code(email):
    code = random.randint(100000, 999999)
    # Send email with code
    return code

# After password verification
if password_correct:
    code = send_verification_code(user_email)
    entered_code = st.text_input("Enter verification code")
    if entered_code == str(code):
        st.session_state.authenticated = True
```

---

## Compliance & Regulations

### GDPR Considerations

If handling EU data:
- ✅ Inform users about data collection
- ✅ Allow users to request data deletion
- ✅ Use encrypted connections (HTTPS)
- ✅ Keep access logs

### HIPAA Considerations

If handling healthcare data:
- ✅ Use encrypted storage
- ✅ Implement audit trails
- ✅ Regular security reviews
- ✅ Access control policies

### SOC 2 Considerations

For enterprise clients:
- ✅ Document security procedures
- ✅ Regular password rotations
- ✅ Access reviews
- ✅ Incident response plan

---

## User Guide for End Users

### How to Login

1. **Open the app URL**
2. **Enter your username** (provided by admin)
3. **Enter your password** (provided by admin)
4. **Click "Login"**
5. **Start using the app!**

### If You Forget Password

1. **Contact administrator**
2. **Verify your identity**
3. **Receive new temporary password**
4. **Login with new password**
5. **(Future) Change password immediately**

### Security Tips for Users

- ✅ Keep password confidential
- ✅ Don't share credentials
- ✅ Logout when done
- ✅ Report suspicious activity
- ✅ Use secure network (avoid public WiFi)
- ❌ Don't write password down
- ❌ Don't save password in browser (for sensitive apps)
- ❌ Don't login on public computers

---

## Checklist for Production

Before going live with authentication:

- [ ] Changed default passwords
- [ ] Used strong passwords (16+ chars)
- [ ] Configured secrets in Streamlit Cloud
- [ ] Tested all user logins
- [ ] Tested logout functionality
- [ ] Verified wrong credentials are rejected
- [ ] Documented user credentials (securely)
- [ ] Shared credentials with users (securely)
- [ ] Set up password rotation schedule
- [ ] Enabled GitHub 2FA
- [ ] Made repository private (if needed)
- [ ] Reviewed access list
- [ ] Set up monitoring
- [ ] Created user guide
- [ ] Tested on multiple devices

---

## Summary

Your app now has:
- ✅ Secure password authentication
- ✅ Multiple user support
- ✅ Production-ready secrets management
- ✅ Session management
- ✅ Logout functionality

**Remember:**
1. Change default passwords
2. Use strong passwords
3. Rotate regularly
4. Monitor access
5. Keep documentation updated

**Your data is now protected! 🛡️**
