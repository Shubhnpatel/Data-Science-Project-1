from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = "-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of the required lib
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        [req.replace("\n","") for req in requirements ]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)


setup(
    name = 'mlproject',
    version='0.0.1',
    author='Shubh',
    author_email='shubhnpatel@gmail.com',
    packages=find_packages(), # here find_packages will do one thing that our whole project will be treated as one library of python and this function will find for __init__.py in each folder and which ever have this will be treated as one package 
    install_requires= get_requirements('requirements.txt')
)