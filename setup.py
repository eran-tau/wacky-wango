from setuptools import setup, find_packages


setup(
    name = 'wacky wango',
    version = '0.1.0',
    author = 'Eran Kirshenboim',
    description = 'An example package.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
