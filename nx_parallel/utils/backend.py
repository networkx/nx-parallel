import inspect
import nx_parallel.algorithms as algorithms

__all__ = ["get_info"]

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
                            # Extracting Parallel Computation description
                            # Assuming that the first para in docstring is the function's PC desc
                            par_docs_ = docstring.split("\n\n")[0]
                            par_docs_ = par_docs_.split("\n")
                            par_docs_ = [
                                line.strip() for line in par_docs_ if line.strip()
                            ]
                            par_docs = "\n".join(par_docs_)
                        except IndexError:
                            par_docs = None

                    except Exception as e:
                        print(e)
                        par_docs = None

                    funcs[function] = {
                        "backend_func_url": f"https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/{file_name}.py#{func_line}",
                        "backend_func_docs": par_docs,
                        "additional_parameters": None,  # just for now, as we don't have any additional parameters in any function
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
