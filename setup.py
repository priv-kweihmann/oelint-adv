import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oelint_adv",
    version="1.2.0",
    author="Konrad Weihmann",
    author_email="kweihmann@outlook.com",
    description="Advanced bitbake-recipe linter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priv-kweihmann/oelint-adv",
    packages=setuptools.find_packages(),
    scripts=['bin/oelint-adv'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
)