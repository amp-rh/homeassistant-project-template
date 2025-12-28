# Import Organization

See @AGENTS.md for project-wide rules.

## Overview

Import organization follows PEP 8 with Ruff enforcement.

## Order

Imports are organized in groups, separated by blank lines:

1. **Standard library** - `import os`, `from typing import ...`
2. **Third-party** - `import pytest`, `from pydantic import ...`
3. **Local/project** - `from src.models import ...`

## Example

```python
import logging
import os
from collections.abc import Iterator
from typing import TypeAlias

import pytest
from pydantic import BaseModel

from src.models import User
from src.services import UserService
```

## Rules

- MUST organize imports in the standard order
- MUST use absolute imports for project modules
- SHOULD use `from` imports for specific items
- SHOULD NOT use wildcard imports (`from module import *`)

## Ruff Handling

Ruff automatically sorts imports. Run:

```bash
uv run ruff check --fix .
```

See @.agents/docs/tooling/ruff.md for more details.

## Related

- @.agents/docs/tooling/ruff.md - Automatic import sorting
- @.agents/docs/conventions/naming.md - Module naming


