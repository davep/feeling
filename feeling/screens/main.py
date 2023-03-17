"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.containers import Horizontal
from textual.widgets    import Header, Footer, ListView, ListItem
from textual.binding    import Binding

##############################################################################
# Local imports.
from ..data    import load
from ..widgets import Year, Month, Day

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
                self.years = years
            with ListView( id="months" ) as months:
                self.months = months
            with ListView( id="days" ) as days:
                self.days = days
            with ListView( id="feelings" ) as feelings:
                self.feelings = feelings
        yield Footer()

    async def on_mount( self ) -> None:
        """Populate the display once the DOM is mounted."""
        self.data = load() # pylint:disable=attribute-defined-outside-init
        for year in reversed( self.data.years() ):
            await self.years.append( Year( self.data, year ) )
        self.years.focus()

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

    async def show_day( self, day: ListItem | None ) -> None:
        """Show the data for the given day.

        Args:
            day: The day to show the data for, or `None` if no day active.
        """
        await self.feelings.clear()
        if day is not None:
            assert isinstance( day, Day )
            for feeling in day.feelings:
                await self.feelings.append( feeling )

    async def on_list_view_highlighted( self, event: ListView.Highlighted ) -> None:
        """Handle list view highlight events.

        Args:
            event: The ListView highlight event to handle.
        """
        if event.list_view.id is not None:
            try:
                await {
                    "years": self.show_year,
                    "months": self.show_month,
                    "days": self.show_day
                }[ event.list_view.id ]( event.item )
            except KeyError:
                pass

### main.py ends here
