"""
Application entry point for PyInstaller.

This script is located at the project root and ensures that the 'temp_cleaner'
directory is treated as a package, allowing relative imports within it to work
correctly when bundled into an executable.
"""
from temp_cleaner.main import main
import sys

if __name__ == '__main__':
    # Set the package context correctly for the bundled app
    # and then call the original main function.
    if getattr(sys, 'frozen', False):
        # When running in a bundle, PyInstaller may not set the package correctly
        __package__ = 'temp_cleaner'
    
    main()