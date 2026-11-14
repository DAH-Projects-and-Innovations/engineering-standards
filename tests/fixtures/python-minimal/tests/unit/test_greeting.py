import pytest

from dah_fixture import greet
from dah_fixture.greeting import Greeting, UnsupportedLanguageError


def test_greet_defaults_to_english() -> None:
    # Arrange
    name = "Awa"

    # Act
    result = greet(name)

    # Assert
    assert result == "Hello, Awa!"


@pytest.mark.parametrize(
    ("language", "expected"),
    [("fr", "Bonjour, Kofi!"), ("sw", "Habari, Kofi!"), ("wo", "Nanga def, Kofi!")],
)
def test_greet_uses_requested_language(language: str, expected: str) -> None:
    assert greet("Kofi", language) == expected


def test_greet_strips_surrounding_spaces() -> None:
    assert greet("  Amina  ", "fr") == "Bonjour, Amina!"


def test_render_raises_for_unsupported_language() -> None:
    greeting = Greeting(language="xx", name="Awa")

    with pytest.raises(UnsupportedLanguageError, match="Unsupported language: 'xx'"):
        greeting.render()
