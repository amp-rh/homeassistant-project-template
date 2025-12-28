# Publishing Home Assistant Add-ons

This guide describes how to publish your add-on to a Home Assistant add-on repository.

## Publishing Methods

### 1. Personal Add-on Repository (Recommended for Starting)

Create your own add-on repository for personal use or sharing.

### 2. Community Add-ons

Submit to the Home Assistant Community Add-ons repository (requires review).

### 3. Official Add-ons

Submit to official Home Assistant add-ons (strict requirements).

## Creating an Add-on Repository

### Repository Structure

```
my-ha-addons/
├── README.md
├── repository.yaml
└── my-addon/
    ├── config.yaml
    ├── build.yaml
    ├── Dockerfile
    ├── DOCS.md
    ├── CHANGELOG.md
    ├── icon.png
    └── logo.png
```

### repository.yaml

```yaml
name: "My Home Assistant Add-ons"
url: "https://github.com/username/my-ha-addons"
maintainer: "Your Name <your.email@example.com>"
```

### Repository README.md

```markdown
# My Home Assistant Add-ons

## Installation

1. Navigate to Supervisor → Add-on Store in Home Assistant
2. Click ⋮ (3 dots) → Repositories
3. Add this repository URL:
   ```
   https://github.com/username/my-ha-addons
   ```
4. Find the add-on in the store and install

## Add-ons

### My Python Add-on

Description of your add-on.

[Documentation](my-addon/DOCS.md)
```

## Add-on Files

### CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Basic functionality

### Changed
- Updated dependencies

### Fixed
- Bug fixes
```

### Icon and Logo

**icon.png**:
- Size: 128x128 pixels
- Format: PNG
- Purpose: Add-on store listing

**logo.png**:
- Size: 256x256 pixels (or larger)
- Format: PNG
- Purpose: Add-on details page

```bash
# Create placeholder icons (replace with actual images)
convert -size 128x128 xc:blue icon.png
convert -size 256x256 xc:blue logo.png
```

### config.yaml

Ensure all required fields are present:

```yaml
name: "My Python Add-on"
description: "A Python-based Home Assistant add-on"
version: "0.1.0"
slug: "my_python_addon"
url: "https://github.com/username/my-ha-addons/tree/main/my-addon"
arch:
  - aarch64
  - amd64
  - armv7
startup: services
boot: auto
init: false
options:
  log_level: "info"
schema:
  log_level: "list(trace|debug|info|warning|error|fatal)?"
image: "ghcr.io/{arch}-addon-my-addon"
```

## Building for Multiple Architectures

### GitHub Actions

Create `.github/workflows/build.yaml`:

```yaml
name: Build Add-on

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    name: Build ${{ matrix.arch }} add-on
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [aarch64, amd64, armv7]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build ${{ matrix.arch }}
        uses: home-assistant/builder@master
        with:
          args: |
            --${{ matrix.arch }} \
            --target my-addon \
            --docker-hub "${{ secrets.DOCKER_USERNAME }}" \
            --password "${{ secrets.DOCKER_PASSWORD }}"
```

### Manual Multi-Arch Build

```bash
# Build for all architectures
for arch in aarch64 amd64 armv7 armhf i386; do
    echo "Building for $arch..."
    ./scripts/build-addon.sh $arch ghcr.io/username/addon-name:$arch-latest
done

# Push to registry
for arch in aarch64 amd64 armv7 armhf i386; do
    podman push ghcr.io/username/addon-name:$arch-latest
done
```

## Container Registry

### GitHub Container Registry (Recommended)

**Setup:**

1. Enable GitHub Packages for your repository
2. Create Personal Access Token with `write:packages` scope
3. Login to GHCR:

```bash
echo $GITHUB_TOKEN | podman login ghcr.io -u USERNAME --password-stdin
```

**Build and Push:**

```bash
# Build
podman build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18" \
    -f addon/Dockerfile \
    -t ghcr.io/username/my-addon:amd64-latest \
    .

# Push
podman push ghcr.io/username/my-addon:amd64-latest
```

**Update config.yaml:**

```yaml
image: "ghcr.io/username/{arch}-addon-my-addon"
```

### Docker Hub

```bash
# Login
podman login docker.io

