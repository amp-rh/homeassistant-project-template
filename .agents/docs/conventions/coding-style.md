# Coding Style

See @AGENTS.md for project-wide rules.

## Philosophy

Write **clean, self-documenting code**. The code itself should be clear enough that comments are unnecessary.

## Core Principles

### No Comments

Code should explain itself through:
- Descriptive names
- Small, focused functions
- Clear structure
- Type hints

```python
# BAD: Comment explaining unclear code
# Calculate the total price with tax
total = sum(i.p * i.q for i in items) * 1.08

# GOOD: Self-documenting code
total_price = calculate_subtotal(items) + calculate_tax(items)
```

### Object-Oriented with Dataclasses

Use Python dataclasses for data structures:

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    is_active: bool = True
    
@dataclass
class Order:
    user: User
    items: list[OrderItem]
    
    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)
```

### Small, Focused Classes

Each class should have a single responsibility:

```python
# BAD: God class doing everything
class UserManager:
    def create_user(self): ...
    def send_email(self): ...
    def validate_password(self): ...
    def generate_report(self): ...

# GOOD: Focused classes
@dataclass
class User:
    id: int
    email: str

class UserRepository:
    def create(self, user: User) -> User: ...
    def find_by_id(self, user_id: int) -> User | None: ...

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def register(self, email: str) -> User: ...
```

### Test-Driven Development (TDD)

Always write tests first:

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Clean up while tests pass

```python
# 1. Write test first
def test_user_full_name():
    user = User(first_name="John", last_name="Doe")
    assert user.full_name == "John Doe"

# 2. Write implementation
@dataclass
class User:
    first_name: str
    last_name: str
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

## Dataclass Patterns

### Immutable by Default

```python
@dataclass(frozen=True)
class Config:
    host: str
    port: int
```

### Factory Methods

```python
@dataclass
class User:
    id: int
    email: str
    created_at: datetime
    
    @classmethod
    def create(cls, email: str) -> "User":
        return cls(
            id=generate_id(),
            email=email,
            created_at=datetime.now()
        )
```

### Composition Over Inheritance

```python
@dataclass
class Address:
    street: str
    city: str
    country: str

@dataclass
class Customer:
    name: str
    billing_address: Address
    shipping_address: Address
```

## Function Guidelines

### Small Functions

Functions should do one thing:

```python
# BAD: Function doing multiple things
def process_order(order):
    validate_items(order.items)
    total = sum(i.price for i in order.items)
    tax = total * 0.08
    send_confirmation_email(order.user, total + tax)
    return total + tax

# GOOD: Single responsibility
def calculate_order_total(order: Order) -> float:
    return order.subtotal + order.tax

def process_order(order: Order) -> float:
    total = calculate_order_total(order)
    send_confirmation(order, total)
    return total
```

### Descriptive Names

Names should reveal intent:

```python
# BAD
def proc(d):
    return d["a"] + d["b"]

# GOOD
def calculate_total_price(order_data: dict) -> float:
    return order_data["subtotal"] + order_data["tax"]
```

## Rules Summary

- MUST NOT include comments (code should self-document)
- MUST use dataclasses for data structures
- MUST keep classes small and focused (single responsibility)
- MUST write tests before implementation (TDD)
- MUST use descriptive names
- SHOULD prefer composition over inheritance
- SHOULD use frozen dataclasses for immutable data
- SHOULD keep functions under 10 lines

## Related

- @.agents/docs/conventions/naming.md - Naming conventions
- @.agents/docs/patterns/typing.md - Type hints
- @.agents/docs/workflows/testing.md - Testing workflow


