# Python Circular Imports: Why They Happen and How to Fix Them

> Source: https://realpython.com/python-circular-imports/
> Collected: 2026-11-07
> Published: 2026-10-27

# Python Circular Imports: Why They Happen and How to Fix Them

by Srujana Maddula Updated Oct 27, 2026 Reading time estimate 18m

## Table of Contents

- In Short: A Python Circular Import Is a Loop Between Modules
- Why Python Circular Imports Fail
  - A Python Circular Import Example
  - Tracing the Import Sequence
- Step-by-Step Explanation: How to Fix Circular Imports
  - Step 1: Remove the Runtime Dependency
  - Step 2: Guard the Type-Only Import
- Workarounds to Escape a Circular Dependency
  - Defer Imports to Inside Functions
  - Move Imports to the Bottom
  - Change How You Import the Module
- Conclusion
- Frequently Asked Questions

## Introduction

A Python circular import happens when two modules import each other and one of them isn’t finished loading yet. Python reports it as an `ImportError` or an `AttributeError`, usually with a message about a partially initialized module.

**By the end of this tutorial, you’ll understand that:**

- A **Python circular import** happens when two modules depend on each other and one asks for a name before the other has finished loading.
- The reliable fix is to **remove the dependency** so that imports flow in one direction.
- `ImportError` and `AttributeError` signal the same cycle, and which one you get depends on the **form** of the import statement you used.
- Moving an import **inside the function** that needs it is the only workaround that survives any import order.
- A type-only import still needs a **`TYPE_CHECKING` guard**, even on Python 3\.14, where annotations are evaluated lazily.

## In Short: A Python Circular Import Is a Loop Between Modules

A circular import happens when two or more modules import each other, directly or through a chain. The cycle fails only when one module asks for a name that the other module hasn’t defined yet, because Python is still loading that module. You’ll see this as an `ImportError` or an `AttributeError`.

The reliable fix is to restructure your code so imports flow in one direction, toward the module that could exist without the other. Guard imports used only for type hints with `TYPE_CHECKING`. If you can’t restructure yet, move the import inside the function that needs it.

## Why Python Circular Imports Fail

Whenever Python imports a module, it first creates an entry for that module in `sys.modules`. It then starts executing the file from top to bottom.

Think of `sys.modules` as Python’s cache of imported modules. If another import requests a module that’s already in the cache, Python reuses the existing module object instead of importing it again.

The key is that Python adds the module to `sys.modules` before it finishes executing the file. That means the module can exist in a partially initialized state. Some functions, classes, and variables may not exist yet because Python hasn’t reached those lines of code. If another module tries to import one of those objects before it’s defined, Python raises an `ImportError` or `AttributeError`.

### Example: E-commerce Shop Package

Project structure:

```
shop_project/
│
├── shop/
│   ├── __init__.py
│   ├── order.py
│   └── product.py
│
└── main.py
```

**shop/order.py:**
```python
from shop.product import Product

SHIPPING_FEE = 4.99

class Order:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity
        self.extras: list[Product] = []

    def add_shipping(self) -> None:
        self.extras.append(Product("Shipping", SHIPPING_FEE))

    def get_total(self) -> float:
        subtotal = self.product.price * self.quantity
        return subtotal + sum(extra.price for extra in self.extras)
```

**shop/product.py:**
```python
from shop.order import Order

class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def order(self, quantity: int) -> Order:
        return Order(self, quantity)

    def is_in_order(self, order: Order) -> bool:
        return order.product.name == self.name
```

**main.py:**
```python
from shop.product import Product

laptop = Product("Laptop", 1000.0)
order = laptop.order(1)
order.add_shipping()

print(order.get_total())
```

Running `main.py` produces:

```
$ python main.py
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from shop.product import Product
  File "shop/product.py", line 1, in <module>
    from shop.order import Order
  File "shop/order.py", line 1, in <module>
    from shop.product import Product
ImportError: cannot import name 'Product' from partially initialized module 'shop.product'
```

### Tracing the Import Sequence

1. `main.py` runs `from shop.product import Product`.
2. Python creates `shop.product`, adds it to `sys.modules`, starts executing `product.py`.
3. `product.py` runs `from shop.order import Order`. `shop.order` isn’t loaded yet, so Python switches to loading `order.py`.
4. Python creates `shop.order`, adds it to `sys.modules`, starts executing `order.py`.
5. `order.py` runs `from shop.product import Product`.
6. Python finds `shop.product` in `sys.modules`, but it’s still being initialized and `Product` isn’t available yet, so Python raises `ImportError`.

Python adds `shop.product` to `sys.modules` before defining any names in that module. The module object exists, so Python won’t start loading it again, but the names inside don’t exist yet.

## How to Fix Circular Imports

