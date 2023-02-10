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
        """Compose the screen.

        Returns:
            The composed widgets.
        """
        yield Header()
        yield Tree( "Feelings" )
        yield Footer()

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

    @staticmethod
    def colour( scale: Scale ) -> str:
        """Get a colour for the label given a scale.

        Args:
            scale: The scale to get the colour for.

        Returns:
            A colour label for Rich.
        """
        return {
            Scale.VERY_GOOD: "[black on spring_green2]",
            Scale.GOOD: "[black on green3]",
            Scale.NEUTRAL: "[black on green]",
            Scale.LOW: "[black on orange_red1]",
            Scale.VERY_LOW: "[white on red]"
        }[ scale ]

    def on_mount( self ) -> None:
        """Populate the display once the DOM is mounted."""
        tree           = self.query_one( Tree )
        tree.show_root = False
        feelings       = load()
        for year in reversed( feelings.years() ):
            year_node = tree.root.add(
                f"{self.colour( feelings.year_scale( year ) )}{year} {self.emoji( feelings.year_scale( year ) )}",
                expand=True
            )
            for month in reversed( feelings.months( year ) ):
                month_node = year_node.add(
                    f"{self.colour( feelings.month_scale( year, month ) )}"
                    f"{month} {self.emoji( feelings.month_scale( year, month ) )}",
                    expand=True
                )
                for day in reversed( feelings.days( year, month ) ):
                    day_node = month_node.add(
                        f"{self.colour( feelings.day_scale( year, month, day ) )}"
                        f"{day} {self.emoji( feelings.day_scale( year, month, day ) )}"
                    )
                    for feeling in reversed( list( feelings.for_day( year, month, day ) ) ):
                        day_node.add_leaf( Emoji.replace(
                            f"{self.colour( feeling.feeling )}{self.emoji( feeling.feeling )} {feeling.description}"
                        ) )

### main.py ends here
