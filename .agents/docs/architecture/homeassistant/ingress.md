# Ingress - Web UI for Add-ons

This document describes how to implement web UIs for Home Assistant add-ons using Ingress.

## Overview

Ingress allows add-ons to provide web interfaces accessible through the Home Assistant UI without exposing ports or requiring authentication.

**Benefits:**
- No port exposure needed
- Automatic authentication via Home Assistant
- SSL/TLS handled by Home Assistant
- Accessible in HA sidebar

## Configuration

### Enable Ingress

```yaml
# addon/config.yaml
panel_icon: mdi:flask
panel_title: "My Add-on"
panel_admin: true  # Only show to admins
ingress: true
ingress_port: 8000
```

**Fields:**
- `panel_icon`: Material Design Icon for sidebar
- `panel_title`: Display name in sidebar
- `panel_admin`: Restrict to admin users
- `ingress`: Enable ingress feature
- `ingress_port`: Internal port your app listens on

### No Port Mapping Required

When using ingress, **do not** expose ports:

```yaml
# DON'T DO THIS with ingress
# ports:
#   8000/tcp: 8000
```

## Web Server Implementation

### aiohttp Example

```python
from aiohttp import web
import os

def create_app() -> web.Application:
    """Create web application."""
    app = web.Application()

    # Get ingress path if running in HA
    ingress_path = os.getenv('INGRESS_PATH', '')

    # Setup routes with ingress prefix
    app.router.add_get(f'{ingress_path}/', handle_index)
    app.router.add_get(f'{ingress_path}/api/status', handle_status)

    # Serve static files
    app.router.add_static(
        f'{ingress_path}/static',
        'static',
        name='static'
    )

    return app

async def handle_index(request: web.Request) -> web.Response:
    """Serve main page."""
    return web.Response(
        text="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Add-on</title>
        </head>
        <body>
            <h1>My Add-on Dashboard</h1>
            <div id="content"></div>
            <script>
                // Use relative URLs for API calls
                fetch('./api/status')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('content').innerHTML =
                            `Status: ${data.status}`;
                    });
            </script>
        </body>
        </html>
        """,
        content_type='text/html'
    )

# Start server
if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8000)
```

### Flask Example

```python
from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Get ingress path
    ingress_path = os.getenv('INGRESS_PATH', '')

    @app.route(f'{ingress_path}/')
    def index():
        return '<h1>My Add-on</h1>'

    @app.route(f'{ingress_path}/api/status')
    def status():
        return {'status': 'ok'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
```

## Environment Variables

Home Assistant provides these environment variables:

```python
import os

# Ingress URL path (e.g., /api/hassio_ingress/xxx)
ingress_path = os.getenv('INGRESS_PATH', '')

# Ingress entry point (e.g., /api/hassio_ingress/xxx)
ingress_entry = os.getenv('INGRESS_ENTRY', '')

# Ingress token for backend validation
ingress_token = os.getenv('INGRESS_TOKEN', '')
```

## Authentication

### Automatic Authentication

Ingress handles authentication automatically. Users are authenticated through Home Assistant.

### Backend Validation (Optional)

For additional security, validate ingress tokens:

```python
from aiohttp import web
import os

@web.middleware
async def ingress_auth_middleware(request, handler):
    """Validate ingress token."""
    ingress_token = os.getenv('INGRESS_TOKEN')

    if ingress_token:
        # Check X-Ingress-Token header
        token = request.headers.get('X-Ingress-Token')
        if token != ingress_token:
            return web.Response(status=403, text='Forbidden')

    return await handler(request)

# Add middleware
app.middlewares.append(ingress_auth_middleware)
```

## URL Handling

### Relative URLs

Always use relative URLs in HTML/JavaScript:

```html
<!-- Good: Relative URLs -->
<link rel="stylesheet" href="./static/style.css">
<script src="./static/app.js"></script>

<script>
fetch('./api/status')
    .then(r => r.json())
    .then(data => console.log(data));
</script>

<!-- Bad: Absolute URLs -->
<link rel="stylesheet" href="/static/style.css">
<script>
fetch('/api/status')  // Will fail under ingress
</script>
```

### Base URL

For complex apps, use a base URL:

