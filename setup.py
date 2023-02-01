from setuptools import setup, find_packages


setup(
    name="serply_notifications",
    version="1.0.0",
    packages=find_packages('src'),
    package_dir={"": 'src'},
)
