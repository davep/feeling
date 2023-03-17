"""Provides a widget for presenting details of a particular month."""

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
from .day          import Day

##############################################################################
class Month( FeelingItem ):
    """A list item that's a month's feeling information."""

    def __init__( self, feelings: Feelings, year: str, month: str ) -> None:
        super().__init__( feelings )
        self._year  = year
        self._month = month

    @property
    def days( self ) -> list[ Day ]:
        """The list of recorded days in this month."""
        return [
            Day( self._feelings, self._year, self._month, day )
            for day in reversed( self._feelings.days( self._year, self._month ) )
        ]

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        scale = self._feelings.month_scale( self._year, self._month )
        yield Label(
            Text.from_markup(
                f"{self.emoji( scale )} {self._year}-{self._month} "
                f"{self._feelings.month_value( self._year, self._month ):6.2f}"
            ), classes=scale.name.lower()
        )

### month.py ends here
