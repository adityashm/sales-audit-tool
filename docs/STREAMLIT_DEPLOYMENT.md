# Complete Deployment Guide 🚀

## Deploy to Streamlit Cloud (FREE & EASIEST)

Follow this step-by-step guide to deploy your authenticated app to the cloud.

---

## Prerequisites ✅

Before deploying, make sure you have:
- [x] GitHub account
- [x] Code pushed to GitHub (see GITHUB_SETUP.md)
- [x] Working app locally
- [x] All dependencies in requirements.txt

---

## Step 1: Push to GitHub

If you haven't already, follow **GITHUB_SETUP.md** first!

**Quick check:**
```powershell
# Verify your code is on GitHub
git remote -v
git status
```

Your repository should be at: `https://github.com/YOUR_USERNAME/sales-audit-tool`

---

## Step 2: Create Streamlit Cloud Account

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io

2. **Sign up with GitHub:**
   - Click "Sign up"
   - Choose "Continue with GitHub"
   - Authorize Streamlit Cloud

3. **Grant repository access:**
   - Allow Streamlit to access your repositories
   - You can choose specific repos or all repos

---

## Step 3: Deploy Your App

1. **Click "New app"**
   - From your dashboard, click the "New app" button

2. **Configure deployment:**
   
   | Field | Value | Example |
   |-------|-------|---------|
   | **Repository** | Your GitHub repo | `YOUR_USERNAME/sales-audit-tool` |
   | **Branch** | `main` | `main` |
   | **Main file path** | `src/app.py` | `src/app.py` |
   | **App URL** (optional) | Custom subdomain | `my-sales-audit` |

3. **Advanced settings (optional):**
   - Python version: `3.11` (recommended)
   - Click "Advanced settings" if you need to customize

4. **Click "Deploy!"**
   - Deployment will start automatically
   - Takes 2-5 minutes first time

---

## Step 4: Configure Secrets (Authentication)

**IMPORTANT:** Set up authentication passwords securely.

1. **Go to App Settings:**
   - Click the menu (⋮) in your app dashboard
   - Select "Settings"

2. **Add Secrets:**
   - Click "Secrets" in left sidebar
   - Add your credentials in TOML format:

   ```toml
   [passwords]
   admin = "YourStrongPassword123!"
   auditor = "AnotherSecurePass456!"
   manager = "Manager@Secure789"
   ```

3. **Save Secrets:**
   - Click "Save"
   - App will automatically reboot with new secrets

**⚠️ Security Tips:**
- Use strong passwords (12+ characters)
- Mix uppercase, lowercase, numbers, symbols
- Don't use the demo passwords in production!
- Change passwords regularly

---

## Step 5: Verify Deployment

1. **Wait for deployment:**
   - Green checkmark appears when ready
   - Status shows "Running"

2. **Test your app:**
   - Click "Open app" or visit your app URL
   - Example: `https://your-username-sales-audit-tool.streamlit.app`

3. **Test login:**
   - Try logging in with your configured credentials
   - Verify file upload works
   - Test analysis and download features

---

## Step 6: Share Your App

Your app is now live! Share it with:

**Direct Link:**
```
https://your-app-name.streamlit.app
```

**QR Code:**
- Use any QR generator with your app URL
- Print for easy mobile access

**Email:**
```
Hi Team,

Our Sales Price Variance Audit Tool is now live!

🔗 URL: https://your-app-name.streamlit.app

📋 Login Credentials:
- Username: [provided separately]
- Password: [provided separately]

Please keep credentials secure and don't share outside the team.

Best regards
```

---

## Managing Your Deployed App

### View Logs
1. Go to app dashboard
2. Click "Manage app"
3. View logs at bottom of page
4. Check for errors or usage patterns

### Update Your App
```powershell
# Make changes locally
# Test changes

# Commit and push to GitHub
git add .
git commit -m "Update: description"
git push

# Streamlit Cloud auto-deploys in ~1 minute!
```

