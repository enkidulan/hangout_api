from setuptools import setup, find_packages
import os

version = '1.0'

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
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'selenium',
          'seleniumwrapper',
          'pyscreenshot',
          # 'entrypoint2',
          # 'Pillow',
          'pyvirtualdisplay',
          'easydict',
          'chromedriver',
          # -*- Extra requirements: -*-
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
