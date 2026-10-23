from setuptools import setup

setup(
    name='interface',
    packages=['interface'],
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'flask',
        'colorama'
    ],
)