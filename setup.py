from setuptools import setup, find_packages

setup(
    name='assignment0',
    version='1.0',
    author='Vedant Upganlawar',
    author_email='v.upganlawar@ufl.edu',
    packages=find_packages(exclude=('tests', 'docs', 'resources')),
    setup_requires=['pytest-runner', 'tabula', 'requests', 'sqlite3'],
    tests_require=['pytest']
)