The best way to fix circular imports is to remove the circular dependency by restructuring the code or design.

### Step 1: Remove the Runtime Dependency

An order needs a product, but a product can exist without an order. The dependency should flow `order.py` → `product.py`, not the other way around. So `product.py` shouldn’t import `Order` at runtime.

Remove `Product.order()` and create `Order` directly in `main.py`:

**shop/product.py (fixed):**
```python
class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def is_in_order(self, order: Order) -> bool:
        return order.product.name == self.name
```

**main.py (fixed):**
```python
from shop.order import Order
from shop.product import Product

laptop = Product("Laptop", 1000.0)
order = Order(laptop, 2)
order.add_shipping()

print(order.get_total())
```

On Python 3.13 and earlier, this raises `NameError: name 'Order' is not defined` because older versions evaluate annotations right away. On Python 3.14, the code runs because Python evaluates annotations lazily.

### Step 2: Guard the Type-Only Import

Python’s `TYPE_CHECKING` constant lets you import modules for static type checking without performing those imports at runtime.

**shop/product.py (final fix):**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shop.order import Order

class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def is_in_order(self, order: "Order") -> bool:
        return order.product.name == self.name
```

The quotes around `"Order"` make the annotation a string, so Python 3.13 and earlier don’t try to look up `Order` at runtime. On Python 3.14, you can leave them out.

Now the runtime cycle is gone:

```
$ python main.py
2004.99
```

## Workarounds to Escape a Circular Dependency

Sometimes restructuring isn’t easy. Here are escape hatches.

### Defer Imports to Inside Functions

Move the import inside the function that needs it:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shop.order import Order

class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def order(self, quantity: int) -> "Order":
        from shop.order import Order
        return Order(self, quantity)

    def is_in_order(self, order: "Order") -> bool:
        return order.product.name == self.name
```

This works no matter which module your program imports first.

### Move Imports to the Bottom

Move the import to the bottom of the file:

```python
class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def order(self, quantity: int) -> "Order":
        return Order(self, quantity)

    def is_in_order(self, order: "Order") -> bool:
        return order.product.name == self.name

from shop.order import Order
```

This goes against PEP 8 and linters flag it as `E402` (“module level import not at top of file”). It also only works if `main.py` imports `shop.product` first.

### Change How You Import the Module

`from shop.product import Product` and `from shop import product` behave differently during circular imports:

- `from shop.product import Product` looks for `Product` immediately → `ImportError` if not yet defined
- `from shop import product` defers the lookup → `AttributeError` only if code accesses `product.Product` before loading finishes

**shop/order.py (fixed):**
```python
from typing import TYPE_CHECKING

from shop import product

if TYPE_CHECKING:
    from shop.product import Product

SHIPPING_FEE = 4.99

class Order:
    def __init__(self, product: "Product", quantity: int) -> None:
        self.product = product
        self.quantity = quantity
        self.extras: list["Product"] = []

    def add_shipping(self) -> None:
        self.extras.append(product.Product("Shipping", SHIPPING_FEE))

    def get_total(self) -> float:
        subtotal = self.product.price * self.quantity
        return subtotal + sum(extra.price for extra in self.extras)
```

Don’t access `Product` at the module level. Leave access inside functions where both modules have finished loading.

## Conclusion

Circular imports are often a sign that two modules depend on each other in a way that makes them difficult to load and maintain.

**The reliable fix:** Restructure so imports flow in one direction. Use `TYPE_CHECKING` for type-only imports so Python never executes them at runtime.

**Workarounds:** Moving an import inside the function that needs it is the sturdiest workaround. Moving imports to the bottom or changing import form depends on import order and should be treated as stopgaps.

**Note:** Python 3.15 adds an explicit `lazy` import form in PEP 810. It changes when an import is resolved but doesn’t change your dependency graph — a true cycle still needs restructuring.

## FAQ

**What causes a circular import?**
Two or more modules that import each other, directly or through a chain, form a cycle. The error appears when one asks for a name the other hasn’t defined yet.

**How do you fix a circular import?**
Remove the circular dependency so imports flow in one direction. When restructuring isn’t an option, move the import inside the function that needs it.

**Why `AttributeError` instead of `ImportError`?**
The exception type depends on the import form. `from shop.product import Product` fails with `ImportError` immediately. `from shop import product` defers the lookup, giving `AttributeError` only when accessing `product.Product` too early.

**Is putting imports at the bottom bad practice?**
It works but goes against PEP 8 (flagged as `E402`). It also relies on import order, so it breaks if modules are imported in the opposite order.

**Does `TYPE_CHECKING` remove a circular import?**
It removes the runtime import so the cycle no longer breaks your program, and type checkers can still resolve the annotation. It’s a targeted fix, not a restructuring.