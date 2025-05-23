import setuptools

from oelint_adv.version import __version__

with open('README.md') as f:
    _long_description = f.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='oelint_adv',
    version=__version__,
    author='Konrad Weihmann',
    author_email='kweihmann@outlook.com',
    description='Advanced bitbake-recipe linter',
    license='BSD-2-Clause',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/priv-kweihmann/oelint-adv',
    packages=setuptools.find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'oelint-adv = oelint_adv.__main__:main',
        ],
    },
    package_data={
        'oelint_adv': ['data/*'],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance',
    ],
    python_requires='>=3.9',
)
