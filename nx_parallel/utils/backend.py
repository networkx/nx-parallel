import nx_parallel.algorithms as algorithms


__all__ = ["get_info"]


def get_info():
    """Return a dict with info about the package like functions supported."""

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

                        try:
                            # Extracting extra parameters
                            # Assuming that the last para in docstring is the function's extra params
                            par_params_ = docstring.split("------------")[1]

                            par_params_ = par_params_.split("\n")
                            par_params_ = [
                                line.strip() for line in par_params_ if line.strip()
                            ]
                            par_params = "\n".join(
                                par_params_[:-1]
                            )  # removing last line with the networkx link
                        except IndexError:
                            par_params = None
                    except Exception as e:
                        print(e)
                        par_docs = None

                    funcs[function] = {
                        "extra_docstring": par_docs,
                        "extra_parameters": par_params,
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
