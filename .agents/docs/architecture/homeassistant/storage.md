# Persistent Storage in Home Assistant Add-ons

This document describes storage patterns and best practices for Home Assistant add-ons.

## Storage Locations

### /data - Add-on Data Directory

**Purpose:** Persistent storage for add-on-specific data

**Characteristics:**
- Unique to each add-on
- Persists across add-on restarts
- Survives add-on updates
- Backed up with Home Assistant backups
- Full read/write access

**Usage:**

```python
from pathlib import Path

DATA_DIR = Path("/data")

# Store configuration
config_file = DATA_DIR / "config.json"
with open(config_file, 'w') as f:
    json.dump(config, f)

# Store database
db_file = DATA_DIR / "database.sqlite"
conn = sqlite3.connect(db_file)

# Store logs
log_file = DATA_DIR / "addon.log"
```

### /share - Shared Directory

**Purpose:** Data shared between all add-ons and Home Assistant

**Characteristics:**
- Accessible by all add-ons
- Use for inter-add-on file exchange
- Typically `/usr/share/hassio/share` on host
- Full read/write access

**Usage:**

```python
from pathlib import Path

SHARE_DIR = Path("/share")

# Share files with other add-ons
export_file = SHARE_DIR / "my_addon_export.json"
with open(export_file, 'w') as f:
    json.dump(data, f)

# Read files from other add-ons
import_file = SHARE_DIR / "other_addon_data.csv"
if import_file.exists():
    df = pd.read_csv(import_file)
```

### /config - Home Assistant Configuration

**Purpose:** Access to Home Assistant configuration

**Characteristics:**
- Contains HA configuration.yaml and related files
- Read-only by default
- Requires `homeassistant_config: true` in addon/config.yaml
- Use sparingly

**Configuration:**

```yaml
# addon/config.yaml
homeassistant_config: true
```

**Usage:**

```python
from pathlib import Path
import yaml

CONFIG_DIR = Path("/config")

# Read Home Assistant configuration
ha_config_file = CONFIG_DIR / "configuration.yaml"
if ha_config_file.exists():
    with open(ha_config_file) as f:
        ha_config = yaml.safe_load(f)

# Read secrets
secrets_file = CONFIG_DIR / "secrets.yaml"
if secrets_file.exists():
    with open(secrets_file) as f:
        secrets = yaml.safe_load(f)
```

### /ssl - SSL Certificates

**Purpose:** Access to SSL/TLS certificates

**Characteristics:**
- Shared SSL certificates
- Requires `ssl: true` in addon/config.yaml
- Read-only access

**Configuration:**

```yaml
# addon/config.yaml
ssl: true
```

**Usage:**

```python
from pathlib import Path
import ssl

SSL_DIR = Path("/ssl")

# Create SSL context
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    certfile=SSL_DIR / "fullchain.pem",
    keyfile=SSL_DIR / "privkey.pem"
)

# Use with aiohttp
from aiohttp import web
web.run_app(app, ssl_context=ssl_context)
```

### /backup - Backup Directory

**Purpose:** Create and access backups

**Characteristics:**
- Requires `backup: true` in addon/config.yaml
- Use for backup-related operations
- Limited access

**Configuration:**

```yaml
# addon/config.yaml
backup: true
```

### /media - Media Directory

**Purpose:** Access to Home Assistant media

**Characteristics:**
- Home Assistant media files
- Requires `media: true` in addon/config.yaml
- Useful for media-related add-ons

**Configuration:**

```yaml
# addon/config.yaml
media: true
```

## Data Persistence Patterns

### Configuration Files

```python
import json
from pathlib import Path
from typing import Any

class PersistentConfig:
    """Manage persistent configuration."""

    def __init__(self, path: Path = Path("/data/config.json")):
        self.path = path
        self.data: dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from disk."""
        if self.path.exists():
            with open(self.path) as f:
                self.data = json.load(f)

    def save(self):
        """Save configuration to disk."""
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value and save."""
        self.data[key] = value
        self.save()
```

### SQLite Database

```python
import sqlite3
from pathlib import Path
from contextlib import contextmanager

class Database:
    """SQLite database manager."""

    def __init__(self, db_path: Path = Path("/data/database.sqlite")):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    data TEXT
                )
            """)
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def add_event(self, event_type: str, data: dict):
        """Add event to database."""
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO events (event_type, data) VALUES (?, ?)",
                (event_type, json.dumps(data))
            )
            conn.commit()
```

### State Files

```python
import json
from pathlib import Path
from datetime import datetime

class StateManager:
    """Manage add-on state."""

    def __init__(self, state_file: Path = Path("/data/state.json")):
        self.state_file = state_file
        self.state = self.load_state()

    def load_state(self) -> dict:
        """Load state from file."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {
            "started_at": datetime.now().isoformat(),
            "status": "initializing"
        }

    def save_state(self):
        """Save state to file."""
        self.state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def update_status(self, status: str):
        """Update status and save."""
        self.state["status"] = status
        self.save_state()
```

## File Management

### Atomic Writes

