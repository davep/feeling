"""Defines the code for loading/holding/saving the feeling data."""

##############################################################################
# Python imports.
from __future__  import annotations
from typing      import cast, TypeAlias, Iterator, Iterable
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
    Scale.VERY_LOW: {
        str( Scale.VERY_LOW.value ),
        "rubbish", "worst", "lowest", "horrible"
    },
    Scale.LOW: {
        str( Scale.LOW.value ),
        "low", "down", "meh", "blah", "downbeat", "negative"
    },
    Scale.NEUTRAL: {
        str( Scale.NEUTRAL.value ),
        "ok", "okay", "flat", "neutral", "level"
    },
    Scale.GOOD: {
        str( Scale.GOOD.value ),
        "good", "upbeat", "fine", "better", "positive"
    },
    Scale.VERY_GOOD: {
        str( Scale.VERY_GOOD.value ),
        "excellent", "great", "amazing", "wonderful", "elated",
        "fantastic", "awesome"
    }
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

    def years( self ) -> tuple[ str, ... ]:
        """Years where feelings have been recorded.

        Returns:
            All of the years that have been recorded.
        """
        return tuple( self._history.keys() )

    def months( self, year: str ) -> tuple[ str, ... ]:
        """Months in a year where feelings have been recorded.

        Args:
            year: The year to get the recorded months for.

        Returns:
            The months recorded for that year.
        """
        return tuple( self._history[ year ].keys() )

    def days( self, year: str, month: str ) -> tuple[ str, ... ]:
        """Days in a month in a year where feelings have been recorded.

        Args:
            year: The year of the month to get the recorded days for.
            month: The month to get the record days for.

        Returns:
            The recorded days for that month in that year.
        """
        return tuple( self._history[ year ][ month ].keys() )

    def for_day( self, year: str, month: str, day: str ) -> Iterator[ Feeling ]:
        """The feelings for a given day.

        Args:
            year: The year of the month of the day to get the feelings for.
            month: The month of the day to get the feelings for.
            day: The day to get the feelings for.

        Yields:
            The feelings for that day.
        """
        yield from self._history[ year ][ month ][ day ].values()

    def for_month( self, year: str, month: str ) -> Iterator[ Feeling ]:
        """The feelings for a given month.

        Args:
            year: The year of the month of the day to get the feelings for.
            month: The month to get the feelings for.

        Yields:
            The feelings for that month.
        """
        for day in self.days( year, month ):
            yield from self.for_day( year, month, day )

    def for_year( self, year: str ) -> Iterator[ Feeling ]:
        """The feelings for a given year.

        Args:
            year: The year to get the feelings for.

        Yields:
            The feelings for that year.
        """
        for month in self.months( year ):
            for day in self.days( year, month ):
                yield from self.for_day( year, month, day )

    def _overall_value( self, feelings: Iterable[ Feeling ] ) -> float:
        """Calculate the overall feeling value for a collection of feelings.

        Returns:
           The overall value of feeling for all of the given feelings.
        """
        if ( values := [ feeling.feeling.value for feeling in feelings ] ):
            return sum( values ) / len( values )
        return 0.0

    def _overall_scale( self, feelings: Iterable[ Feeling ] ) -> Scale:
        """Calculate the overall feeling scale for a collection of feelings.

        Returns:
           The overall scale of feeling for all of the given feelings.
        """
        return Scale( round( self._overall_value( feelings ) ) )

    def year_scale( self, year: str ) -> Scale:
        """Get the overall feeling scale for a given year.

        Args:
            year: The year to get the scale for.

        Returns:
            The overall scale of the feelings for that year.

        Note:
            If nothing is recorded for that year, the return value will be
            for a neutral scale.
        """
        return self._overall_scale( self.for_year( year ) )

    def year_value( self, year: str ) -> float:
        """Get the overall feeling value for a given year.

        Args:
            year: The year to get the scale for.

        Returns:
            The overall value of the feelings for that year.

        Note:
            If nothing is recorded for that year, the return value will be
            for a neutral value.
        """
        return self._overall_value( self.for_year( year ) )

    def month_scale( self, year: str, month: str ) -> Scale:
        """Get the overall feeling scale for a given month.

        Args:
            year: The year of the month of the day to get the scale for.
            month: The month to get the scale for.

        Returns:
            The overall scale of the feelings for that month.

        Note:
            If nothing is recorded for that month, the return value will be
            for a neutral scale.
        """
        return self._overall_scale( self.for_month( year, month ) )

    def month_value( self, year: str, month: str ) -> float:
        """Get the overall feeling value for a given month.

        Args:
            year: The year of the month of the day to get the value for.
            month: The month to get the value for.

        Returns:
            The overall value of the feelings for that month.

        Note:
            If nothing is recorded for that month, the return value will be
            for a neutral value.
        """
        return self._overall_value( self.for_month( year, month ) )

    def day_scale( self, year: str, month: str, day: str ) -> Scale:
        """Get the overall feeling scale for a given day.

        Args:
            year: The year of the month of the day to get the scale for.
            month: The month of the day to get the scale for.
            day: The day to get the scale for.

        Returns:
            The overall scale of the feelings for that day.

        Note:
            If nothing is recorded for that day, the return value will be
            for a neutral scale.
        """
        return self._overall_scale( self.for_day( year, month, day ) )

    def day_value( self, year: str, month: str, day: str ) -> float:
        """Get the overall feeling value for a given day.

        Args:
            year: The year of the month of the day to get the value for.
            month: The month of the day to get the value for.
            day: The day to get the value for.

        Returns:
            The overall value of the feelings for that day.

        Note:
            If nothing is recorded for that day, the return value will be
            for a neutral value.
        """
        return self._overall_value( self.for_day( year, month, day ) )

    def add( self, feeling: Feeling ) -> Feeling:
        """Add a feeling.

        Args:
            feeling: The feeling to add.

        Returns:
            The newly-added feeling entry.
        """
        self._history[ feeling.year_key ][ feeling.month_key ][ feeling.day_key ][ feeling.key ] = feeling
        return feeling

    def record( self,
                feeling: Scale | int=Scale.NEUTRAL,
                recorded: datetime | None=None,
                description: str="" ) -> Feeling:
        """Record a feeling.

        Args:
            feeling: The scale of the feeling.
            recorded: Optional time at which the feeling was recorded.
            description: A description to associate with the feeling.

        Raises:
            ValueError: If an integer feeling is out of range.

        Returns:
            The newly-created feeling entry.
        """
        return self.add( Feeling(
            datetime.now() if recorded is None else recorded,
            Scale( feeling ),
            description
        ) )

    def __iter__( self ) -> Iterator[ Feeling ]:
        """Allow iterating through all the recorded feelings.

        Yields:
            Each feeling record.
        """
        for year in self._history.values():
            for month in year.values():
                for day in month.values():
                    yield from day.values()

    @property
    def as_dict( self ) -> FeelingsDict:
        """The feelings as a JSON-friendly dictionary."""
        return { feeling.key: feeling.as_dict for feeling in self }

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

    def __getitem__( self, key: str ) -> Feeling:
        return self._history[ key[ 0:4 ] ][ key[ 5:7 ] ][ key[ 8:10 ] ][ key ]

### feelings.py ends here
