class FestError(Exception):
    """Base class for every problem this package reports."""


class InvalidRegistration(FestError):
    """One line is damaged or invalid (raised in validator, handled in main.run)."""


class DuplicateRegistration(InvalidRegistration):
    """The register number was already accepted."""