```python
import tempfile
import shutil
from pathlib import Path

def atomic_write(path: Path, content: str):
    """Write file atomically to prevent corruption."""
    # Write to temporary file
    fd, temp_path = tempfile.mkstemp(dir=path.parent)
    try:
        with open(fd, 'w') as f:
            f.write(content)
        # Atomic move
        shutil.move(temp_path, path)
    except:
        # Clean up temp file on error
        Path(temp_path).unlink(missing_ok=True)
        raise
```

### File Rotation

```python
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

def setup_file_logging():
    """Setup rotating file logger."""
    log_file = Path("/data/addon.log")

    handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )

    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logging.getLogger().addHandler(handler)
```

### Directory Structure

```python
from pathlib import Path

def setup_directories():
    """Create standard directory structure."""
    base = Path("/data")

    directories = [
        base / "cache",
        base / "logs",
        base / "config",
        base / "db",
        base / "temp"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
```

## Backup Integration

### Prepare for Backup

```python
import asyncio
from pathlib import Path

async def prepare_backup():
    """Prepare add-on for backup."""
    # Flush databases
    await flush_database()

    # Create backup metadata
    metadata = {
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat(),
        "files": []
    }

    # List important files
    data_dir = Path("/data")
    for file in data_dir.rglob("*"):
        if file.is_file():
            metadata["files"].append(str(file.relative_to(data_dir)))

    with open(data_dir / "backup_metadata.json", 'w') as f:
        json.dump(metadata, f)
```

### Restore from Backup

```python
async def restore_from_backup():
    """Restore add-on after backup restore."""
    metadata_file = Path("/data/backup_metadata.json")

    if not metadata_file.exists():
        return

    with open(metadata_file) as f:
        metadata = json.load(f)

    # Verify version compatibility
    if metadata["version"] != CURRENT_VERSION:
        await migrate_data(metadata["version"], CURRENT_VERSION)

    # Rebuild indexes, caches, etc.
    await rebuild_indexes()
```

## Cleanup and Maintenance

### Periodic Cleanup

```python
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

async def cleanup_old_files():
    """Remove files older than retention period."""
    retention_days = 30
    cutoff = datetime.now() - timedelta(days=retention_days)

    cache_dir = Path("/data/cache")

    for file in cache_dir.glob("*"):
        if file.is_file():
            # Check file modification time
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < cutoff:
                file.unlink()
                logger.info(f"Deleted old file: {file}")

async def cleanup_task():
    """Background cleanup task."""
    while True:
        await cleanup_old_files()
        await asyncio.sleep(86400)  # Run daily
```

### Disk Space Monitoring

```python
import shutil
from pathlib import Path

def check_disk_space(path: Path = Path("/data")) -> dict:
    """Check available disk space."""
    usage = shutil.disk_usage(path)

    return {
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent": (usage.used / usage.total) * 100
    }

def ensure_disk_space(required_mb: int = 100):
    """Ensure minimum free disk space."""
    space = check_disk_space()
    free_mb = space["free"] / (1024 * 1024)

    if free_mb < required_mb:
        raise RuntimeError(
            f"Insufficient disk space: {free_mb:.1f}MB free, "
            f"{required_mb}MB required"
        )
```

## Best Practices

1. **Use /data for add-on data** - Primary storage location
2. **Use /share for inter-add-on data** - Share files between add-ons
3. **Minimize /config access** - Only when necessary
4. **Implement atomic writes** - Prevent file corruption
5. **Rotate log files** - Prevent unbounded growth
6. **Clean up old files** - Implement retention policies
7. **Monitor disk space** - Alert when space is low
8. **Prepare for backups** - Flush data before backup
9. **Test restore** - Verify backup/restore works
10. **Document storage requirements** - In DOCS.md

## Migration Example

```python
from pathlib import Path
import json

class DataMigrator:
    """Handle data migrations between versions."""

    def __init__(self, data_dir: Path = Path("/data")):
        self.data_dir = data_dir
        self.version_file = data_dir / "version.txt"

    def get_current_version(self) -> str:
        """Get current data version."""
        if self.version_file.exists():
            return self.version_file.read_text().strip()
        return "0.0.0"

    def set_version(self, version: str):
        """Set current data version."""
        self.version_file.write_text(version)

    async def migrate(self, from_version: str, to_version: str):
        """Run migrations."""
        if from_version == "0.0.0" and to_version >= "0.1.0":
            await self.migrate_0_0_0_to_0_1_0()

        if from_version < "0.2.0" and to_version >= "0.2.0":
            await self.migrate_0_1_0_to_0_2_0()

        self.set_version(to_version)

    async def migrate_0_0_0_to_0_1_0(self):
        """Migrate from 0.0.0 to 0.1.0."""
        # Example: Rename old config file
        old_config = self.data_dir / "settings.json"
        new_config = self.data_dir / "config.json"

        if old_config.exists() and not new_config.exists():
            old_config.rename(new_config)

    async def migrate_0_1_0_to_0_2_0(self):
        """Migrate from 0.1.0 to 0.2.0."""
        # Example: Update database schema
        db = Database()
        with db.get_connection() as conn:
            conn.execute("ALTER TABLE events ADD COLUMN priority INTEGER DEFAULT 0")
            conn.commit()
```

## See Also

- `.agents/docs/patterns/addon-structure.md` - Add-on structure
- [Home Assistant Add-on Data](https://developers.home-assistant.io/docs/add-ons/configuration#add-on-advanced-options)
