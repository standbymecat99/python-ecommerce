import setuptools

setuptools.setup(
    name='python-ecommerce',
    version='0.1',
    author="Simple Ideas Technology Limited",
    description="An ecommerce library for python",
    long_description="An ecommerce library for python",
    packages=setuptools.find_packages(),
    package_data={
        'ecommerce': ['alembic.ini', 'migrations/*', 'migrations/**/*'
                      'country_data/*', 'country_data/**/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "SQLAlchemy>=1.1.0",
        "alembic>=0.8.9",
        "stripe>=2.40.0"
    ],
    entry_points={'console_scripts': ['ecommerce=ecommerce.ecommerce:main']}
 )
