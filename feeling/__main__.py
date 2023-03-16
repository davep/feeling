"""Main entry point for the application."""

##############################################################################
# Local imports.
from . import cli, chui

##############################################################################
def main() -> None:
    """Main entry point."""
    # If the CLI didn't handle this invocation...
    if not cli.run():
        # ...go with the full CHUI.
        chui.run()

##############################################################################
# Run the app if we're being called as the main entry point.
if __name__ == "__main__":
    main()

### __main__.py ends here
