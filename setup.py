import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oelint_adv",
    version="1.0.0",
    author="Konrad Weihmann",
    author_email="kweihmann@outlook.com",
    description="Advanced bitbake-recipe linter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priv-kweihmann/oelint-adv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)