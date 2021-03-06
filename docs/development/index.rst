Contribute
==========

.. contents:: In this section:
   :depth: 2
   :local:


Roadmap
-------

- Add more tests

- Work on packaging

- Use GitHub pages to build a homepage

  - Use `Leaflet <http://leafletjs.com/>`_ to get and display coords on a ...
  - `MapBox <https://www.mapbox.com/>`_ map


Contributing
------------

Contributions are always welcome! Here are a few ways you could contribute:

- Bug fixes
- New tests
- New features
- Testing on different platforms
- Documentation

Support: :ref:`external-links`


Development
-----------

All of the following commands assume you are are starting in the root ``ArchMap`` directory.

System Requirements
^^^^^^^^^^^^^^^^^^^

In addition to the :ref:`install-reqs` for the install, the following packages are required:

- To generate these docs:

  - sphinx

- For packaging:

  - setuptools
  - wheel (optional) - for building :ref:`wheels <build-wheel>`

Documentation
^^^^^^^^^^^^^

`Sphinx <http://sphinx-doc.org/>`_ can be used to build a variety of
`formats <http://sphinx-doc.org/invocation.html#invocation>`_.

First, make sure you're in the docs directory::

    cd docs/

Make the preferred output::

    make html

Open the the index page in your browser::

    firefox _build/html/index.html

Testing
^^^^^^^

``unittest`` is used for testing::

    python setup.py test

This will search the ``tests`` directory for tests.

To check your commits before submitting, it is advisable to set up `pre-commit <http://pre-commit.com/>`_ first.
Install it with::

    pip3 install pre-commit

Then install the hooks so that they automatically run before each commit::

    pre-commit install

Make sure the hooks are up to date::

    pre-commit autoupdate

To run the hooks before a commit use::

    pre-commit run --all-files

For further information, have a look at the pre-commit `advanced features <http://pre-commit.com/#advanced>`_ page
or the :download:`.pre-commit-config.yaml <.pre-commit-config.yaml>` config file to see what is run.

See also:

* `unittest - Python docs <https://docs.python.org/3/library/unittest.html>`_

.. _packaging:

Packaging
^^^^^^^^^

ArchMap is currently packaged in two forms.

Arch Linux package
""""""""""""""""""
Packages are built using the ``PKGBUILD`` and ``archmap.install`` for settings.

To build package using the `PKGBUILD <https://wiki.archlinux.org/index.php/PKGBUILD>`_::

    cd pkgbuild
    makepkg PKGBUILD

See also:

* `Creating packages <https://wiki.archlinux.org/index.php/Creating_packages>`_
* `Python Package Guidelines <https://wiki.archlinux.org/index.php/Python_Package_Guidelines>`_

Python package
""""""""""""""
Packages are built using ``setup.py`` and ``setup.cfg`` for settings.

To build a `source distribution <http://packaging.python.org/en/latest/glossary.html#term-source-distribution-or-sdist>`_::

   python3 setup.py sdist

.. _build-wheel:

To build a `wheel <http://packaging.python.org/en/latest/glossary.html#term-wheel>`_::

   python3 setup.py bdist_wheel

See also:

* `Installation & Packaging Tutorial <http://packaging.python.org/en/latest/tutorial.html>`_
