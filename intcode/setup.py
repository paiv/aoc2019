
NAME = 'intcode'
VERSION = '0.2.0'
DESCRIPTION = 'AoC 2019 Intcode VM Assembler'
AUTHOR = 'Pavel paiv Ivashkov'
LICENSE = 'MIT'
URL = 'https://github.com/paiv/'


from setuptools import setup

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    license=LICENSE,
    url=URL,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],

    packages=['intcode'],

    python_requires='>=3.6',
    install_requires=['Jinja2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
            'intcode=intcode.cli:cli',
            'icd=intcode.icd:cli',
        ]
    },
)
