from setuptools import setup, find_packages

setup(
    name='actividad',
    version='0.1.0',
    packages=find_packages(),
    python_requires= '>3.7',
    install_requires=[
        'openpyxl==3.1.3',
        'pandas==1.3.5',
        'selenium==4.11.2',
        'webdriver-manager==4.0.2'
    ]
)