"""Domain errors raised by Familiar."""


class FamiliarError(Exception):
    """Base error for user-facing Familiar failures."""


class CharacterNotFoundError(FamiliarError):
    """Raised when a character pack cannot be found."""


class CharacterDefinitionError(FamiliarError):
    """Raised when a character pack definition is invalid."""


class MoodNotFoundError(FamiliarError):
    """Raised when a mood cannot be resolved."""
