from setuptools import find_packages, setup

setup(
    name='evalmyai',
    packages=find_packages(include=['evalmyai']),
    version='0.1.0',
    description='EVALMY.AI Python library',
    author='Petr Pascenko <petr.pascenko@profinit.eu>',
    setup_requires=['requests'],
    tests_require=['unittest', 'pandas'],
)
