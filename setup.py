import setuptools


def read(file: str):
    with open(file, 'r') as file:
        return file.read()


setuptools.setup(
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
)
