from setuptools import setup, find_packages

requirements = ['cycler==0.10.0',
                'future==0.15.2',
                'geopy==1.11.0',
                'isodate==0.5.4',
                'nose==1.3.7',
                'numpy==1.14.4',
                'pandas==0.20.2',
                'patsy==0.4.1',
                'py==1.4.31',
                'pyparsing==2.1.9',
                'pytest==3.0.3',
                'python-dateutil==2.5.3',
                'pytz==2018.4',
                'requests==2.11.1',
                'six==1.10.0',
                'slisonner']


setup(
    name="slayer",
    version='0.3.27',
    author="Nikita Pestrov",
    author_email="nikita.pestrov@habidatum.com",
    description=("Index tabular data into volume slices, convert volumes to"
                 "projects and environments."),
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
    dependency_links=['git+ssh://git@bitbucket.org/mathrioshka/slisonner.git#egg=slisonner'],
    classifiers=['Programming Language :: Python :: 3.6']
)
