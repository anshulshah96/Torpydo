from setuptools import setup

setup(name='torpydo',
		version='0.0.1',
		packages=['torpydo'],
		entry_points={
		  'console_scripts': [
		      'torpydo = torpydo.__main__:main'
		  ]
		},
    )