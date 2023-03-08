from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='sensuous',
      version='0.0.1',
      description='Sensuous spotify prediction system backend package',
      install_requires=requirements,
      packages=find_packages())
