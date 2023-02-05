"""Code that handles the saving/loading of the feeling data."""

##############################################################################
# Python imports.
from pathlib import Path
from json    import dumps, loads

##############################################################################
# XDG imports.
from xdg import xdg_data_home

##############################################################################
# Local imports.
from .feelings import Feelings

##############################################################################
def feelings_file() -> Path:
    """Get the path to the feeling data file.

    Returns:
        The path to the file where the data is held.

    Note:
        As a side-effect, this function will check if the directory that
        holds the file exists and, if it doesn't, it will create it.
    """
    ( feelings_home := xdg_data_home() / "feelings" ).mkdir( parents=True, exist_ok=True )
    return feelings_home / "feelings.json"

##############################################################################
def save( feelings: Feelings ) -> None:
    """Save the feelings.

    Args:
        feelings: The feelings data to save.
    """
    feelings_file().write_text( dumps( feelings.as_dict, indent=4 ) )

##############################################################################
def load() -> Feelings:
    """Load the feelings.

    Returns:
        A `Feelings` instance.
    """
    return Feelings().from_dict(
        loads( feelings_file().read_text() )
    ) if feelings_file().exists() else Feelings()

### storage.py ends here
