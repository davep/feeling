"""Provides a widget for presenting details of a particular year."""

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
from .month        import Month
from .feeling_item import FeelingItem

##############################################################################
class Year( FeelingItem ):
    """A list item that a year's feeling information."""

    def __init__( self, feelings: Feelings, year: str ) -> None:
        super().__init__( feelings )
        self._year = year

    @property
    def months( self ) -> list[ Month ]:
        """The list of recorded months in this year."""
        return [
            Month( self._feelings, self._year, month )
            for month in reversed( self._feelings.months( self._year ) )
        ]

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        scale = self._feelings.year_scale( self._year )
        yield Label(
            Text.from_markup(
                f"{self.emoji( scale )} {self._year} "
                f"{self._feelings.year_value( self._year ):6.2f}"
            ), classes=scale.name.lower()
        )

### year.py ends here
