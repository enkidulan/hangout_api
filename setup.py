from setuptools import setup, find_packages
import os
import sys

version = '1.0'

install_requires = [
    'setuptools',
    'selenium',
    'seleniumwrapper',
    'pyscreenshot',
    'entrypoint2',
    'Pillow',
    'pyvirtualdisplay',
    'easydict',
    'chromedriver',
    'zope.interface',
    'zope.component',
    'retrying>=1.3.1enkidu',
    # -*- Extra requirements: -*-
]

if sys.version[:3] < '3.4':
    install_requires.append('enum34')

setup(name='hangout_api',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Google Hangout API',
      author='Maksym Shalenyi (enkidulan)',
      author_email='supamaxy@gmail.com',
      url='https://github.com/enkidulan/hangout_api',
      license='apache2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      dependency_links=[
        'http://dist.enkidulan.tk/retrying-1.3.1enkidu.zip',
      ],
      extras_require={
          'tests': ['testfixtures',
                    'nose',
                    'nose-selecttests',
                    'pyyaml',
                    ]
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
