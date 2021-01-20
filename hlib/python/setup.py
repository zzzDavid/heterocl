from setuptools import setup, find_packages
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)

def get_lib_path():
    """Get library path, name and version"""
    # We can not import `libinfo.py` in setup.py directly since __init__.py
    # Will be invoked which introduces dependences
    libinfo_py = os.path.join(CURRENT_DIR, '../../python/heterocl/tvm/_ffi/libinfo.py')
    libinfo = {'__file__': libinfo_py}
    exec(compile(open(libinfo_py, "rb").read(), libinfo_py, 'exec'), libinfo, libinfo)
    version = libinfo['__version__']
    lib_path = libinfo['find_lib_path']()
    libs = [lib_path[0]]
    if libs[0].find("runtime") == -1:
        for name in lib_path[1:]:
            if name.find("runtime") != -1:
                libs.append(name)
                break
    return libs, version

LIB_LIST, __version__ = get_lib_path()

curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
for i, path in enumerate(LIB_LIST):
    LIB_LIST[i] = os.path.relpath(path, curr_path)
setup_kwargs = {
    "include_package_data": True,
    "data_files": [('lib', LIB_LIST)]
}

# Include extern ip files
if os.path.exists("MANIFEST.in"):
    os.remove("MANIFEST.in")

EXTERN_IP_DIR = os.path.join(CURRENT_DIR, "hlib/ip")
with open("MANIFEST.in", "w") as fp:
    for subdir, dirs, files in os.walk(EXTERN_IP_DIR):
        for file_name in files:
            if not (file_name.endswith(".pyc") or file_name.endswith(".py")):
                filepath = subdir + os.sep + file_name
                fp.write("include {}\n".format(filepath))

setup(
  name = "hlib",
  version = "0.1",
  packages = find_packages(),
  install_requires=[
      'numpy==1.18.5',
      'decorator',
      'networkx',
      'matplotlib',
      'backports.functools_lru_cache',
      'ordered_set',
      'keras==2.3.1',
      'tensorflow==2.4.0',
      'tvm',
      ],
  **setup_kwargs)
