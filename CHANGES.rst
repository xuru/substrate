Changes
-------

* **Pre 0.3** (Development Version) -- Not released

  * Updated `WebTest`_ to version 1.3.1
  * Added ``assertUnauthorized`` to ``WebTest``
  * Implemented ``get_tasks`` and ``assertTasksInQueue``
  * Added ``delete()`` method to ``agar.test.web_test.WebTest``

  * `agar`_ changes:

    * `agar.auth`_

      * **Breaking Changes**
      
        * Changed `authentication_required`_ decorator to **not** `abort`_ with status ``403`` if the
          `authenticate function`_ returns ``None``. Instead, the decorator will simply set the request ``user`` attribute
          (or any `re-configured property`_) to ``None``. This is useful for handlers where authentication is optional.
          Users will have to update their `authenticate function`_ to `abort`_ if they still wish to keep the
          previous behavior.

        * The `authenticate function`_ will be passed the current `RequestHandler`_ rather than the
          `Request`_. The `Request`_ can still be accessed from the `RequestHandler`_ via ``handler.request``.

        * The `AuthConfig`_ configuration ``authenticate`` has been renamed to `DEFAULT_AUTHENTICATE_FUNCTION`_.
        
      * Updated default `authenticate function`_ to retain ``403`` behavior out of the box.

* **0.2** (First Public Release) -- 2011-10-14

  * Updated docs

* **0.1** (Development Version Only) -- 2011-09-21


.. Links

.. _abort: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.abort
.. _Request: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.Request
.. _RequestHandler: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.RequestHandler

.. _WebTest: http://webtest.pythonpaste.org/

.. _agar: http://packages.python.org/substrate/agar.html
.. _agar.auth: http://packages.python.org/substrate/agar.html#module-agar.auth
.. _AuthConfig: http://packages.python.org/substrate/agar.html#agar.auth.AuthConfig
.. _authentication_required: http://packages.python.org/substrate/agar.html#agar.auth.authentication_required
.. _authenticate function: http://packages.python.org/substrate/agar.html#agar.auth.AuthConfig.authenticate
.. _re-configured property: http://packages.python.org/substrate/agar.html#agar.auth.AuthConfig.AUTHENTICATION_PROPERTY
.. _DEFAULT_AUTHENTICATE_FUNCTION: http://packages.python.org/substrate/agar.html#agar.auth.AuthConfig.DEFAULT_AUTHENTICATE_FUNCTION
