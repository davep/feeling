"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer
from textual.binding import Binding

##############################################################################
# The main screen.
class Main( Screen ):
    """The main screen for the application."""

    BINDINGS = [
        Binding( "escape", "app.quit", "Quit" ),
    ]
    """The bindings for the main screen."""

    def compose( self ) -> ComposeResult:
        """Compose the screen."""
        yield Header()
        # TODO
        yield Footer()

### main.py ends here
