from setuptools import setup, find_packages


setup(
    name='promptist',
    version='0.1.0',
    packages=find_packages(),        # Автоматически найдет все пакеты и модули
    install_requires=[
        'annotated-types==0.7.0',
        'pydantic==2.9.0',
        'pydantic_core==2.23.2',
        'typing_extensions==4.12.2',
        'tzdata==2024.1',
    ],
    author='Tsotne Otanadze',              # Автор
    author_email='your_email@example.com',  # Email автора
    description='Short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Тип содержания README (Markdown)
    url='https://github.com/otanadzetsotne/promptist',  # URL проекта, если есть
    classifiers=[                   # Классификаторы (метаданные)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
