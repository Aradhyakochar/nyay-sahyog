# 📦 Compression Guide - What to Archive

## ✅ Files to INCLUDE in Archive

### **Backend:**
```
backend/
├── *.py                    # All Python source files
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker configuration
├── env.example            # Environment template
├── env.test.example       # Test environment template
└── database_migration.py  # Migration script
```

### **Frontend:**
```
frontend/
├── src/                   # All source files
│   ├── *.tsx, *.ts       # TypeScript files
│   ├── *.jsx, *.js       # JavaScript files
│   ├── *.css             # Stylesheets
│   └── index.html        # HTML entry
├── package.json           # Dependencies
├── vite.config.ts        # Vite config
├── tsconfig.json         # TypeScript config
├── tailwind.config.js    # Tailwind config
├── postcss.config.js     # PostCSS config
├── Dockerfile            # Docker config
├── Dockerfile.prod       # Production Docker
├── nginx.conf            # Nginx config
└── env.example           # Environment template
```

### **Root Files:**
```
projectR/
├── *.md                   # All documentation
├── *.bat                  # Batch scripts
├── docker-compose.yml     # Docker compose
├── docker-compose.prod.yml # Production compose
└── README.md             # Main readme
```

---

## ❌ Files to EXCLUDE from Archive

### **Auto-Generated:**
- `node_modules/` - Can be reinstalled with `npm install`
- `venv/` - Can be recreated with `python -m venv venv`
- `__pycache__/` - Python cache (auto-generated)
- `dist/` - Build output (can be regenerated)
- `.next/` - Next.js build (if exists)

### **Database Files:**
- `backend/instance/*.db` - SQLite database (can be regenerated with seed_data.py)
- `*.db-journal` - SQLite journal files

### **Environment Files:**
- `.env` - Contains secrets (use `.env.example` instead)
- `.env.local` - Local environment variables

### **IDE/Editor:**
- `.vscode/` - VS Code settings
- `.idea/` - IntelliJ settings
- `*.swp`, `*.swo` - Vim swap files

### **OS Files:**
- `.DS_Store` - macOS
- `Thumbs.db` - Windows
- `desktop.ini` - Windows

---

## 📦 Compression Commands

### **Option 1: PowerShell (Windows)**
```powershell
# Navigate to project root
cd C:\Users\KIIT\OneDrive\Desktop\projectR

# Create archive (excludes node_modules, venv, etc.)
Compress-Archive -Path `
  backend\*.py,backend\*.txt,backend\*.yml,backend\*.example,backend\Dockerfile,`
  frontend\src,frontend\*.json,frontend\*.ts,frontend\*.js,frontend\*.html,frontend\*.conf,frontend\Dockerfile*,`
  *.md,*.bat,*.yml `
  -DestinationPath nyay_sahyog_project.zip `
  -Force
```

### **Option 2: Manual Selection**
1. Select these folders/files:
   - `backend/` (except `venv/`, `__pycache__/`, `instance/*.db`)
   - `frontend/` (except `node_modules/`, `dist/`)
   - All `.md` files
   - All `.bat` files
   - `docker-compose.yml` files
2. Right-click → Send to → Compressed (zipped) folder

### **Option 3: Using 7-Zip (if installed)**
```powershell
7z a -tzip nyay_sahyog_project.zip `
  backend\*.py backend\*.txt backend\*.yml backend\*.example backend\Dockerfile `
  frontend\src frontend\*.json frontend\*.ts frontend\*.js frontend\*.html frontend\*.conf frontend\Dockerfile* `
  *.md *.bat *.yml `
  -xr!node_modules -xr!venv -xr!__pycache__ -xr!dist -xr!*.db
```

---

## 📋 Pre-Compression Checklist

Before compressing, ensure:

- [ ] All code is saved
- [ ] No `.env` files included (only `.env.example`)
- [ ] Database file excluded (or use seed scripts)
- [ ] `node_modules/` excluded
- [ ] `venv/` excluded
- [ ] Documentation files included
- [ ] Batch scripts included
- [ ] Docker files included

---

## 📊 Estimated Archive Size

**Included:**
- Backend Python files: ~50 KB
- Frontend source: ~200 KB
- Documentation: ~100 KB
- Config files: ~20 KB
- **Total: ~370 KB** (without dependencies)

**Excluded:**
- `node_modules/`: ~200-500 MB
- `venv/`: ~100-300 MB
- Database: ~1-10 MB

**Final Archive:** ~500 KB - 1 MB (compressed)

---

## 🔄 After Extraction

To restore the project:

1. **Extract archive**
2. **Backend setup:**
   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup:**
   ```powershell
   cd frontend
   npm install
   ```

4. **Environment files:**
   ```powershell
   # Copy examples
   copy backend\env.example backend\.env
   copy frontend\env.example frontend\.env
   ```

5. **Seed data:**
   ```powershell
   cd backend
   venv\Scripts\activate
   python seed_data.py
   ```

---

## ✅ Verification

After compression, verify:
- [ ] Archive opens successfully
- [ ] All source files present
- [ ] No sensitive data (.env files)
- [ ] Documentation included
- [ ] Can extract and run project

---

**Archive Name:** `nyay_sahyog_project.zip`  
**Location:** Project root directory


