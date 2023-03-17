"""Base widget for holding a feeling-related item."""

##############################################################################
# Textual imports.
from textual.widgets import ListItem

##############################################################################
# Local imports.
from ..data import Scale, Feelings

##############################################################################
class FeelingItem( ListItem ):
    """Base class for a feeling list item."""

    DEFAULT_CSS = """
    FeelingItem {
        height: 3;
        padding: 0 2 0 2;
    }

    FeelingItem > Label {
        width: 100%;
        height: 100%;
        color: black;
        padding: 1 0 0 1;
    }

    FeelingItem > Label.very_low {
        color: white;
        background: red;
    }

    FeelingItem > Label.low {
        background: #ff5f00;
    }

    FeelingItem > Label.neutral {
        background: #008700;
    }

    FeelingItem > Label.good {
        background: #00d700;
    }

    FeelingItem > Label.very_good {
        background: #00ff5f;
    }
    """

    def __init__( self, feelings: Feelings ) -> None:
        super().__init__()
        self._feelings = feelings

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

### feeling_item.py ends here
