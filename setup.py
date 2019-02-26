from setuptools import setup

def readme():
      with open("readme.md") as f:
            return f.read()

setup(name='opencombatflow',
      version='1.0',
      description='Tools for rapid development of RPGs',
      url='https://github.com/architectdrone/OpenCombatFlow',
      author='Owen Mellema',
      license='MIT',
      keywords='games game rpg turn',
      include_package_data=True)