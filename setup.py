import codecs
import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "pygmsh", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="pygmsh",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    description="Python frontend for Gmsh",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url=about["__website__"],
    project_urls={"Documentation": "https://pygmsh.readthedocs.org/en/latest"},
    license=about["__license__"],
    platforms="any",
    install_requires=["meshio >=3.0, <4.0", "numpy >= 1.9"],
    python_requires=">=3",
    keywords=["mesh", "gmsh", "mesh generation", "mathematics"],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
