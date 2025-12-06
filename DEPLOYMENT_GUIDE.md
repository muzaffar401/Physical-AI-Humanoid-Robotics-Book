# GitHub Pages Deployment Guide

## Step-by-Step Instructions

### 1. GitHub Repository Settings

1. GitHub repository me jao: `https://github.com/muzaffar401/Physical-AI-Humanoid-Robotics-Book`
2. **Settings** tab click karo
3. Left sidebar me **Pages** section me jao
4. **Source** dropdown me **GitHub Actions** select karo
5. Save karo

### 2. Code Push Karo

Ab aapko code push karna hai:

```bash
# Terminal me ye commands run karo:
cd C:\Users\ma940\Desktop\Physical-AI-Humanoid-Robotics-Book

# Git status check karo
git status

# Agar koi changes hain to add karo
git add .

# Commit karo
git commit -m "Add GitHub Pages deployment workflow"

# Push karo
git push origin main
```

### 3. GitHub Actions Check Karo

1. GitHub repository me jao
2. **Actions** tab click karo
3. "Deploy Docusaurus to GitHub Pages" workflow dikhega
4. Click karke check karo ki build successfully ho raha hai

### 4. Site Access Karo

Build complete hone ke baad, aapka site yahan available hoga:
- **URL**: `https://muzaffar401.github.io/Physical-AI-Humanoid-Robotics-Book/`

## Important Notes

### Base URL Configuration

Agar aapko site root me deploy karna hai (subdirectory ke bina), to `book_frontend/docusaurus.config.ts` me ye change karo:

```typescript
baseUrl: '/',  // Instead of '/Physical-AI-Humanoid-Robotics-Book/'
```

Aur workflow file me path change karo:
```yaml
path: book_frontend/build
```

### Manual Deployment (Alternative)

Agar GitHub Actions use nahi karna chahte, to manually bhi deploy kar sakte ho:

```bash
cd book_frontend
npm install
npm run build
npm run deploy
```

Ye command `gh-pages` branch me automatically deploy kar dega.

## Troubleshooting

### Build Fail Ho Raha Hai

1. **Actions** tab me jao
2. Failed workflow click karo
3. Error message check karo
4. Common issues:
   - Node version mismatch
   - Missing dependencies
   - Build errors

### Site Load Nahi Ho Raha

1. Base URL check karo - `docusaurus.config.ts` me sahi hai?
2. GitHub Pages settings me source sahi set hai?
3. Browser cache clear karo
4. Hard refresh karo (Ctrl+Shift+R)

### Local Testing

Deploy se pehle local me test karo:

```bash
cd book_frontend
npm run build
npm run serve
```

Phir browser me `http://localhost:3000/Physical-AI-Humanoid-Robotics-Book/` open karo.

## Next Steps

1. ✅ GitHub Pages settings configure karo
2. ✅ Code push karo
3. ✅ Actions workflow check karo
4. ✅ Site verify karo
5. ✅ Custom domain add karo (optional)

## Support

Agar koi issue aaye to:
- GitHub Actions logs check karo
- Docusaurus documentation: https://docusaurus.io/docs/deployment
- GitHub Pages docs: https://docs.github.com/en/pages

