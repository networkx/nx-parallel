## Installation

It is recommended to first refer the [NetworkX's INSTALL.rst](https://github.com/networkx/networkx/blob/main/INSTALL.rst).
nx-parallel requires Python >=3.11. Right now, the only dependencies of nx-parallel are networkx and joblib.

### Installing nx-parallel using `pip`

You can install the stable version of nx-parallel using pip:

```sh
pip install nx-parallel
```

The above command also installs the two main dependencies of nx-parallel i.e. networkx
and joblib. To upgrade to a newer release use the `--upgrade` flag:

```sh
pip install --upgrade nx-parallel
```

### Installing the development version

Before installing the development version, you may need to uninstall the
standard version of `nx-parallel` and other two dependencies using `pip`:

```sh
pip uninstall nx-parallel networkx joblib
```

Then do:

```sh
pip install git+https://github.com/networkx/nx-parallel.git@main
```

### Installing nx-parallel with conda

Installing `nx-parallel` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

```sh
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Once the `conda-forge` channel has been enabled, `nx-parallel` can be installed with `conda`:

```sh
conda install nx-parallel
```

or with `mamba`:

```sh
mamba install nx-parallel
```
