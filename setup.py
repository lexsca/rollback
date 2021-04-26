from setuptools import setup

setup(
    name="rollback",
    version="1.0.8",
    description="Simple rollback mechanism",
    long_description=open("README.rst").read(),
    author="Lex Scarisbrick",
    author_email="lex@scarisbrick.org",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/lexsca/rollback",
    py_modules=["rollback"],
)
