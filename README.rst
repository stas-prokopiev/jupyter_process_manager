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

Lets say that you want to run many processes with different arguments for the function below

.. code-block:: python

    def test_just_wait(int_seconds):
        for int_num in range(int_seconds):
            print(int_num)
            sleep(1)

Then to run it you just need to do the following:

.. code-block:: python

    from jupyter_process_manager import JupyterProcessesManager
    # Create an object which will be handling processes
    process_manager = JupyterProcessesManager(".")

    for seconds_to_wait in range(5, 50, 5):
        process_manager.add_function_to_processing(test_just_wait, seconds_to_wait)


All the processes were started and now you can check what is happening with them


Show processes output as widget
--------------------------------------------------------------------------------------------------

.. code-block:: python

    process_manager.show_jupyter_widget(
        int_seconds_step=2,
        int_max_processes_to_show=20
    )

.. image:: images/2.PNG

JupyterProcessesManager arguments
--------------------------------------------------------------------------------------------------

#. **str_dir_for_output**: Directory where to store processes output
#. **is_to_delete_previous_outputs=True**: Flag If you want to delete outputs for all previous processes in the directory



Usual print output
--------------------------------------------------------------------------------------------------

.. code-block:: python

    process_manager.wait_till_all_processes_are_over(int_seconds_step=2)


.. image:: images/1.PNG


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
