from setuptools import setup, find_packages

setup(
    name='restapi',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'marshmallow'
    ],
    entry_points={
        'console_scripts': [
            'run=restapi.main:run',
        ],
    },
)