# Build and push
podman build -t username/my-addon:amd64-latest .
podman push username/my-addon:amd64-latest
```

**Update config.yaml:**

```yaml
image: "docker.io/username/{arch}-my-addon"
```

## Versioning

### Semantic Versioning

Follow [semver](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- `1.0.0` - Initial release
- `1.0.1` - Bug fixes
- `1.1.0` - New features
- `2.0.0` - Breaking changes

### Version Workflow

```bash
# 1. Update version in config.yaml
version: "0.2.0"

# 2. Update CHANGELOG.md
echo "## [0.2.0] - $(date +%Y-%m-%d)" >> CHANGELOG.md

# 3. Commit changes
git add addon/config.yaml CHANGELOG.md
git commit -m "Bump version to 0.2.0"

# 4. Tag release
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0

# 5. Build and push
./scripts/build-addon.sh
```

## Testing Before Release

### Pre-Release Checklist

- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Builds for all architectures
- [ ] Tested on local HA instance
- [ ] DOCS.md is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version number is bumped
- [ ] Icons are present
- [ ] No hardcoded credentials
- [ ] No debug logging in production

### Beta Testing

```yaml
# config.yaml for beta
name: "My Add-on (Beta)"
version: "0.2.0-beta.1"
slug: "my_addon_beta"
```

## Publishing Workflow

### 1. Prepare Release

```bash
# Update version
vim addon/config.yaml

# Update changelog
vim CHANGELOG.md

# Commit
git add addon/config.yaml CHANGELOG.md
git commit -m "Release version 0.2.0"
```

### 2. Build All Architectures

```bash
# Build script for all archs
./scripts/build-all-archs.sh

# Or use GitHub Actions
git push origin main
# Monitor build in GitHub Actions
```

### 3. Push to Registry

```bash
# Push all architecture images
./scripts/push-all-archs.sh

# Or automated via GitHub Actions
```

### 4. Tag Release

```bash
# Create tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push tag
git push origin v0.2.0
```

### 5. Create GitHub Release

```bash
# Using GitHub CLI
gh release create v0.2.0 \
    --title "v0.2.0" \
    --notes-file CHANGELOG.md

# Or create manually in GitHub UI
```

### 6. Update Repository

```bash
# Push to add-on repository
cd my-ha-addons
git pull

# Copy updated add-on files
cp -r ../my-addon-source/addon/* my-addon/

# Commit and push
git add my-addon/
git commit -m "Update My Add-on to v0.2.0"
git push
```

## Automated Publishing

### GitHub Actions Complete Workflow

```yaml
name: Publish Add-on

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [aarch64, amd64, armv7, armhf, i386]

    steps:
      - uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: home-assistant/builder@master
        with:
          args: |
            --${{ matrix.arch }} \
            --target addon \
            --image "ghcr.io/${{ github.repository }}" \
            --docker-hub "ghcr.io" \
            --no-latest

      - name: Create Release
        if: matrix.arch == 'amd64'
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

## Distribution

### Share Repository URL

Users add your repository:

```
https://github.com/username/my-ha-addons
```

### README Badge

Add build status to README:

```markdown
![Build](https://github.com/username/my-ha-addons/workflows/Build/badge.svg)
[![GitHub Release][releases-shield]][releases]

[releases-shield]: https://img.shields.io/github/release/username/my-ha-addons.svg
[releases]: https://github.com/username/my-ha-addons/releases
```

## Best Practices

1. **Test thoroughly** before each release
2. **Use semantic versioning** for clarity
3. **Maintain CHANGELOG** for users
4. **Build for all architectures** to maximize compatibility
5. **Automate builds** with GitHub Actions
6. **Use container registry** for reliability
7. **Document breaking changes** prominently
8. **Provide migration guides** for major versions
9. **Respond to issues** promptly
10. **Keep dependencies updated** regularly

## See Also

- `.agents/docs/workflows/repository-setup.md` - Repository structure
- `.agents/docs/workflows/local-development.md` - Development workflow
- [Home Assistant Add-on Repository](https://developers.home-assistant.io/docs/add-ons/repository)
