"""Defines the code for loading/holding/saving the feeling data."""

##############################################################################
# Python imports.
from __future__  import annotations
from typing      import cast, TypeAlias
from datetime    import datetime
from collections import defaultdict
from dataclasses import dataclass, field
from enum        import Enum

##############################################################################
class Scale( Enum ):
    """The scale of feelings."""

    VERY_LOW  = -2
    LOW       = -1
    NEUTRAL   = 0
    GOOD      = 1
    VERY_GOOD = 2

##############################################################################
SCALE_NAMES = {
    Scale.VERY_LOW: { "-2", "rubbish", "worst", "lowest", "horrible" },
    Scale.LOW: { "-1", "low", "down", "meh" },
    Scale.NEUTRAL: { "0", "okay", "flat", "neutral", "level" },
    Scale.GOOD: { "1", "good", "upbeat", "fine" },
    Scale.VERY_GOOD: { "2", "excellent", "great", "amazing", "wonderful", "elated" }
}
"""Scale to alternate name mappings."""

##############################################################################
def scale_names() -> set[ str ]:
    """All of the names that describe the feeling scales.

    Returns:
        A set of all of the names that describe the feeling scales.
    """
    return set.union( *SCALE_NAMES.values() )

##############################################################################
def scale_from_name( name: str ) -> Scale:
    """Get a feeling scale from a given name.

    Args:
        name: The name of a feeling scale.

    Returns:
        The related feeling scale.

    Raises:
        TypeError: If the name is not recognised.
    """
    for scale, names in SCALE_NAMES.items():
        if name in names:
            return scale
    raise ValueError( f"'{name}' is not a recognised feeling scale name" )

##############################################################################
FeelingDict: TypeAlias = dict[ str, int | str ]

##############################################################################
@dataclass
class Feeling:
    """Class to hold an individual feeling."""

    recorded: datetime = field( default_factory=datetime.now )
    """When the feeling was recorded."""

    feeling: Scale = Scale.NEUTRAL
    """The value for the feeling."""

    description: str = ""
    """A description of the feeling."""

    @property
    def year_key( self ) -> str:
        """The key for the year under which to store this feeling."""
        return self.recorded.strftime( "%Y" )

    @property
    def month_key( self ) -> str:
        """The key for the month under which to store this feeling."""
        return self.recorded.strftime( "%m" )

    @property
    def day_key( self ) -> str:
        """The key for the day under which to store this feeling."""
        return self.recorded.strftime( "%d" )

    @property
    def key( self ) -> str:
        """The unique key under which to store this feeling."""
        return self.recorded.isoformat()

    @property
    def as_dict( self ) -> FeelingDict:
        """The feeling as a JSON-friendly dictionary."""
        return {
            "recorded":    self.recorded.isoformat(),
            "feeling":     self.feeling.value,
            "description": self.description
        }

    @classmethod
    def from_dict( cls, data: FeelingDict ) -> "Feeling":
        """Create a feeling entry from the given dictionary.

        Args:
            data: A dictionary containing the feeling data.

        Returns:
            A new `Feeling` object.
        """
        return cls(
            datetime.fromisoformat( cast( str, data[ "recorded" ] ) ),
            Scale( cast( int, data[ "feeling" ] ) ),
            cast( str, data[ "description" ] )
        )

##############################################################################
FeelingsDict: TypeAlias = dict[ str, FeelingDict ]

##############################################################################
class Feelings:
    """Class to hold the feeling data."""

    def __init__( self ) -> None:
        """Initialise the class."""
        self._history: defaultdict[ str, defaultdict[ str, defaultdict[ str, dict[ str, Feeling ] ] ] ] = defaultdict(
            lambda: defaultdict( lambda: defaultdict( dict ) )
        )

    def record( self,
                feeling: Scale | int=Scale.NEUTRAL,
                recorded: datetime | None=None,
                description: str="" ) -> Feeling:
        """Record a feeling.

        Args:
            feeling: The rating of the feeling.
            recorded: Optional time at which the feeling was recorded.
            description: A description to associate with the feeling.

        Raises:
            ValueError: If an integer feeling is out of range.

        Returns:
            The newly-created feeling entry.
        """
        entry = Feeling(
            datetime.now() if recorded is None else recorded,
            Scale( feeling ),
            description
        )
        self._history[ entry.year_key ][ entry.month_key ][ entry.day_key ][ entry.key ] = entry
        return entry

    @property
    def as_dict( self ) -> FeelingsDict:
        """The feelings as a JSON-friendly dictionary."""
        flat_dict: FeelingsDict = {}
        for year in self._history.values():
            for month in year.values():
                for day in month.values():
                    for feeling in day.values():
                        flat_dict[ feeling.key ] = feeling.as_dict
        return flat_dict

    def from_dict( self, data: FeelingsDict ) -> "Feelings":
        """Reset the data to that given in the dictionary.

        Args:
            data: A dictionary containing the feelings data.

        Returns:
            self
        """
        for value in data.values():
            feeling = Feeling.from_dict( value )
            self._history[ feeling.year_key ][ feeling.month_key ][ feeling.day_key ][ feeling.key ] = feeling
        return self

### feelings.py ends here
