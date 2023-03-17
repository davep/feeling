"""Provides the widget that holds an individual feeling."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.widgets import Label

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Local imports.
from ..data        import Feelings
from .feeling_item import FeelingItem

##############################################################################
class Feeling( FeelingItem ):
    """A list item that's an individual feeling record."""

    DEFAULT_CSS = """
    Feeling {
        height: auto;
        border: hkey black;
    }

    Feeling > Label {
        height: auto;
        padding: 1;
    }
    """

    def __init__( self, feelings: Feelings, key: str ) -> None:
        super().__init__( feelings )
        self._key = key

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        feeling = self._feelings[ self._key ]
        yield Label(
            Text.assemble(
                Text.from_markup( self.emoji( feeling.feeling ) ),
                f" {feeling.recorded:%H:%M:%S}",
                *(
                    [ f"\n\n{feeling.description}" ]
                    if feeling.description else []
                )
            ),
            classes=feeling.feeling.name.lower()
        )

### feeling.py ends here
