"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.containers import Horizontal
from textual.widgets    import Header, Footer, ListView, ListItem, Label
from textual.binding    import Binding

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Local imports.
from ..data import load, Scale, Feelings

##############################################################################
class FeelingItem( ListItem ):
    """Base class for a feeling list item."""

    DEFAULT_CSS = """
    FeelingItem {
        height: 3;
        padding: 0 2 0 2;
    }

    FeelingItem > Label {
        width: 100%;
        height: 100%;
        color: black;
        padding: 1 0 0 1;
    }

    FeelingItem > Label.very_low {
        color: white;
        background: red;
    }

    FeelingItem > Label.low {
        background: #ff5f00;
    }

    FeelingItem > Label.neutral {
        background: #008700;
    }

    FeelingItem > Label.good {
        background: #00d700;
    }

    FeelingItem > Label.very_good {
        background: #00ff5f;
    }
    """

    def __init__( self, feelings: Feelings ) -> None:
        super().__init__()
        self._feelings = feelings

    @staticmethod
    def emoji( scale: Scale ) -> str:
        """Get an emoji to for a given scale.

        Args:
            scale: The scale to get the emoji for.

        Returns:
            An emoji name.
        """
        return {
            Scale.VERY_GOOD: ":beaming_face_with_smiling_eyes:",
            Scale.GOOD: ":grinning_face:",
            Scale.NEUTRAL: ":slightly_smiling_face:",
            Scale.LOW: ":slightly_frowning_face:",
            Scale.VERY_LOW: ":frowning:"
        }[ scale ]

##############################################################################
class Day( FeelingItem ):
    """A list item that's a day's feeling information."""

    def __init__( self, feelings: Feelings, year: str, month: str, day: str ) -> None:
        super().__init__( feelings )
        self._year        = year
        self._month       = month
        self._day         = day

    def compose( self ) -> ComposeResult:
        """Compose the child widgets."""
        scale = self._feelings.day_scale( self._year, self._month, self._day )
        yield Label(
            Text.from_markup( f"{self.emoji( scale )} {self._year}-{self._month}-{self._day}" ),
            classes=scale.name.lower()
        )

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
            Text.from_markup( f"{self.emoji( scale )} {self._year}-{self._month}" ),
            classes=scale.name.lower()
        )

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
            Text.from_markup( f"{self.emoji( scale )} {self._year}" ),
            classes=scale.name.lower()
        )

##############################################################################
# The main screen.
class Main( Screen ):
    """The main screen for the application."""

    BINDINGS = [
        Binding( "escape", "app.quit", "Quit" ),
    ]
    """The bindings for the main screen."""

    DEFAULT_CSS = """
    ListView {
        width: 1fr;
        background: $panel;
        border: round $primary;
    }
    """

    def compose( self ) -> ComposeResult:
        """Compose the screen.

        Returns:
            The composed widgets.
        """
        # pylint:disable=attribute-defined-outside-init
        yield Header()
        with Horizontal():
            with ListView( id="years" ) as years:
                self.years = years # pylint:disable=attribute-defined-outside-init
            with ListView( id="months" ) as months:
                self.months = months# pylint:disable=attribute-defined-outside-init
            with ListView( id="days" ) as days:
                self.days = days # pylint:disable=attribute-defined-outside-init
            with ListView( id="feelings" ) as feelings:
                self.feelings = feelings # pylint:disable=attribute-defined-outside-init
        yield Footer()

    async def on_mount( self ) -> None:
        """Populate the display once the DOM is mounted."""
        self.data = load() # pylint:disable=attribute-defined-outside-init
        for year in reversed( self.data.years() ):
            await self.years.append( Year( self.data, year ) )

    async def show_year( self, year: ListItem | None ) -> None:
        """Show the data for the given year.

        Args:
            year: The year to show the data for, or `None` if no year active.
        """
        await self.months.clear()
        if year is not None:
            assert isinstance( year, Year )
            for month in year.months:
                await self.months.append( month )

    async def show_month( self, month: ListItem | None ) -> None:
        """Show the data for the given month.

        Args:
            month: The month to show the data for, or `None` if no month active.
        """
        await self.days.clear()
        if month is not None:
            assert isinstance( month, Month )
            for day in month.days:
                await self.days.append( day )

    async def on_list_view_highlighted( self, event: ListView.Highlighted ) -> None:
        """Handle list view highlight events.

        Args:
            event: The ListView highlight event to handle.
        """
        if event.list_view.id == "years":
            await self.show_year( event.item )
        elif event.list_view.id == "months":
            await self.show_month( event.item )

### main.py ends here
