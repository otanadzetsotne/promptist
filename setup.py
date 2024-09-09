from setuptools import setup, find_packages


setup(
    name='promptist',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'annotated-types==0.7.0',
        'pydantic==2.9.0',
        'pydantic_core==2.23.2',
        'typing_extensions==4.12.2',
        'tzdata==2024.1',
    ],
    author='Tsotne Otanadze',
    author_email='otanadzetsotne@yahoo.com',
    description='Short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/otanadzetsotne/promptist',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
