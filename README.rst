=======================
jupyter_process_manager
=======================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/jupyter_process_manager
    :target: https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://travis-ci.org/stas-prokopiev/jupyter_process_manager.svg?branch=master
    :target: https://travis-ci.org/stas-prokopiev/jupyter_process_manager

.. image:: https://img.shields.io/pypi/v/jupyter_process_manager
   :target: https://img.shields.io/pypi/v/jupyter_process_manager
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/jupyter_process_manager
   :target: https://img.shields.io/pypi/pyversions/jupyter_process_manager
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Overview.
=========================

This is a library which helps working with many processes in a jupyter notebook in a very simple way.

Installation via pip:
======================

.. code-block:: bash

    pip install jupyter_process_manager

Usage examples
===================================================================

| Lets say that you want to run some function defined in file **test_function.py**
| with different arguments as separate processes and have control over them.


.. code-block:: python

    # In the file test_function.py
    def test_just_wait(int_seconds):
        for int_num in range(int_seconds):
            print(int_num)
            sleep(1)

Then to run it you just need to do the following:

.. code-block:: python

    from jupyter_process_manager import JPM
    # OR from jupyter_process_manager import JupyterProcessManager
    from .test_function import test_just_wait
    # Create an object which will be handling processes
    process_manager = JPM(".")

    for seconds_to_wait in range(5, 50, 5):
        process_manager.add_function_to_processing(test_just_wait, seconds_to_wait)

All the processes were started and now you can check what is happening with them

**WARNING: Please do NOT try to use functions defined inside jupyter notebook, they won't work.**

Show processes output as widget
--------------------------------------------------------------------------------------------------

.. code-block:: python

    process_manager.show_jupyter_widget(
        int_seconds_step=2,
        int_max_processes_to_show=20
    )

.. image:: images/2.PNG

JPM arguments
--------------------------------------------------------------------------------------------------

#. **str_dir_for_output**: Directory where to store processes output
#. **is_to_delete_previous_outputs=True**: Flag If you want to delete outputs for all previous processes in the directory

Usual print output
--------------------------------------------------------------------------------------------------

.. code-block:: python

    process_manager.wait_till_all_processes_are_over(int_seconds_step=2)

.. image:: images/1.PNG


How to Debug
--------------------------------------------------------------------------------------------------

.. code-block:: python

    debug_run_of_1_function(self, func_to_process, *args, **kwargs)

Links
=====

    * `PYPI <https://pypi.org/project/jupyter_process_manager/>`_
    * `readthedocs <https://jupyter_process_manager.readthedocs.io/en/latest/>`_
    * `GitHub <https://github.com/stas-prokopiev/jupyter_process_manager>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/CHANGELOG.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.
