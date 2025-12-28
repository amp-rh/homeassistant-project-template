# Authentication in Home Assistant Add-ons

Authentication patterns for Home Assistant add-ons accessing the Home Assistant API and providing secure web interfaces.

## Overview

Add-ons can use:
1. **Long-lived access tokens** - Provided by Supervisor
2. **Ingress authentication** - Automatic user authentication
3. **Custom authentication** - For exposed ports

## Supervisor-Provided Tokens

### Getting Access Token

The Supervisor provides a long-lived access token for Home Assistant API access:

```python
from my_addon.supervisor import SupervisorAPI

async with SupervisorAPI() as supervisor:
    # Get Home Assistant API credentials
    api_info = await supervisor.get_homeassistant_api()
    ha_token = api_info['data']['password']  # Long-lived access token
    ha_url = f"http://{api_info['data']['ip']}:{api_info['data']['port']}"
```

### Using the Token

```python
import aiohttp

headers = {
    "Authorization": f"Bearer {ha_token}",
    "Content-Type": "application/json"
}

async with aiohttp.ClientSession() as session:
    # Get states
    async with session.get(
        f"{ha_url}/api/states",
        headers=headers
    ) as resp:
        states = await resp.json()

    # Call service
    async with session.post(
        f"{ha_url}/api/services/light/turn_on",
        headers=headers,
        json={"entity_id": "light.bedroom"}
    ) as resp:
        result = await resp.json()
```

## Ingress Authentication

When using ingress, authentication is handled automatically by Home Assistant.

### Configuration

```yaml
# addon/config.yaml
ingress: true
ingress_port: 8000
panel_admin: true  # Restrict to admin users only
```

### Token Validation (Optional)

```python
import os
from aiohttp import web

@web.middleware
async def ingress_auth_middleware(request, handler):
    """Validate ingress token."""
    expected_token = os.getenv('INGRESS_TOKEN')

    if expected_token:
        token = request.headers.get('X-Ingress-Token')
        if token != expected_token:
            return web.Response(status=403, text='Forbidden')

    return await handler(request)

app = web.Application(middlewares=[ingress_auth_middleware])
```

### User Information

Ingress provides user information in headers:

```python
async def handle_request(request):
    # Get authenticated user (if available)
    user_id = request.headers.get('X-Hass-User-ID')
    is_admin = request.headers.get('X-Hass-Is-Admin') == '1'

    return web.json_response({
        'user_id': user_id,
        'is_admin': is_admin
    })
```

## Custom Authentication

For add-ons with exposed ports, implement custom authentication.

### Basic Authentication

```python
import secrets
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware

# Generate secure credentials at startup
username = "admin"
password = secrets.token_urlsafe(16)

# Log credentials for user
logging.info(f"Username: {username}")
logging.info(f"Password: {password}")

# Setup middleware
auth = BasicAuthMiddleware(
    username=username,
    password=password,
    force=True
)

app = web.Application(middlewares=[auth])
```

### Token-Based Authentication

```python
import secrets
from aiohttp import web

# Generate API token at startup
API_TOKEN = secrets.token_urlsafe(32)
logging.info(f"API Token: {API_TOKEN}")

@web.middleware
async def token_auth_middleware(request, handler):
    """Validate API token."""
    # Skip auth for health check
    if request.path == '/health':
        return await handler(request)

    # Check Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return web.Response(status=401, text='Unauthorized')

    token = auth_header[7:]  # Remove 'Bearer ' prefix
    if token != API_TOKEN:
        return web.Response(status=403, text='Forbidden')

    return await handler(request)

app = web.Application(middlewares=[token_auth_middleware])
```

### Session-Based Authentication

```python
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
import secrets

# Generate secret key
secret_key = fernet.Fernet.generate_key()

# Setup sessions
setup(app, EncryptedCookieStorage(secret_key))

async def login(request):
    """Login endpoint."""
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if validate_credentials(username, password):
        session = await get_session(request)
        session['user'] = username
        return web.json_response({'status': 'logged_in'})

    return web.json_response({'status': 'failed'}, status=401)

async def protected_handler(request):
    """Protected endpoint."""
    session = await get_session(request)
    if 'user' not in session:
        return web.json_response({'error': 'Unauthorized'}, status=401)

    return web.json_response({'user': session['user']})

app.router.add_post('/api/login', login)
app.router.add_get('/api/protected', protected_handler)
```

