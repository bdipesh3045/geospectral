# The '.' means "from the current directory"
# We are importing the function 'describe_tiff' from the file 'describe_tiff.py'
from .describe_tiff import describe_tiff

# (Optional) If you have functions in operation.py, add them here later like this:
# from .operation import some_function

# This defines what gets imported if someone types "from augmentation import *"
__all__ = ["describe_tiff"]