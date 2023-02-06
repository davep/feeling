"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer, Tree
from textual.binding import Binding

##############################################################################
# Rich imports.
from rich.emoji import Emoji

##############################################################################
# Local imports.
from ..data import load, Scale

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
        yield Tree( "Feelings" )
        yield Footer()

    @staticmethod
    def emoji( scale: Scale ) -> str:
        """Get an emoji to for a given scale."""
        return {
            Scale.VERY_GOOD: ":beaming_face_with_smiling_eyes:",
            Scale.GOOD: ":grinning_face:",
            Scale.NEUTRAL: ":slightly_smiling_face:",
            Scale.LOW: ":slightly_frowning_face:",
            Scale.VERY_LOW: ":frowning:"
        }[ scale ]

    def on_mount( self ) -> None:
        """Populate the display once the DOM is mounted."""
        tree           = self.query_one( Tree )
        tree.show_root = False
        feelings       = load()
        for year in reversed( feelings.years() ):
            year_node = tree.root.add( year, expand=True )
            for month in reversed( feelings.months( year ) ):
                month_node = year_node.add( month, expand=True )
                for day in reversed( feelings.days( year, month ) ):
                    day_node = month_node.add( day, expand=True )
                    for feeling in reversed( feelings.for_day( year, month, day ) ):
                        day_node.add_leaf( Emoji.replace( self.emoji( feeling.feeling ) ) )

### main.py ends here
