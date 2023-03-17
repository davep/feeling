"""Provides a widget for presenting details of a particular day."""

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
from .feeling      import Feeling
from .feeling_item import FeelingItem

##############################################################################
class Day( FeelingItem ):
    """A list item that's a day's feeling information."""

    def __init__( self, feelings: Feelings, year: str, month: str, day: str ) -> None:
        super().__init__( feelings )
        self._year        = year
        self._month       = month
        self._day         = day

    @property
    def feelings( self ) -> list[ Feeling ]:
        """The feelings recorded for this day."""
        return [
            Feeling( self._feelings, feeling.key )
            for feeling in self._feelings.for_day( self._year, self._month, self._day )
        ]

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        scale = self._feelings.day_scale( self._year, self._month, self._day )
        yield Label(
            Text.from_markup(
                f"{self.emoji( scale )} {self._year}-{self._month}-{self._day} "
                f"{self._feelings.day_value( self._year, self._month, self._day ):6.2f}"
            ), classes=scale.name.lower()
        )

### day.py ends here