## Storing Credentials

### Environment Variables

Store credentials in add-on configuration:

```yaml
# addon/config.yaml
options:
  api_key: ""
  api_secret: ""

schema:
  api_key: "password"
  api_secret: "password"
```

```python
from my_addon.config import Config

config = Config.from_options()
api_key = config.api_key
api_secret = config.api_secret
```

### Secrets in Home Assistant

Reference secrets defined in Home Assistant:

```yaml
# addon/config.yaml
options:
  api_key: "!secret my_addon_api_key"
```

Users add to their `secrets.yaml`:

```yaml
# secrets.yaml (in Home Assistant config)
my_addon_api_key: "actual-secret-key-here"
```

### Persistent Storage

Store generated credentials persistently:

```python
import json
from pathlib import Path

def load_or_create_credentials():
    """Load existing credentials or create new ones."""
    cred_file = Path('/data/credentials.json')

    if cred_file.exists():
        with open(cred_file) as f:
            return json.load(f)

    # Generate new credentials
    credentials = {
        'api_key': secrets.token_urlsafe(32),
        'created_at': datetime.now().isoformat()
    }

    with open(cred_file, 'w') as f:
        json.dump(credentials, f)

    return credentials
```

## OAuth 2.0 Integration

For services requiring OAuth:

```python
from aiohttp import web
import aiohttp

async def oauth_start(request):
    """Start OAuth flow."""
    client_id = config.oauth_client_id
    redirect_uri = f"{request.url.scheme}://{request.host}/api/oauth/callback"

    auth_url = (
        f"https://provider.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
    )

    return web.HTTPFound(auth_url)

async def oauth_callback(request):
    """Handle OAuth callback."""
    code = request.query.get('code')

    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://provider.com/oauth/token',
            data={
                'client_id': config.oauth_client_id,
                'client_secret': config.oauth_client_secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
        ) as resp:
            tokens = await resp.json()

    # Store tokens
    save_tokens(tokens)

    return web.Response(text='Authentication successful!')

app.router.add_get('/api/oauth/start', oauth_start)
app.router.add_get('/api/oauth/callback', oauth_callback)
```

## Best Practices

1. **Use ingress when possible** - Simplest and most secure
2. **Generate secure tokens** - Use `secrets.token_urlsafe()`
3. **Log credentials once** - On first start for user reference
4. **Store in /data** - Persist across restarts
5. **Use HTTPS for exposed ports** - Encrypt traffic
6. **Validate all inputs** - Prevent injection attacks
7. **Implement rate limiting** - Prevent brute force
8. **Rotate tokens periodically** - Improve security

## Security Considerations

### Token Security

```python
# Good: Secure token generation
import secrets
token = secrets.token_urlsafe(32)

# Bad: Weak token generation
import random
token = str(random.randint(1000, 9999))  # Don't do this!
```

### Password Hashing

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password with bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

### Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Simple rate limiter."""

    def __init__(self, max_requests: int = 10, window: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window)
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed."""
        now = datetime.now()
        cutoff = now - self.window

        # Clean old requests
        self.requests[identifier] = [
            ts for ts in self.requests[identifier]
            if ts > cutoff
        ]

        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False

        self.requests[identifier].append(now)
        return True

# Usage
rate_limiter = RateLimiter(max_requests=10, window=60)

@web.middleware
async def rate_limit_middleware(request, handler):
    client_ip = request.remote
    if not rate_limiter.is_allowed(client_ip):
        return web.Response(status=429, text='Too Many Requests')
    return await handler(request)
```

## See Also

- `.agents/docs/architecture/homeassistant/ingress.md` - Ingress setup
- `.agents/docs/patterns/options-handling.md` - Configuration
- [Home Assistant Authentication](https://developers.home-assistant.io/docs/auth_api/)
