from setuptools import setup

setup(name='wirecode',
      version='0.1',
      description='For stretched wire analysis',
      url='http://github.com/tobinjones',
      author='Tobin Jones',
      author_email='tobin.jones@buckleysystems.com',
      license='All rights reserved',
      packages=['wirecode'],
      install_requires=[
          'numpy',
          'matplotlib',
          'scipy',
          'setuptools'
      ],
      zip_safe=False)
