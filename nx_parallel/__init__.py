from .algorithms import *
from .interface import *
from .utils import *

__version__ = "0.2rc0.dev0"

import inspect


def get_info():
    """Return a dictionary with information about the package."""

    def get_funcs_info():
        """Return a dictionary with all the information about all the functions."""
        funcs = {}
        for file_name in dir(algorithms):
            file_module = getattr(algorithms, file_name, None)
            if file_module is not None and hasattr(file_module, "__all__"):
                all_list = getattr(file_module, "__all__")
                functions = [
                    name
                    for name in all_list
                    if callable(getattr(file_module, name, None))
                ]
                for function in functions:
                    try:
                        func_line = inspect.getsourcelines(
                            getattr(file_module, function)
                        )[1]
                    except Exception as e:
                        print(e)
                        func_line = None
                    try:
                        # Extracting docstring
                        docstring = getattr(file_module, function).__doc__

                        try:
                            # extracting examples section
                            examples = docstring.split("Examples")[1].split("--------")[
                                1
                            ]
                        except IndexError:
                            examples = None

                        try:
                            # extracting additional parameters section
                            add_params = (
                                docstring.split("Additional Parameters")[1]
                                .split("----------------------")[1]
                                .split("-------")[0]
                            )
                            add_params = "\n".join(
                                [
                                    line.strip()
                                    for line in add_params.split("\n")
                                    if line.strip()
                                ][:-1]
                            )
                        except IndexError:
                            add_params = None

                        try:
                            # extracting Parallel Computation section
                            para_comp = (
                                docstring.split("Parallel Computation")[1]
                                .split("---------------------")[1]
                                .split("-------")[0]
                            )
                            para_comp = "\n".join(
                                [
                                    line.strip()
                                    for line in para_comp.split("\n")
                                    if line.strip()
                                ][:-1]
                            )
                        except IndexError:
                            para_comp = None

                    except Exception as e:
                        print(e)
                        examples, add_params, para_comp = None, None, None

                    funcs[function] = {
                        "backend_func_url": f"https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/{file_name}.py#{func_line}",
                        "backend_func_docs": para_comp,
                        "backend_func_examples": examples,
                        "additional_parameters": add_params,
                    }

        return funcs

    return {
        "backend_name": "parallel",
        "project": "nx-parallel",
        "package": "nx_parallel",
        "url": "https://github.com/networkx/nx-parallel",
        "short_summary": "Parallel backend for NetworkX algorithms",
        "functions": get_funcs_info(),
    }
