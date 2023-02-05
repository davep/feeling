"""Defines the code for loading/holding/saving the feeling data."""

##############################################################################
# Python imports.
from __future__  import annotations
from typing      import cast, TypeAlias
from datetime    import datetime
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
    def key( self ) -> str:
        """The key for the feeling."""
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
        self._history: dict[ str, Feeling ] = {}

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
        self._history[ entry.key ] = entry
        return entry

    @property
    def as_dict( self ) -> FeelingsDict:
        """The feelings as a JSON-friendly dictionary."""
        return { key: feeling.as_dict for key, feeling in self._history.items() }

    def from_dict( self, data: FeelingsDict ) -> "Feelings":
        """Reset the data to that given in the dictionary.

        Args:
            data: A dictionary containing the feelings data.

        Returns:
            self
        """
        self._history = { key: Feeling.from_dict( value ) for key, value in data.items() }
        return self

### feelings.py ends here
