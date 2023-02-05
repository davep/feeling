"""The command line interface for the app."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace, REMAINDER

##############################################################################
# Textual imports.
from textual import __version__ as __textual_version__

##############################################################################
# Local imports.
from . import __version__

##############################################################################
def get_args() -> tuple[ Namespace, list[ str ] ]:
    """Get the command line arguments.

    Returns:
        The parsed command line arguments and the remaining command line as a tuple.
    """
    parser = ArgumentParser(
        prog        = "feeling",
        description = "A simple terminal-based feelings tracker.",
        epilog      = f"v{__version__}"
    )

    # Add --version
    parser.add_argument(
        "-v", "--version",
        help    = "Show version information.",
        action  = "version",
        version = f"%(prog)s {__version__} (Textual v{__textual_version__})"
    )

    # We're going to use sub-parsers to create mood commands.
    subparsers = parser.add_subparsers(
        dest        = "rating",
        title       = "rating",
        description = "Recognised feeling ratings",
        help        = "The feeling ratings recognised by `feeling`"
    )

    # Add the commands for the highest-level feeling.
    subparsers.add_parser( "best", aliases=[
        "2", "excellent", "amazing", "fantastic"
    ] )

    # Add the commands for the high-level feeling.
    subparsers.add_parser( "good", aliases=[
        "1", "upbeat"
    ] )

    # Add the commands for the neutral-level feeling.
    subparsers.add_parser( "fine", aliases = [
        "0", "okay", "neutral", "level"
    ] )

    # Add the commands for the low-level feeling.
    subparsers.add_parser( "low", aliases=[
        "-1", "down", "meh"
    ] )

    # Add the commands for the lowest-level feeling.
    subparsers.add_parser( "lowest", aliases=[
        "-2", "rubbish", "worst"
    ] )

    # Return the arguments.
    return parser.parse_known_args()

##############################################################################
def save_feeling( rating: str, description: str ) -> None:
    """Save the feeling passed on the command line.

    Args:
        rating: The rating for the feeling.
        description: The description for the feeling.
    """
    # TODO
    print( f"TODO: Save that we feel {rating} because {description}" )

##############################################################################
def run() -> bool:
    """Attempt to run the command line interface for the app.

    Returns:
        `True` if the CLI handled things or `False` if we should go into the CHI.
    """

    # Look on the command line.
    args, description = get_args()

    # If we got given a rating, add it to the database...
    if args.rating is not None:
        save_feeling( args.rating, " ".join( description ) )
        return True

    # The CLI didn't handle things.
    return False

### cli.py ends here
