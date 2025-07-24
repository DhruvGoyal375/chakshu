# GitHub Actions Workflows

This directory contains automated workflows for the Chakshu project.

## 📖 Documentation Workflows

### `deploy-docs.yml` - Simple Documentation Deployment
**Triggers:**
- Push to `production` branch with changes to documentation files
- Manual trigger via workflow dispatch

**What it does:**
- Builds MkDocs documentation
- Deploys to GitHub Pages automatically
- Simple, fast deployment for quick updates

### `docs-ci.yml` - Comprehensive Documentation CI/CD
**Triggers:**
- Push to `production` or `main` branches with documentation changes
- Pull requests to `production` or `main` branches
- Manual trigger with optional deployment

**What it does:**
1. **Validation Job:**
   - Validates MkDocs configuration
   - Builds documentation to check for errors
   - Uploads build artifacts for review

2. **Deployment Job:** (only on production branch)
   - Deploys to GitHub Pages
   - Creates deployment summary
   - Provides deployment URL and status

3. **Notification Job:**
   - Notifies on deployment failures
   - Creates failure summary with details

## 🚀 Usage

### Automatic Deployment
Simply push changes to the `production` branch:

```bash
git checkout production
# Make changes to chakshu/docs/ or chakshu/mkdocs.yml
git add chakshu/docs/ chakshu/mkdocs.yml
git commit -m "docs: update documentation"
git push origin production
```

The documentation will automatically build and deploy to:
**https://DhruvGoyal375.github.io/chakshu/**

### Manual Deployment
You can manually trigger deployment from the GitHub Actions tab:

1. Go to **Actions** tab in your repository
2. Select **Documentation CI/CD** workflow
3. Click **Run workflow**
4. Choose whether to deploy to GitHub Pages

### Pull Request Validation
When creating pull requests that modify documentation:

1. The workflow will automatically validate your changes
2. Build artifacts will be available for review
3. No deployment occurs until merged to production

## 📁 Files Monitored

The workflows trigger on changes to:
- `chakshu/docs/**` - All documentation files
- `chakshu/mkdocs.yml` - MkDocs configuration
- `apiResponses.md` - API response examples
- `docs-requirements.txt` - Documentation dependencies
- `.github/workflows/docs-ci.yml` - Workflow configuration

## 🔧 Dependencies

Documentation dependencies are managed in `docs-requirements.txt`:
- MkDocs and Material theme
- Python Markdown extensions
- Additional plugins for enhanced functionality

## 🛠️ Troubleshooting

### Common Issues

**Build Failures:**
- Check MkDocs configuration syntax
- Verify all referenced files exist
- Check for broken internal links

**Deployment Failures:**
- Ensure GitHub Pages is enabled in repository settings
- Check repository permissions for GitHub Actions
- Verify branch protection rules don't block deployment

**Missing Dependencies:**
- Update `docs-requirements.txt` if using new MkDocs plugins
- Check Python version compatibility

### Debugging

1. **Check Workflow Logs:**
   - Go to Actions tab → Select failed workflow → View logs

2. **Local Testing:**
   ```bash
   cd chakshu
   mkdocs build --strict  # Check for build errors
   mkdocs serve           # Test locally
   ```

3. **Validate Configuration:**
   ```bash
   mkdocs build --verbose  # Detailed build output
   ```

## 📊 Workflow Status

You can check the status of documentation deployments:

- **Badge**: Add to README for status visibility
- **Actions Tab**: View detailed workflow history
- **Deployments**: Check GitHub Pages deployment status

## 🔒 Security

- Workflows use `GITHUB_TOKEN` for authentication
- No sensitive information is exposed in logs
- Deployments are restricted to production branch
- Pull request builds don't have deployment permissions