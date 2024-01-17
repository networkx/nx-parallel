from .algorithms import *
from .interface import *
from .utils import *

__version__ = "0.2rc0.dev0"

import inspect
import networkx as nx
import nx_parallel as nxp


def get_info():
    """Return a dictionary with information about the package."""

    def get_funcs_info():
        """Return a dictionary with all the information about all the functions."""

        def get_function_parameters(function_name, package=nx, file_name=None):
            """Returns a list of parameter names of the given function, if it's in networkx"""
            try:
                if file_name in [
                    "tournament",
                ]:  # can add more to this list later
                    module_obj = getattr(package, file_name)
                    function_obj = getattr(module_obj, function_name)
                else:
                    function_obj = getattr(package, function_name)
                parameters = inspect.signature(function_obj).parameters
                parameter_names = list(parameters.keys())
                return parameter_names

            except AttributeError:
                print(f"Function '{function_name}' not found in NetworkX.")
                return None

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
                            # Extracting additional parameters section

                            # Requirement : all additional parameters should be
                            # described after the non-additional parameters
                            all_params_list = get_function_parameters(
                                function, package=nxp, file_name=str(file_name).strip()
                            )
                            non_add_params = get_function_parameters(
                                function, package=nx, file_name=str(file_name).strip()
                            )
                            first_add_para = all_params_list[
                                all_params_list.index(non_add_params[-3]) + 1
                            ]
                            all_params = docstring.split("Parameters")[1].split(
                                "-------"
                            )[1][4:]
                            if function in [
                                "closeness_vitality",
                            ]:
                                all_params = all_params.split("Other parameters")[0]
                            else:
                                all_params = all_params.split("Returns")[0]

                            string = first_add_para + " : "
                            add_params_ = all_params.split(string)[-1]
                            add_params = string + add_params_

                        except IndexError:
                            add_params = None

                        try:
                            # Extracting Parallel Computation section

                            # Requirement : "Parallel Computation :" should
                            # be the last paragraph, preferably before Parameters
                            par_docs = docstring.split("Parallel Computation : ")[1]
                            par_docs = par_docs.split("-------")[0]
                            par_docs = "\n".join(
                                [
                                    line.strip()
                                    for line in par_docs.split("\n")
                                    if line.strip()
                                ][:-1]
                            )
                        except IndexError:
                            par_docs = None

                    except Exception as e:
                        print(e)
                        add_params, par_docs = None, None

                    funcs[function] = {
                        "backend_func_url": f"https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/{file_name}.py#{func_line}",
                        "backend_func_docs": par_docs,
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
