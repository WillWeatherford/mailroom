"""Test excercise to learn about setup files."""

from setuptools import setup


setup(name='mailroom',
      description='Command line program to manage Mailroom Madness.',
      version=0.1,
      keywords=[],
      classifiers=[],
      author='Will Weatherford',
      author_email='weatherford.william@gmail.com',
      license='MIT',
      packages=[],  # all your python packages with an __init__ file
      py_modules=['mailroom'],  # your python modules to include
      package_dir={'': 'src'},
      install_requires=[],
      extras_require={'test': ['pytest', 'pytest-xdist', 'tox']}
      )
