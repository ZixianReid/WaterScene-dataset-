
from setuptools import setup
from setuptools import find_packages

requirements = [
      "logging",
      "matplotlib",
      "numpy"
]

setup(
    name="waterScene",
    version="1.0",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)

