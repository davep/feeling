"""The CHUI entry point."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .        import __version__
from .screens import Main

##############################################################################
class Feeling( App[ None ] ):
    """The main app class."""

    TITLE = "Feeling"
    """The title of the application."""

    SUB_TITLE  = f"The simple terminal feeling tracker - v{__version__}"
    """The subtitle of the application."""

    SCREENS = { "main": Main }
    """The screens for the application."""

    def on_mount( self ) -> None:
        """Initialise the application on startup."""
        self.push_screen( "main" )

##############################################################################
def run() -> None:
    """Run the application."""
    Feeling().run()

### chui.py ends here
