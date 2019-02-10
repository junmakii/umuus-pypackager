
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        import sys
        import shlex
        import pytest
        errno = pytest.main(['--doctest-modules'])
        if errno != 0:
            raise Exception('An error occured during installution.')
        install.run(self)


setup(
    packages=setuptools.find_packages('.'),
    version='0.1',
    url='https://github.com/junmakii/umuus-pypackager',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['fire', 'yapf', 'jinja2', 'cookiecutter', 'PyGithub', 'autoflake'],
    dependency_links=[],
    classifiers=['Development Status :: 3 - Alpha',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
 'Natural Language :: English',
 'Programming Language :: Python',
 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': ['umuus_pypackager = umuus_pypackager:main'],
 'gui_scripts': []},
    project_urls={'Bug Tracker': 'https://github.com/junmakii/umuus-pypackager/issues',
 'Documentation': 'https://github.com/junmakii/umuus-pypackager/',
 'Source Code': 'https://github.com/junmakii/umuus-pypackager/'},
    test_suite='umuus_pypackager',
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    extras_require={},
    package_data={'': [], 'umuus_pypackager': ['templates/umuus-bootstrap-template']},
    python_requires='>=3',
    include_package_data=True,
    zip_safe=True,
    name='umuus-pypackager',
    description='A simple packaging utility for Python.',
    long_description=('A simple packaging utility for Python.\n'
 '\n'
 'umuus-pypackager\n'
 '================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install git+https://github.com/junmakii/umuus-pypackager.git\n'
 '\n'
 'Requiremnts\n'
 '-----------\n'
 '\n'
 '    $ apt-get install -y pandoc\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_pypackager\n'
 '\n'
 '    >>> import umuus_pypackager\n'
 '\n'
 '    $ python -m umuus_pypackager run --file FILE.py --output_dir OUTPUT_DIR '
 '--commit --push --install --test\n'
 '\n'
 '    $ docker run -v $(pwd)/config:/app/config umuus-google-oauth:0.1 '
 'run       --credential_file '
 '"config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json"       '
 '--token_file "config/google/google_blogger_access_token.json"       --scope '
 '"$(cat config/google/google_blogger_scope.json)"\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>\n'
 '\n'
 'NOTE\n'
 '----\n'
 '\n'
 '    cp umuus_pypackager.py '
 '~/workspace/lib/umuus-pypackager/umuus_pypackager/__init__.py'),
    cmdclass={"pytest": PyTest},
)