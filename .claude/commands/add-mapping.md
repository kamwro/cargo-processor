Guide the user through adding a new field alias mapping to the normalizer.

Steps:
1. Ask: which entity does the new field belong to — `item_types` (the `types` array) or `items`?
2. Ask: what is the canonical output field name (e.g., `unitWeightKg`)?
3. Ask: what input alias(es) should also be accepted (e.g., `w`, `weight`)?
4. Ask: what is the default value when all aliases are missing (e.g., `0.0`, `"Unknown"`, `None`)?
5. Ask: what is the Python type of the field (`str`, `float`, `int`, or optional like `float | None`)?

Then make the changes:
- In `app/services/normalizer.py`: add `_get(obj, "<canonical>", "<alias>", default=<default>, cast=<type>)` to the appropriate dict inside `normalize_raw()`. For optional fields (`default=None`), use the inline ternary pattern instead: `float(t["<field>"]) if t.get("<field>") is not None else None`.
- In `app/graphql/types.py`: add the field to the corresponding `@strawberry.type` class (`ItemType` or `Item`) and the corresponding `@strawberry.input` class (`ItemTypeIn` or `ItemIn`).
- In `tests/test_services_normalizer.py`: add a test that passes the alias key in input and asserts the canonical name appears in output with correct value.

Finally run `python scripts/test.py && python scripts/typecheck.py` and confirm both pass.