### Reboot App
1. Go to app settings
2. Click "Reboot app"
3. Wait for restart (~30 seconds)

### Delete App
1. Go to app dashboard
2. Click menu (⋮)
3. Select "Delete app"
4. Confirm deletion

---

## Custom Domain (Optional - Paid Feature)

### Using Your Own Domain

1. **Upgrade to paid plan:**
   - Go to Streamlit Cloud settings
   - Choose a paid plan

2. **Add custom domain:**
   - Settings → Custom domain
   - Enter: `audit.yourcompany.com`

3. **Configure DNS:**
   - Add CNAME record in your domain provider
   - Point to: `your-app.streamlit.app`
   - Wait for DNS propagation (up to 48 hours)

4. **Enable HTTPS:**
   - Automatic with Streamlit Cloud
   - SSL certificate provided free

---

## Advanced Features

### Environment Variables

If you need additional configuration:

1. Go to Settings → Secrets
2. Add environment variables:

```toml
[passwords]
admin = "password123"

[settings]
max_upload_size = 200
debug_mode = false
company_name = "Your Company"

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
```

3. Access in code:
```python
company_name = st.secrets["settings"]["company_name"]
```

### Multiple Users/Roles

Update `src/app.py` to add more users:

```python
# In Streamlit Cloud Secrets:
[passwords]
admin = "admin_pass"
manager1 = "manager1_pass"
manager2 = "manager2_pass"
auditor1 = "auditor1_pass"
auditor2 = "auditor2_pass"
analyst1 = "analyst1_pass"
```

### Database Connection (Future)

For connecting to databases:

```toml
[database]
host = "your-db-host.com"
port = 5432
database = "sales_db"
user = "db_user"
password = "db_password"
```

---

## Monitoring & Analytics

### View Usage Statistics

1. **Streamlit Cloud Dashboard:**
   - Shows active users
   - Resource usage
   - Request counts

2. **Add Google Analytics (Optional):**

In `src/app.py`, add to the `<head>`:
```python
st.markdown("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
""", unsafe_allow_html=True)
```

---

## Troubleshooting Deployment

### ❌ Build Failed

**Check build logs for errors:**
- Missing dependencies in requirements.txt
- Syntax errors in src/app.py
- Incompatible package versions

**Solution:**
```powershell
# Test locally first
pip install -r requirements.txt
streamlit run src/app.py

# If works locally, push to GitHub
git push
```

### ❌ App Crashes on Startup

**Common causes:**
- Import errors
- Missing secrets
- Configuration issues

**Solution:**
1. Check logs in Streamlit Cloud
2. Verify secrets are configured
3. Test locally with same secrets

### ❌ Authentication Not Working

**Check:**
- Secrets configured correctly in Streamlit Cloud
- Format is correct TOML
- No extra spaces or quotes

**Correct format:**
```toml
[passwords]
admin = "password123"
```

**Incorrect:**
```toml
[passwords]
admin = password123        # Missing quotes
admin = "password123"      # Extra quotes around value
```

### ❌ File Upload 403 Error

**Solution:**
- Remove `enableCORS` and `enableXsrfProtection` from config.toml
- Let Streamlit Cloud use defaults
- See TROUBLESHOOTING.md for details

### ❌ App is Slow

**Reasons:**
- Large file uploads
- Complex calculations
- Free tier limitations

**Solutions:**
1. Optimize code (use caching)
2. Reduce file sizes
3. Upgrade to paid plan for more resources

---

## Streamlit Cloud Plans

### Free Tier
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ Basic resources
- ✅ Community support
- ❌ No custom domain
- ❌ No advanced authentication

### Paid Plans (Starting ~$20/month)
- ✅ Multiple private apps
- ✅ More resources (CPU/RAM)
- ✅ Custom domains
- ✅ Priority support
- ✅ Team collaboration
- ✅ Advanced security

