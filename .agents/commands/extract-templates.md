# /extract-templates

Extract reusable templates from the codebase.

## Purpose

Identify and extract common patterns, boilerplate, or reusable code structures from the project and save them as templates in `.agents/templates/`.

## Steps

1. **Analyze codebase**: Scan for repeated patterns, common structures, or boilerplate code
2. **Identify candidates**: Look for:
   - Class patterns (services, models, handlers)
   - Function signatures with common patterns
   - Configuration file structures
   - Test file structures
   - Documentation patterns
3. **Extract templates**: Create template files with placeholders
4. **Document templates**: Add description and usage instructions to each template
5. **Update index**: Add new templates to `.agents/templates/` listing

## Template Format

Templates should use clear placeholders:

```python
# Template: <template-name>
# Description: <what this template is for>
# Usage: <when to use this template>

class <ClassName>:
    """<Description>."""
    
    def __init__(self, <params>) -> None:
        self.<attr> = <value>
    
    def <method_name>(self) -> <return_type>:
        """<Method description>."""
        pass
```

## What to Extract

### Code Templates
- Service class pattern
- Model/dataclass pattern
- Exception class pattern
- Test class/function pattern
- Fixture pattern

### File Templates
- New module with standard imports
- Test file structure
- Configuration file patterns

### Documentation Templates
- Docstring formats
- AGENTS.md structure
- ADR format

## Output Location

Save templates to `.agents/templates/` with descriptive names:
- `service-class.py.template`
- `test-module.py.template`
- `model-dataclass.py.template`
- `agents-md.md.template`

## Rules

- MUST use clear placeholder syntax (`<placeholder_name>`)
- MUST include description and usage in each template
- MUST NOT extract project-specific logic (only patterns)
- SHOULD group related templates

## Related

- @.agents/templates/ - Where templates are stored
- @.agents/docs/patterns/ - Documented patterns
- @.agents/docs/conventions/ - Coding conventions


