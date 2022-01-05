from setuptools import find_packages, setup


with open("requirements.txt", "r") as requirements_txt:
    requirements = requirements_txt.read().splitlines()


setup(
   name="sensory_cloud",
   version="0.0.1",
   description="Python SDK for Sensory Cloud",
   author="Jonathan Hersch",
   author_email="jhersch@sensoryinc.com",
   packages=find_packages(where="src"),
   package_dir={"": "src"},
   install_requires=requirements
)