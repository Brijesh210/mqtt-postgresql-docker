from setuptools import setup, find_packages

setup(
    name='HomeWork',
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where='src'),
    package_dir={"": "src"},
)
