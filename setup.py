from setuptools import find_packages, setup


with open("requirements.txt", "r") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sensory_cloud",
    version="0.11.0",
    description="Python SDK for Sensory Cloud",
    author="Jonathan Hersch",
    author_email="jhersch@sensoryinc.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sensory-Cloud/python-sdk",
    license_files = ('LICENSE.txt',),
)