import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'requests',
    'click'
    ]

setup(name='openwifi_cli',
      version='0.0',
      description='openwifi',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='openwifi-cli',
      install_requires=requires,
      entry_points= {
          'console_scripts' : [
              'openwifi-cli = openwifi_cli.__init__:main',
              ]
          },
      )