**Check pricing:** https://streamlit.io/cloud

---

## Security Best Practices

### For Production Deployment:

1. **Strong Passwords:**
   ```toml
   # ❌ Bad
   admin = "admin123"
   
   # ✅ Good
   admin = "aD#9mK$2pL@8nQ!5"
   ```

2. **Regular Password Rotation:**
   - Change passwords every 90 days
   - Update in Streamlit Cloud secrets

3. **Limit User Access:**
   - Only add necessary users
   - Remove users who leave team

4. **Monitor Logs:**
   - Check for suspicious activity
   - Review access patterns

5. **Enable 2FA on GitHub:**
   - Protects your source code
   - Settings → Security → Two-factor authentication

6. **Private Repository:**
   - Keep code private if handling sensitive data
   - Use GitHub private repository

---

## Maintenance Schedule

### Weekly:
- [ ] Check app logs for errors
- [ ] Verify app is running
- [ ] Test login functionality

### Monthly:
- [ ] Review user access
- [ ] Update dependencies
- [ ] Check for package updates

### Quarterly:
- [ ] Rotate passwords
- [ ] Review security settings
- [ ] Update documentation

---

## Cost Estimation

### Free Tier Usage:
- **Cost:** $0/month
- **Apps:** 1 private + unlimited public
- **Resources:** Basic (sufficient for small teams)
- **Users:** Unlimited (with authentication)

### Paid Tier (~$20-100/month):
- Multiple private apps
- More resources
- Custom domain
- Priority support

### Alternative Hosting Costs:
- **Heroku:** Free - $7/month
- **Railway:** $5/month (with credits)
- **AWS/GCP:** ~$10-30/month
- **VPS:** $5-20/month

**Streamlit Cloud is most cost-effective for small-medium teams!**

---

## Migration from Other Platforms

### From Heroku:
1. Remove `Procfile`
2. Keep `requirements.txt`
3. Follow Streamlit Cloud steps above

### From AWS/GCP:
1. Push code to GitHub
2. Deploy to Streamlit Cloud
3. Configure secrets
4. Update DNS (if using custom domain)

---

## Backup & Recovery

### Backup Your Work:

1. **Code:** Always on GitHub (automatic)
2. **Secrets:** Store securely offline
3. **Data:** Not stored on Streamlit Cloud (upload each time)

### Disaster Recovery:

If app is deleted or crashes:
1. Code is safe on GitHub
2. Re-deploy takes 2 minutes
3. Re-configure secrets
4. App is back online!

---

## Success Checklist ✅

Before going live, verify:

- [ ] App works locally without errors
- [ ] All dependencies in requirements.txt
- [ ] Code pushed to GitHub
- [ ] .gitignore excludes secrets.toml
- [ ] Deployed to Streamlit Cloud
- [ ] Secrets configured correctly
- [ ] Strong passwords set
- [ ] Login tested and works
- [ ] File upload tested
- [ ] Analysis works correctly
- [ ] Download feature works
- [ ] URL shared with team
- [ ] Credentials shared securely
- [ ] Documentation updated
- [ ] Monitoring set up

---

## Your App is Now Live! 🎉

**Share your success:**
```
🚀 Sales Price Variance Audit Tool is LIVE!

🔗 URL: https://your-app.streamlit.app
🔐 Secure login required
📊 Real-time analysis
💾 Download reports
📱 Mobile friendly

Questions? Check the documentation or contact admin.
```

---

## Next Steps

1. **Monitor usage** for first week
2. **Gather feedback** from users
3. **Make improvements** based on feedback
4. **Add features** as needed (see src/app.py for ideas)
5. **Scale up** if needed (upgrade plan)

---

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **GitHub Issues:** Your repository issues tab
- **This Guide:** Keep for reference!

---

**Congratulations! Your app is deployed and ready for use! 🎊**
