# setup.py

""" Project installation configuration """

from setuptools import setup, find_packages

setup(
    name="serply_notifications_app",
    version="1.0.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
)