from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(name='opencombatflow',
      version='1.0',
      description='Tools for rapid development of RPGs',
      url='https://github.com/architectdrone/OpenCombatFlow',
      author='Owen Mellema',
      license='MIT',
      keywords='games game rpg turn',
      long_description=long_description,
      include_package_data=True)