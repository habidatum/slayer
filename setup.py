from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="slayer",
    version='0.3.0',
    author="Nikita Pestrov",
    author_email="nikita.pestrov@habidatum.com",
    description=("Index tabular data into volume slices, convert volumes to"
                 "projects and environments."),
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
    dependency_links=['git+ssh://git@bitbucket.org/mathrioshka/slisonner.git#egg=slisonner'],
    classifiers=['Programming Language :: Python :: 3.4']
)
