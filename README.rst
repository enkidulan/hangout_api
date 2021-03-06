Hangout API
============

.. image:: https://travis-ci.org/enkidulan/hangout_api.svg?branch=master
    :target: https://travis-ci.org/enkidulan/hangout_api?branch=master
    :alt: Tests
.. image:: https://coveralls.io/repos/enkidulan/hangout_api/badge.png?branch=master
    :target: https://coveralls.io/r/enkidulan/hangout_api?branch=master
    :alt: Code Coverage
.. image:: https://readthedocs.org/projects/python-hangout-api/badge/?version=latest
    :target: https://readthedocs.org/projects/python-hangout-api/?badge=latest
    :alt: Documentation Status
.. image:: https://landscape.io/github/enkidulan/hangout_api/master/landscape.png
   :target: https://landscape.io/github/enkidulan/hangout_api/master
   :alt: Code Health
.. image:: https://www.versioneye.com/user/projects/551bed6b3661f1de6d0001f6/badge.svg?style=flat
   :target: https://www.versioneye.com/user/projects/551bed6b3661f1de6d0001f6
   :alt: Dependency Status

**Python API for controlling Google+ Hangouts**

.. DANGER::
   This package is under heavy development

Read the `Python Hangout API documentation`_.


Preinstall requirements
=======================

Chrome browser
---------------

Hangout API is using Google Chrome browse, so make sure you have it
installed. To install Chrome on debian based distributions you can use
following command:

            .. code:: bash

                wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
                sudo apt-get update
                sudo apt-get install google-chrome-stable -y

PyVirtualDisplay requirements
-------------------------------

Make sure that `PyVirtualDisplay requirements`_ are installed.
In most cases it will be enough to run command:

        .. code:: bash

            $ sudo apt-get install python-dev python-imaging xvfb scrot -y


.. _Python Hangout API documentation: http://python-hangout-api.readthedocs.org
.. _PyVirtualDisplay requirements: https://pypi.python.org/pypi/PyVirtualDisplay
