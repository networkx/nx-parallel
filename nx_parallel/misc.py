import importlib

def optional_package(pkg_name):
    """Import an optional package and return the package and whether it was found.
    Parameters
    ----------
    pkg_name : str
        The name of the package to import.
    Returns
    -------
    pkg : module
        The imported package.
    has_pkg : bool
        Whether the package was found.
    pkg_version : str
        The version of the package.
    """
    try:
        pkg = importlib.import_module(pkg_name)
        has_pkg = True
        if hasattr(pkg, "__version__"):
            pkg_version = pkg.__version__
        else:
            pkg_version = None
    except ImportError:
        pkg = None
        has_pkg = False
        pkg_version = None
    return pkg, has_pkg, pkg_version