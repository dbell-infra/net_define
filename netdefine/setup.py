from setuptools import setup, find_packages

setup(
    name='netdefine',
    version="0.0.1",
    description="declarative modular configuration engine",
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
        'deepdiff',
        'jinja2'
    ],
    entry_points={
        'console_scripts': ['netdefine=netdefine.cli:cli']
    }
)
