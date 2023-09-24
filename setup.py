from setuptools import setup, find_packages

setup(
    name='visualNoise',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'visualNoise=app.app:main'
        ],
    },
    author='Maya Soni',
    author_email='msoni122@gmail.com',
    description='Creating strucutred visual noise from m sequences',
    url='https://github.com/msoni122/visualNoise.git',
    license='MIT',
)
