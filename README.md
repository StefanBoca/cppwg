# cppwg

Automatically generate PyBind11 code for Python wrapping C++ projects.

## Example

`shapes/` is a full example project, demonstrating how to generate a Python package `pyshapes` from
C++ source code. It is recommended that you use it as a template project when getting started.

As a small example, we can start with a free function in `shapes/src/math_funcs/SimpleMathFunctions.hpp`:

```c++
#ifndef _SIMPLEMATHFUNCTIONS_HPP
#define _SIMPLEMATHFUNCTIONS_HPP

/**
 * Add the two input numbers and return the result
 * @param i the first number
 * @param j the second number
 * @return the sum of the numbers
 */
int add(int i, int j)
{
    return i + j;
}

#endif  // _SIMPLEMATHFUNCTIONS_HPP
```

add a package description to `shapes/wrapper/package_info.yaml`:

```yaml
name: pyshapes
modules:
  - name: math_funcs
    free_functions: cppwg_ALL
```

and run `cppwg` (with suitable arguements).

The generator will create the following PyBind wrapper code in `shapes/wrapper/math_funcs/math_funcs.main.cpp`:

```c++
#include <pybind11/pybind11.h>
#include "wrapper_header_collection.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_math_funcs, m)
{
    m.def("add", &add, "");
}
```

which can be built into a Python module and (with some import tidying) used as follows:

```python
from pyshapes import math_funcs
a = 4
b = 5
c = math_funcs.add(4, 5)
print c
>>> 9
```

## Usage

It is recommended that you [learn how to use PyBind11 first](https://pybind11.readthedocs.io/en/stable/). This project just
generates PyBind11 wrapper code, saving lots of boilerplate in bigger projects.

### Test the Installation

To generate the full `pyshapes` wrapper do:

```bash
git clone https://github.com/jmsgrogan/cppwg.git
cd cppwg
pip install .
cppwg --source_root shapes/src/ --wrapper_root shapes/wrapper/ --package_info shapes/wrapper/package_info.yaml --includes shapes/src/
```

then to build the example package do:

```bash
mkdir shapes/build
cd shapes/build
cmake ..
make
```

To test the resulting package do:

```bash
python test_functions.py
python test_classes.py
```

### Starting a New Project

- Make a wrapper directory in your source tree `mkdir wrapper`
- Copy the template in `cppwg\shapes\wrapper\package_info.yaml` to `wrapper` and fill it in.
- Run `cppwg` to generate the PyBind11 wrapper code in `wrapper`.
- Follow the [PyBind11 guide](https://pybind11.readthedocs.io/en/stable/compiling.html) for building with CMake, using `shapes\CMakeLists.txt` as an initial guide.
