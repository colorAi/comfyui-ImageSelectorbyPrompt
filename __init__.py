# __init__.py

# The dot (.) before "adv_image_selector" is crucial. 
# It means "import from the same directory as this __init__.py file".
from .image_selector_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# This is a special variable that tells Python what to export when someone does "from your_package import *"
# It's good practice to include it.
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']