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
from .feelings import Feelings, Feeling

##############################################################################
def feelings_home() -> Path:
    """Get the path to the home feeling directory.

    Returns:
        The path to the directory where the data is held.

    Note:
        As a side-effect, this function will check if the directory that
        holds the file exists and, if it doesn't, it will create it.
    """
    ( home := xdg_data_home() / "feelings" ).mkdir( parents=True, exist_ok=True )
    return home

##############################################################################
def feeling_record( feeling: Feeling ) -> Path:
    """Return the path to the file for a particular feeling.

    Returns:
        The path to the file where the feeling is held.

    Note:
        As a side-effect, this function will check if the directory that
        holds the file exists and, if it doesn't, it will create it.
    """
    (
        day := feelings_home() / feeling.year_key / feeling.month_key / feeling.day_key
    ).mkdir( parents=True, exist_ok=True )
    return ( day / feeling.key.replace( ":", "-" ).replace( ".", "-" ) ).with_suffix( ".json" )

##############################################################################
def save( feelings: Feelings ) -> None:
    """Save the feelings.

    Args:
        feelings: The feelings data to save.
    """
    for feeling in feelings:
        feeling_record( feeling ).write_text( dumps( feeling.as_dict, indent=4 ) )

##############################################################################
def load() -> Feelings:
    """Load the feelings.

    Returns:
        A `Feelings` instance.
    """
    feelings = Feelings()
    for feeling in sorted( feelings_home().glob( "[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*.json" ) ):
        feelings.add( Feeling.from_dict( loads( feeling.read_text() ) ) )
    return feelings

##############################################################################
def make_test_data() -> None:
    """Make some test data.

    Note:
        Running this *will* pollute your real data store with
        randomly-generated test data. Don't call this unless that's what you
        want.
    """

    # I hate to import stuff outside of the top level, but this is just for
    # making test data so I don't need these generally.
    #
    # pylint:disable=import-outside-toplevel
    from random    import randint
    from datetime  import datetime, timedelta
    from .feelings import Scale

    start      = datetime( 2000, 1, 1, 0, 0, 0, 0 )
    end        = datetime.now()
    date_range = int( ( end - start ).total_seconds() )
    feelings   = Feelings()

    for _ in range( 50 ):
        feelings.add(
            Feeling(
                start + timedelta( seconds=randint( 0, date_range ) ),
                Scale( randint( -2, 2 ) ),
                "Random test feeling data"
            )
        )
    save( feelings )

### storage.py ends here
