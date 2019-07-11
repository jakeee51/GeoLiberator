import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "GeoLiberator",
    version = "0.1.6",
    author = "David J. Morfe",
    author_email = "jakemorfe@gmail.com",
    description = "A small module that cleans, parses and standardizes addresses",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jakeee51/GeoLiberator",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
)
