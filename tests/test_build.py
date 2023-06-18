import platform

# import sys

if platform.system() == 'Windows':
    from distutils.errors import DistutilsPlatformError

    from setuptools import Extension, setup
    from setuptools.command.build_ext import build_ext
else:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext
    from distutils.errors import (
        CCompilerError,
        DistutilsExecError,
        DistutilsPlatformError,
    )

from pathlib import Path

BASE_DIR = Path().resolve()

ext_modules = [
    Extension(
        "_readdbc",
        sources=[
            "pyreaddbc/c-src/dbc2dbf.c",
            "pyreaddbc/c-src/blast.c",
        ],
        include_dirs=["pyreaddbc/c-src/"],
    ),
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed("File not found. Could not compile C extension.")

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (
            CCompilerError,
            DistutilsExecError,
            DistutilsPlatformError,
            ValueError,
        ):
            raise BuildFailed("Could not compile C extension.")


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": ExtBuilder}}
    )


def test_linux():
    try:
        setup(
            script_name="build_test.py",
            script_args=["build_ext", "--inplace"],
            ext_modules=ext_modules,
        )
    except BuildFailed as e:
        print(str(e))
    else:
        print("C extension module successfully built on Linux.")


def test_windows():
    try:
        setup(
            script_name="build_test.py",
            script_args=["build_ext", "--inplace"],
            ext_modules=ext_modules,
        )
    except BuildFailed as e:
        print(str(e))
    else:
        print("C extension module successfully built on Windows.")


if __name__ == "__main__":
    if platform.system() == 'Windows':
        test_windows()
    else:
        test_linux()
