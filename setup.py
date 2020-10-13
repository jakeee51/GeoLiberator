import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = "GeoLiberator",
    version = "0.3.7",
    author = "David J. Morfe",
    author_email = "morphetech@gmail.com",
    license = "MIT",
    description = "A small module that cleans, parses and standardizes addresses",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jakeee51/GeoLiberator",
    packages = setuptools.find_packages(),
    py_modules = ["geoliberator"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)