```html
<!DOCTYPE html>
<html>
<head>
    <base href="./">
    <script>
        // All relative URLs now work correctly
        window.BASE_URL = document.querySelector('base').href;
    </script>
</head>
</html>
```

### API Calls

```javascript
// Get base URL from current page
const baseUrl = window.location.pathname.replace(/\/$/, '');

// Make API calls relative to base
fetch(`${baseUrl}/api/status`)
    .then(r => r.json())
    .then(data => console.log(data));
```

## WebSocket Support

WebSockets work through ingress with proper URL construction:

```javascript
// Construct WebSocket URL
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${protocol}//${window.location.host}${window.location.pathname}/ws`;

const ws = new WebSocket(wsUrl);

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};
```

```python
from aiohttp import web

async def websocket_handler(request):
    """WebSocket endpoint."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Echo: {msg.data}")

    return ws

# Add route
ingress_path = os.getenv('INGRESS_PATH', '')
app.router.add_get(f'{ingress_path}/ws', websocket_handler)
```

## Static Files

### Serving Static Files

```python
# aiohttp
app.router.add_static(
    f'{ingress_path}/static',
    'static',
    name='static'
)

# Flask
app = Flask(__name__, static_url_path=f'{ingress_path}/static')
```

### Referencing Static Files

```html
<!-- Use relative paths -->
<link rel="stylesheet" href="./static/css/style.css">
<script src="./static/js/app.js"></script>
<img src="./static/images/logo.png">
```

## Common Issues

### 404 on Resources

**Problem:** CSS, JS, images return 404

**Solution:** Use relative URLs (`./ ` prefix) or base tag

```html
<base href="./">
<link rel="stylesheet" href="static/style.css">
```

### API Calls Fail

**Problem:** API calls go to wrong path

**Solution:** Use relative URLs in fetch/axios

```javascript
// Good
fetch('./api/status')

// Bad
fetch('/api/status')
```

### Redirects Don't Work

**Problem:** Server redirects to absolute URLs

**Solution:** Use relative redirects

```python
# Good
return web.HTTPFound('./dashboard')

# Bad
return web.HTTPFound('/dashboard')
```

## Local Development

For local development without ingress:

```python
import os

def create_app():
    app = web.Application()
    ingress_path = os.getenv('INGRESS_PATH', '')

    # Routes work both with and without ingress
    app.router.add_get(f'{ingress_path}/', handle_index)

    return app

# Local: ingress_path = ''
# HA: ingress_path = '/api/hassio_ingress/xxx'
```

Test locally:

```bash
# No ingress path
python -m my_addon

# Simulate ingress path
INGRESS_PATH=/api/test python -m my_addon
```

## Best Practices

1. **Always use relative URLs** - Works with and without ingress
2. **Test both modes** - Local dev and ingress
3. **Use base tag** - Simplifies URL handling
4. **Validate ingress token** - Optional additional security
5. **Handle WebSocket upgrades** - Construct URLs dynamically
6. **Serve static files correctly** - Use proper prefixes
7. **Don't hardcode paths** - Use INGRESS_PATH environment variable

## Complete Example

```python
from aiohttp import web
import os
import logging

logger = logging.getLogger(__name__)

def create_app() -> web.Application:
    """Create ingress-compatible web application."""
    app = web.Application()

    # Get ingress configuration
    ingress_path = os.getenv('INGRESS_PATH', '')
    ingress_token = os.getenv('INGRESS_TOKEN')

    logger.info(f"Ingress path: {ingress_path or '(none)'}")

    # Middleware for ingress token validation
    if ingress_token:
        @web.middleware
        async def validate_ingress(request, handler):
            token = request.headers.get('X-Ingress-Token')
            if token != ingress_token:
                return web.Response(status=403)
            return await handler(request)

        app.middlewares.append(validate_ingress)

    # Routes
    app.router.add_get(f'{ingress_path}/', index_handler)
    app.router.add_get(f'{ingress_path}/api/status', status_handler)
    app.router.add_get(f'{ingress_path}/ws', websocket_handler)

    # Static files
    app.router.add_static(
        f'{ingress_path}/static',
        'static',
        name='static'
    )

    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8000)
```

## See Also

- [Home Assistant Ingress Documentation](https://developers.home-assistant.io/docs/add-ons/presentation#ingress)
- `.agents/docs/patterns/addon-structure.md` - Add-on structure
