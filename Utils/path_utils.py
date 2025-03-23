import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Icon directory
ICON_DIR = os.path.join(PROJECT_ROOT, "Cfg", "Resources", "icons")

def get_icon_path(icon_name):
    """
    Get the full path to an icon file

    Args:
        icon_name: Name of the icon file (e.g. 'login.png')

    Returns:
        str: Full path to the icon file
    """
    return os.path.join(ICON_DIR, icon_name)

def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource relative to project root
    
    Args:
        relative_path: Path relative to project root directory
    """
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
