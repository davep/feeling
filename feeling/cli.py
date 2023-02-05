"""The command line interface for the app."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace

##############################################################################
# Textual imports.
from textual import __version__ as __textual_version__

##############################################################################
# Local imports.
from .     import __version__
from .data import scale_names

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

    # Add the optional rating parameter.
    parser.add_argument(
        "rating",
        nargs   = "?",
        choices = scale_names(),
        help    = "A description of the rating of the feeling"
    )

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
