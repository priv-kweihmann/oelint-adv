import setuptools

import subprocess
_long_description = "See https://github.com/priv-kweihmann/oelint-adv for documentation"
_long_description_content_type = "text/plain"
try:
    _long_description = subprocess.check_output(
        ["pandoc", "--from", "markdown", "--to", "rst", "README.md"]).decode("utf-8")
    _long_description_content_type = "text/x-rst"
except (subprocess.CalledProcessError, FileNotFoundError):
    pass

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="oelint_adv",
    version="1.22.1",
    author="Konrad Weihmann",
    author_email="kweihmann@outlook.com",
    description="Advanced bitbake-recipe linter",
    long_description=_long_description,
    long_description_content_type=_long_description_content_type,
    url="https://github.com/priv-kweihmann/oelint-adv",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "oelint-adv = oelint_adv.__main__:main",
        ]
    },
    install_requires=requirements,
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
