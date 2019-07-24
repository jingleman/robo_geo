
# For creating python extension of the visiLibity c++ Visibility_Polygon functionality.
# Executed with venv python by compile_and_run.
# TO DO:
# --Replace env var w/ arg.

from distutils.core import setup, Extension
    # Had to install Distutils2-py3
import sysconfig
import numpy
import os


extra_compile_args = sysconfig.get_config_var('CPPFLAGS').split()
    # https://buildmedia.readthedocs.org/media/pdf/pythonextensionpatterns/latest/pythonextensionpatterns.pdf
    # hard to find this, and had to rerun many times for some reason.
extra_compile_args += ["-Wall", "-Wextra", "-std=c++11", "-lstdc++"]
extra_compile_args += ["-g3", "-O0", "-DDEBUG=9", "-UNDEBUG"]
	# Commenting this out didn't seem to speed up the Visibility_Polygon contruction.

visilibity_src = os.getenv('VISILIBITY_SRC', default='')
compute_visibility = Extension('compute_visibility',
                      sources=['compute_visibility.cpp', visilibity_src + '/visilibity.cpp'],
                      extra_compile_args=extra_compile_args)
  # Requires sym link or copy of visilibity.cpp

setup(name='compute visibility',
      version='1.0',
      description='Python package with c++ extension for computing visibility.',
      ext_modules=[compute_visibility],
      include_dirs=[numpy.get_include(), visilibity_src + '/'])
  # Somehow adding an absolute path here eliminated visilibity/compute_visibility warnings
  # until I removed the absolute path from compute_visibility.cpp.


