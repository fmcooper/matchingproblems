from setuptools import find_packages, setup

setup(
	name='matchingproblems',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A matching problem generator and solver.',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'pulp'],
    url='http://github.com/fmcooper/matchingproblems',
    author='Frances Cooper',
    author_email='fmcooper234@gmail.com'
)