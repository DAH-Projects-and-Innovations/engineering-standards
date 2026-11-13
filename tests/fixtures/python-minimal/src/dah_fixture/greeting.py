"""Build greeting messages in the languages supported by the fixture."""

from dataclasses import dataclass
from typing import Final

_GREETINGS: Final[dict[str, str]] = {
    "en": "Hello",
    "fr": "Bonjour",
    "sw": "Habari",
    "wo": "Nanga def",
}


class UnsupportedLanguageError(ValueError):
    """Raised when a greeting is requested in a language that is not supported."""

    def __init__(self, language: str) -> None:
        """Create the error for ``language``."""
        super().__init__(f"Unsupported language: {language!r}")
        self.language = language


@dataclass(frozen=True)
class Greeting:
    """A greeting addressed to one person.

    Attributes:
        language: ISO 639-1 code of the language, for example ``"fr"``.
        name: Name of the person greeted.
    """

    language: str
    name: str

    def render(self) -> str:
        """Return the greeting as text.

        Raises:
            UnsupportedLanguageError: If the language is not supported.
        """
        try:
            word = _GREETINGS[self.language]
        except KeyError as error:
            raise UnsupportedLanguageError(self.language) from error
        return f"{word}, {self.name}!"


def greet(name: str, language: str = "en") -> str:
    """Return a greeting for ``name`` in ``language``.

    Args:
        name: Name of the person greeted. Surrounding spaces are removed.
        language: ISO 639-1 code of the language.

    Returns:
        The greeting, for example ``"Bonjour, Awa!"``.
    """
    return Greeting(language=language, name=name.strip()).render()
