import re

ENTITY_SUFFIXES = {"LLC", "LP", "LLP", "INC", "CORP", "TRUST", "LTD"}


def clean_name(name: str) -> str:
    return " ".join(re.sub(r"[^A-Za-z0-9&' -]", " ", name).upper().split())


def normalize_owner_name(name: str) -> str:
    cleaned = clean_name(name)
    if "," in name:
        last, remainder = (clean_name(part) for part in name.split(",", 1))
        return f"{last}, {remainder}".strip(", ")
    parts = cleaned.split()
    if len(parts) <= 1 or any(part in ENTITY_SUFFIXES for part in parts):
        return cleaned
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def owner_name_variations(name: str) -> list[str]:
    """Generate controlled variants; never use unconstrained fuzzy expansion."""
    normalized = normalize_owner_name(name)
    if "," not in normalized:
        return [normalized]
    last, given = (part.strip() for part in normalized.split(",", 1))
    given_parts = given.split()
    first = given_parts[0] if given_parts else ""
    middle = given_parts[1] if len(given_parts) > 1 else ""
    values = {
        normalized,
        f"{first} {middle} {last}".strip(),
        f"{first} {last}".strip(),
        f"{last}, {first}".strip(),
    }
    if middle:
        values.add(f"{last}, {first} {middle[0]}")
        values.add(f"{first} {middle[0]} {last}")
    return sorted(" ".join(value.split()) for value in values if value)


def comparable(value: str | None) -> str:
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())
