# GitHub Setup Guide 🐙

## Step-by-Step Guide to Push Your Project to GitHub

### Prerequisites
- Git installed on your computer
- GitHub account (free)

---

## Part 1: Install Git (if not already installed)

### For Windows:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (recommended)
4. Verify installation:
   ```powershell
   git --version
   ```

---

## Part 2: Configure Git (First Time Only)

Open PowerShell or Command Prompt and run:

```powershell
# Set your name (will appear in commits)
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Part 3: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)

1. **Go to GitHub.com and login**
   - Visit: https://github.com

2. **Create New Repository**
   - Click the `+` icon in top-right corner
   - Select "New repository"

3. **Repository Settings:**
   - **Repository name:** `sales-audit-tool` (or your preferred name)
   - **Description:** "Sales Price Variance Audit Tool with Streamlit"
   - **Visibility:** Choose:
     - ✅ **Public** - If you want to share with everyone (required for free Streamlit Cloud)
     - 🔒 **Private** - If you want to keep it private (requires paid Streamlit Cloud)
   - **DON'T** initialize with README, .gitignore, or license (we have these already)

4. **Click "Create repository"**

5. **Copy the repository URL** (you'll need this)
   - Should look like: `https://github.com/YOUR_USERNAME/sales-audit-tool.git`

---

## Part 4: Initialize Git in Your Project

Open PowerShell and navigate to your project folder:

```powershell
# Navigate to your project
cd "c:\Users\aditya\Downloads\ayush  project\final"

# Initialize Git repository
git init

# Check status (see untracked files)
git status
```

---

## Part 5: Add Files to Git

```powershell
# Add all files to staging
git add .

# Verify what will be committed
git status

# If you see secrets.toml in the list, make sure .gitignore is working
# Check .gitignore contains: .streamlit/secrets.toml
```

**⚠️ IMPORTANT:** Before committing, verify `.gitignore` includes:
```
.streamlit/secrets.toml
```

---

## Part 6: Create First Commit

```powershell
# Create your first commit
git commit -m "Initial commit: Sales Price Variance Audit Tool"

# Verify commit was created
git log
```

---

## Part 7: Connect to GitHub

```powershell
# Add GitHub repository as remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/sales-audit-tool.git

# Verify remote was added
git remote -v

# Rename branch to main (if needed)
git branch -M main
```

---

## Part 8: Push to GitHub

### First-time push:

```powershell
# Push code to GitHub
git push -u origin main
```

**You'll be prompted to login:**

#### Option A: Using GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com/
2. Install and login
3. It will handle authentication automatically

#### Option B: Using Personal Access Token
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Sales Audit Tool"
4. Select scopes: `repo` (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. When prompted for password, paste the token instead

#### Option C: Using GitHub CLI (Modern)
```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Login
gh auth login

# Follow prompts (choose HTTPS, login via browser)
```

---

## Part 9: Verify Upload

1. Go to your GitHub repository URL
2. You should see all your files listed
3. Verify `secrets.toml` is NOT visible (should be ignored)

---

## Part 10: Update .gitignore (if needed)

If you accidentally committed sensitive files:

```powershell
# Remove from Git but keep locally
git rm --cached .streamlit/secrets.toml

# Commit the removal
git commit -m "Remove secrets from repository"

# Push changes
git push
```

---

## Common Git Commands for Daily Use

### Check status:
```powershell
git status
```

### Add new/modified files:
```powershell
# Add all changes
git add .

# Or add specific file
git add app.py
```

### Commit changes:
```powershell
git commit -m "Description of changes"
```

### Push to GitHub:
```powershell
git push
```

### Pull latest changes (if working with team):
```powershell
git pull
```

### View history:
```powershell
git log --oneline
```

### Create a new branch:
```powershell
git checkout -b feature-name
```

### Switch branches:
```powershell
git checkout main
```

---

## Typical Workflow

```powershell
# 1. Make changes to your files in VS Code

# 2. Check what changed
git status

# 3. Add changes
git add .

# 4. Commit with message
git commit -m "Add authentication feature"

# 5. Push to GitHub
git push

# 6. Changes are now on GitHub!
```

---

## Creating Releases (Optional)

For version tracking:

1. Go to your GitHub repository
2. Click "Releases" on right side
3. Click "Create a new release"
4. Tag version: `v1.0.0`
5. Release title: "Initial Release"
6. Describe changes
7. Click "Publish release"

---

## Collaboration Features

### Inviting Team Members:
1. Go to repository Settings
2. Click "Collaborators"
3. Add team members by username/email

### Creating Issues:
1. Click "Issues" tab
2. Click "New issue"
3. Describe bug or feature request

### Creating Pull Requests:
1. Create a new branch
2. Make changes
3. Push branch to GitHub
4. Click "Create Pull Request"

---

## Troubleshooting

### Error: "Permission denied"
- Use GitHub Desktop or Personal Access Token
- Don't use your GitHub password (deprecated)

### Error: "Remote origin already exists"
```powershell
# Remove existing remote
git remote remove origin

# Add again with correct URL
git remote add origin YOUR_GITHUB_URL
```

### Error: "Your branch is behind"
```powershell
# Pull latest changes first
git pull origin main

# Then push
git push
```

### Undo last commit (not pushed):
```powershell
git reset --soft HEAD~1
```

### Discard local changes:
```powershell
# Discard all changes
git checkout .

# Or discard specific file
git checkout -- app.py
```

---

## Repository Structure on GitHub

After pushing, your GitHub repo will show:

```
sales-audit-tool/
├── .streamlit/
│   └── config.toml
├── app.py
├── sales.py
├── requirements.txt
├── sample_data.csv
├── run_app.bat
├── README.md
├── DEPLOYMENT_GUIDE.md
├── QUICKSTART.md
├── TROUBLESHOOTING.md
├── GITHUB_SETUP.md
├── .gitignore
└── (secrets.toml is hidden - not on GitHub)
```

---

## Best Practices

### DO:
- ✅ Commit often with clear messages
- ✅ Use .gitignore for sensitive files
- ✅ Write descriptive commit messages
- ✅ Create branches for new features
- ✅ Keep README updated

### DON'T:
- ❌ Commit passwords or API keys
- ❌ Commit large files (>100MB)
- ❌ Use vague commit messages ("fix" or "update")
- ❌ Commit directly to main (use branches for features)

---

## What's Next?

After pushing to GitHub:

1. ✅ **Your code is backed up**
2. ✅ **Ready for deployment** (see DEPLOYMENT_GUIDE.md)
3. ✅ **Can collaborate** with team members
4. ✅ **Version history** is tracked
5. ✅ **Can deploy** to Streamlit Cloud in 2 minutes!

**Ready to deploy?** Continue to the Deployment section below!

---

## Quick Reference Cheat Sheet

```powershell
# Setup (one-time)
git init
git remote add origin URL
git branch -M main

# Daily workflow
git add .
git commit -m "message"
git push

# Check things
git status
git log
git remote -v

# Undo/Fix
git reset HEAD~1        # Undo last commit
git checkout .          # Discard changes
git pull               # Get latest changes

# Branching
git checkout -b new-feature
git checkout main
git merge new-feature
```

---

**Need help?** Check GitHub's documentation: https://docs.github.com
