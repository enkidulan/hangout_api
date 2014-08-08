from setuptools import setup, find_packages
import os
from os.path import join
import imp
setupy_download_helper_path = join(
    os.path.dirname(os.path.abspath(__file__)), 'setupy_download_helper.py')
setupy_download_helper = imp.load_source(
    'setupy_download_helper', setupy_download_helper_path)

setupy_download_helper.CHROMEDRIVER_URL_BASE = "http://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip"
setupy_download_helper.CHROMEDRIVER_VERSION = '2.10'
setupy_download_helper.DEST_FILE_NAME = 'CHROMEDRIVER'

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
      namespace_packages=['hangout_api'],
      include_package_data=True,
      zip_safe=False,
      cmdclass={'install': setupy_download_helper.InstallCommand,
                'bdist_egg': setupy_download_helper.InstallCommand,
                'develop': setupy_download_helper.DevelopCommand},
      install_requires=[
          'setuptools',
          'selenium',
          'seleniumwrapper',
          'pyscreenshot',
          'entrypoint2',
          'Pillow',
          'pyvirtualdisplay',
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
