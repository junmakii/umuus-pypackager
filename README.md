
A simple packaging utility for Python.

umuus-pypackager
================

Installation
------------

    $ pip install git+https://github.com/junmakii/umuus-pypackager.git

Requiremnts
-----------

    $ apt-get install -y pandoc

Example
-------

    $ umuus_pypackager

    >>> import umuus_pypackager

    $ python -m umuus_pypackager run --file FILE.py --output_dir OUTPUT_DIR --commit --push --install --test

    $ docker run -v $(pwd)/config:/app/config umuus-google-oauth:0.1 run       --credential_file "config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json"       --token_file "config/google/google_blogger_access_token.json"       --scope "$(cat config/google/google_blogger_scope.json)"

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

NOTE
----

    cp umuus_pypackager.py ~/workspace/lib/umuus-pypackager/umuus_pypackager/__init__.py