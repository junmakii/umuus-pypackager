#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Jun Makii <junmakii@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''A simple packaging utility for Python.

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

    $ docker run -v $(pwd)/config:/app/config umuus-google-oauth:0.1 run \
      --credential_file "config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json" \
      --token_file "config/google/google_blogger_access_token.json" \
      --scope "$(cat config/google/google_blogger_scope.json)"

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

NOTE
----

    cp umuus_pypackager.py ~/workspace/lib/umuus-pypackager/umuus_pypackager/__init__.py

'''
# -- BaseImport --
import os
import sys
import json
import types
import typing
import ast
import datetime
import collections
import re
import pprint
import subprocess
import functools
import itertools
import shlex
import logging
logger = logging.getLogger(__name__)
# -- End BaseImport --
# -- Metadata --
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-pypackager'
__author__ = 'Jun Makii'
__author_username__ = 'junmakii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'fire',
    'yapf',
    'jinja2',
    'cookiecutter',
    'PyGithub',
    'autoflake',
]
__dependency_links__ = []
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {
    'console_scripts': ['umuus_pypackager = umuus_pypackager:main'],
    'gui_scripts': [],
}
__project_urls__ = {
    'Bug Tracker': 'https://github.com/junmakii/umuus-pypackager/issues',
    'Documentation': 'https://github.com/junmakii/umuus-pypackager/',
    'Source Code': 'https://github.com/junmakii/umuus-pypackager/',
}
__test_suite__ = 'umuus_pypackager'
__tests_require__ = ['pytest']
__setup_requires__ = ['pytest-runner']
__extras_require__ = {}
__package_data__ = {
    '': [],
    'umuus_pypackager': ['templates/umuus-bootstrap-template']
}
__python_requires__ = '>=3'
__include_package_data__ = True
__zip_safe__ = True
__static_files__ = {}
__extra_options__ = {
    'docker_image':
    'python:3.7-alpine',
    'docker_requires': [
        'ca-certificates',
        'python3',
        'python3-dev',
    ],
    'docker_commands': [],
    'docker_cmd': [],
    'docker_entrypoint': [
        # 'gunicorn',
        # '--bind', '0.0.0.0:443',
        # '--certfile', 'server.crf',
        # '--keyfile', 'server.key',
        # '{{ name }}:application',
    ],
}
# -- End Metadata --
# -- Extra --
umuus_pypackager = __import__(__name__)
# -- End Extra --
while True:
    try:
        import fire
        import jinja2
        import yapf.yapflib.yapf_api
        import github
        import cookiecutter
        break
    except ImportError:
        subprocess.call(
            'pip install -U {}'.format(' '.join(__install_requires__)),
            shell=True)


def ast_get_root_variables(
        module,  # type: _ast.Module
):  # type: collections.OrderedDict
    return collections.OrderedDict(
        [(re.sub('__', '', _.targets[0].id), ast.literal_eval(_.value))
         for _ in module.body
         if type(_) == ast.Assign and _.targets[0].id.startswith('__')
         and _.targets[0].id.endswith('__')
         # and _.targets[0].id in target_attributes
         ])


class Option(object):
    commit: bool = False
    push: bool = False
    pipenv: str = None
    install: bool = False
    test: bool = False
    cookiecutter: bool = False
    docker: bool = False
    docker_hub: bool = False
    msg: str = ''
    available_keywords: list = '''version
url
author
author_email
keywords
license
scripts
install_requires
dependency_links
classifiers
entry_points
project_urls
setup_requires
test_suite
tests_require
extras_require
package_data
python_requires
include_package_data
download_url
zip_safe'''.splitlines()
    # Example: __download_url__ = 'https://github.com/junmakii/{{ name|replace('_', '-') }}/archive/{{ name }}-0.1'
    year: int = datetime.datetime.utcnow().year
    file: str = None
    file_content: str = None
    file_name: str = None
    module_name: str = None
    package_name: str = None
    output_path: str = None
    output_dir: str = None
    docstring: str = None
    description: str = None
    setup_options: dict = {}
    setup_options_str: str = None
    package_dir: str = None
    git_dir: str = None
    ast_node: typing.Any = None
    readme_name: str = 'README.rst'
    readme_path: str = None
    setup_file_name: str = 'setup.py'
    github: typing.Any = None
    github_file: str = None
    github_file_data: dict = {}
    extra_options: dict = {}
    setup_template: str = '''
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
{{ setup_options_str }},
    cmdclass={"pytest": PyTest},
)

'''
    setup_code: str = None
    static_files: dict = {}
    default_static_files: dict = {
        # 'cookie': {
        #     'type': 'cookiecutter',
        #     'source': 'https://github.com/audreyr/cookiecutter-pypackage',
        # },
        'docs/source/conf.py': {
            'type':
            'file',
            'content':
            '''
project = '{{ package_name }}'
copyright = '{{ year }}, {{ author }}'
author = '{{ author }}'
version = '{{ version }}'
release = '{{ version }}'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None
html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = '{{ module_name }}doc'
latex_elements = {}
latex_documents = [
    (master_doc, 'A.tex', '{{ package_name}} Documentation',
     '{{ package_name}}', 'manual'),
]
man_pages = [
    (master_doc, '{{ module_name }}', '{{ package_name}} Documentation', [author], 1)
]
texinfo_documents = [
    (master_doc, '{{ package_name }}', '{{ package_name }} Documentation',
     author, '{{ module_name }}', 'One line description of project.',
     'Miscellaneous'),
]
epub_title = project
epub_exclude_files = ['search.html']
'''
        },
        'Chart.yaml': {
            'type':
            'file',
            'content':
            '''apiVersion: v1
description: "{{ description }}"
name: {{ module_name }}
version: {{ version }}''',
        },
        'values.yaml': {
            'type': 'file',
            'content': '''
'''
        },
        'templates/development.yaml': {
            'type':
            'file',
            'content':
            '''{% raw %}
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}-deployment
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
      - name: {{ .Chart.Name }}-container
        image: "{{ .Chart.Name }}:{{ .Chart.Version }}"
        ports:
        - containerPort: 80
        - containerPort: 443
---
apiVersion: v1
kind: Service
metadata:
  name: {{ .Chart.Name }}-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
  - port: 443
  selector:
    app: {{ .Chart.Name }}
{% endraw %}
'''
        },
        'Pipfile': {
            'type':
            'file',
            'content':
            '''
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]
{% for setup_require in setup_requires -%}
{%- set match = re.findall('(.*?)((>|<|=|\+)+)(.*)', setup_require) -%}
{%- if match %}
{{ match[0][0] }} = "{{ match[0][1] }}{{ match[0][3] }}"
{%- else %}
{{ setup_require }} = "*"
{%- endif -%}
{% endfor %}

[packages]
{% for install_require in install_requires -%}
{%- set match = re.findall('(.*?)((>|<|=|\+)+)(.*)', install_require) -%}
{%- if match %}
{{ match[0][0] }} = "{{ match[0][1] }}{{ match[0][3] }}"
{%- else %}
{{ install_require }} = "*"
{%- endif -%}
{% endfor %}

{% if python_requires %}
[requires]
python_version = "{{ python_requires.split('>')[-1].split('<')[-1].split('=')[-1].strip() }}"
{% endif %}
'''
        },
        'Dockerfile': {
            'type':
            'file',
            'content':
            '''FROM {{ extra_options.docker_image | default("python:3.7-alpine") }}
MAINTAINER {{ author }} <{{ author_email }}>
RUN apk update
RUN apk add --no-cache ca-certificates
RUN apk add --no-cache python3 python3-dev
RUN apk add --no-cache {{ extra_options.docker_requires | join(" ") }}
RUN python3 -m ensurepip
RUN pip3 install --upgrade --no-cache-dir pip setuptools
ADD . /app/
WORKDIR /app
RUN pip install -U .
{%- for docker_command in extra_options.docker_commands or [] -%}
{{ docker_command }}
{%- endfor %}
ENTRYPOINT {% if extra_options.docker_entrypoint %}{{ json.dumps(extra_options.docker_entrypoint) }}{% else %}["python", "-m", "{{ module_name }}"]{% endif %}
CMD {{ json.dumps(extra_options.docker_cmd or []) }}
'''
        },
        'LICENSE': {
            'type':
            'file',
            'content':
            '''
Copyright (C) {{ year }}  {{ author }} <{{ author_email }}>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
            along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
        },
        'setup.cfg': {
            'type': 'file',
            'content': '''
[aliases]
test=pytest
'''
        },
        'MANIFEST.in': {
            'type':
            'file',
            'content':
            '''
exclude *.txt
exclude MANIFEST.in
include README.rst
include requirements.txt
recursive-include * *
global-exclude __pycache__
global-exclude *.py[co]
'''
        },
        'pytest.ini': {
            'type': 'file',
            'content': '''
[tool:pytest]
addopts = --doctest-modules --verbose
''',
        },
        '.gitignore': {
            'type':
            'file',
            'content':
            '''
# SOURCE: https://github.com/github/gitignore/blob/master/Python.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
'''
        },
    }

    def __init__(self, **kwargs):
        self.static_files = dict(self.default_static_files,
                                 **kwargs.get('static_files', {}))
        self.__dict__.update(kwargs)
        self.__post_init__()

    def __post_init__(self):
        logger.info('__post_init__')
        self.file_content = open(self.file).read()
        self.file_name = self.file_name or os.path.basename(self.file)
        self.file_dir = os.path.dirname(self.file)
        self.module_name = self.module_name or self.file_name.split('.', 1)[0]
        self.package_name = self.package_name or self.module_name.replace(
            '_', '-')
        self.output_path = (self.output_path or os.path.join(
            self.output_dir, self.package_name))
        not os.path.exists(self.output_path) and os.makedirs(self.output_path)
        self.git_dir = os.path.join(self.output_path, '.git')
        self.package_dir = self.package_dir or os.path.join(
            self.output_path, self.module_name)
        not os.path.exists(self.package_dir) and os.makedirs(self.package_dir)

        self.ast_node = ast.parse(open(self.file).read())
        self.docstring = ast.get_docstring(self.ast_node)
        self.description = self.description or self.docstring.splitlines()[0]

        self.readme_path = os.path.join(self.output_path, self.readme_name)
        open(self.readme_path,
             'w').write('\n'.join(self.docstring.splitlines()[1:]))

        self.docstring_rst = '\n'.join(self.docstring.splitlines()[1:]) + '''

Table of Contents
-----------------
.. toctree::
   :maxdepth: 2
   :glob:

   *

'''
        self.doc_dir = os.path.join(self.output_path, 'docs/source')
        not os.path.exists(self.doc_dir) and os.makedirs(self.doc_dir)
        self.doc_index = os.path.join(self.doc_dir, 'index.rst')
        open(self.doc_index, 'w').write(self.docstring_rst)

        module_vars = ast_get_root_variables(self.ast_node)
        for key, value in module_vars.items():
            if key in self.available_keywords:
                self.setup_options[key] = value
            else:
                self.__dict__[key] = value
        self.static_files = dict(self.default_static_files,
                                 **self.static_files)
        # self.__dict__.update(self.setup_options)
        self.setup_options['name'] = self.package_name

        [
            subprocess.call([
                '/usr/bin/rsync', '-azq', path,
                (key and self.package_dir + '/' + key or self.output_path)
            ]) for key, paths in self.setup_options['package_data'].items()
            for path in paths
        ]
        self.setup_options['description'] = self.description
        self.setup_options['long_description'] = self.docstring
        self.static_files['requirements.txt'] = {
            'type': 'file',
            'content': '\n'.join(self.setup_options['install_requires'])
        }
        self.static_files['requirements_dev.txt'] = {
            'type': 'file',
            'content': '\n'.join(self.setup_options['tests_require'])
        }
        self.static_files[os.path.join(self.package_dir, '__main__.py')] = {
            'type':
            'file',
            'content':
            '''import sys
import {{ module_name }}

if __name__ == '__main__':
    {{ module_name }}.main(sys.argv)
''',
        }
        for key, value in self.static_files.items():
            if value['type'] == 'file':
                self.static_files[key]['content'] = jinja2.Template(
                    self.static_files[key]['content']).render(
                        json=json,
                        re=re,
                        **{
                            key: value
                            for key, value in (
                                [] + list(self.setup_options.items()) +
                                list(vars(self).items()) +
                                [('extra_options', self.extra_options)])
                        })
        self.setup_options_str = ',\n'.join([
            '    {}={}'.format(key, pprint.pformat(value))
            for key, value in self.setup_options.items()
        ])
        self.setup_path = os.path.join(self.output_path, self.setup_file_name)
        self.setup_code = jinja2.Template(
            self.setup_template).render(**vars(self))
        open(self.setup_path, 'w').write(self.setup_code)
        # self.render()
        logger.info('yapf.yapflib.yapf_api.FormatCode')
        self.init_file = os.path.join(self.package_dir, '__init__.py')
        open(self.init_file, 'w').write(
            yapf.yapflib.yapf_api.FormatCode(
                self.file_content, style_config='pep8')[0])
        subprocess.call(
            'autoflake --in-place --remove-unused-variables --remove-all-unused-imports {init_file}'
            .format(**vars(self)),
            shell=True)
        logger.info('yapf.yapflib.yapf_api.FormatCode:DONE')

    def run_create_static_files(self):
        logger.info(
            'run_create_static_files: %s' % str(self.static_files.keys()))
        for key, value in self.static_files.items():
            path = os.path.join(self.output_path, key)
            dir = os.path.dirname(path)
            not os.path.exists(dir) and os.makedirs(dir)
            if value['type'] == 'file':
                open(path, 'w').write(value['content'])
            elif value['type'] == 'copy':
                subprocess.call(
                    'cp -rfp {} {}'.format(
                        os.path.join(self.file_dir, value['source']), path),
                    shell=True)
        return self

    def run_install(self):
        exit_code = subprocess.call(
            'pip install -U {}'.format(self.output_path), shell=True)
        if exit_code != 0:
            sys.exit(exit_code)
        return self

    def run_cookiecutter(self):
        logger.info('run_cookiecutter')
        for key, value in self.static_files.items():
            if value['type'] == 'cookiecutter':
                command = '''
cd {output_path}
cookiecutter --no-input --overwrite-if-exists -o {output} {source}
'''.format(**dict(vars(self), output=key, source=value['source']))
                print(command)
                exit_code = subprocess.call(command, shell=True)
                if not exit_code != 0:
                    sys.exit(exit_code)

    def run_git_commit(self):
        if not os.path.exists(self.git_dir):
            subprocess.call(
                '''
cd {output_path}
git init
git remote add origin https://github.com/junmakii/{package_name}.git
'''.format(**vars(self)),
                shell=True)
        command = jinja2.Template('''
cd {{ output_path }}
git add -A .
{% if msg %}
git commit -m {{ json.dumps(msg) }}
{% else %}
git commit --allow-empty --allow-empty-message -m ''
{% endif %}
''').render(json=json, **vars(self))
        subprocess.call(command, shell=True)
        return self

    def run_git_push(self):
        subprocess.call(
            '''
cd {output_path}
git push origin master
'''.format(**vars(self)),
            shell=True)
        return self

    def run_docker_build(self):
        subprocess.call(
            '''
cd {output_path}
sudo docker build -t {author_username}/{package_name}:{version} .
'''.format(**dict(vars(self), **self.setup_options)),
            shell=True)
        return self

    def run_docker_push(self):
        subprocess.call(
            '''
cd {output_path}
sudo docker login --username {author_username}
sudo docker tag {package_name}:{version} {author_username}/{package_name}:{version}
sudo docker push {author_username}/{package_name}:{version}
'''.format(**dict(vars(self), **self.setup_options)),
            shell=True)
        return self

    def run_pipenv(self):
        subprocess.call(
            '''
cd {output_path}
PIPENV_PIPFILE={output_path}/Pipfile pipenv --python $(which python3) run python -m {module_name} {pipenv}
'''.format(**dict(vars(self), **self.setup_options)),
            shell=True)
        return self

    def run_git_create_repo(self):
        import github
        self.github_file_data = json.load(open(self.github_file))
        self.github = github.Github(
            self.github_file_data['user'],
            self.github_file_data['password'],
        )
        self.github_user = self.github.get_user()
        try:
            self.github_repo = self.github_user.get_repo(self.package_name)
        except Exception:
            self.github_repo = self.github_user.create_repo(
                self.package_name, self.description)
        return self

    def run_tests(self):
        exit_code = subprocess.call(
            '''
cd {output_path}
pytest --doctest-modules
'''.format(**vars(self)),
            shell=True)
        if exit_code != 0:
            sys.exit(exit_code)
        return self

    def render(self):
        self.template_context = {}
        matches = re.findall(r'(# <\+\+\+ (.*?) \+\+\+>)', self.file_content)
        for match in matches:
            self.template_context.update(json.loads(match[1]))
        matches = re.findall('(# <--- (.*?) --->)', self.file_content)
        self.template = jinja2.Environment(
            loader=jinja2.FileSystemLoader([os.path.dirname(self.file)]))
        for match in matches:
            self.file_content = self.file_content.replace(
                match[0],
                self.template.from_string(
                    match[1]).render(**self.template_context))
        return self


def run(**kwargs):  # type: None
    option = Option(**kwargs)
    option.run_create_static_files()
    if option.install:
        logger.info('option.install')
        option.run_install()
    if option.test:
        logger.info('option.test')
        option.run_tests()
    if option.commit:
        logger.info('option.commit')
        option.run_git_commit()
    if option.cookiecutter:
        option.run_cookiecutter()
    if option.docker:
        option.run_docker_build()
    if option.docker_hub:
        option.run_docker_push()
    if option.pipenv:
        option.run_pipenv()
    if option.push:
        logger.info('option.push')
        option.run_git_create_repo()
        option.run_git_push()
    return


def main(argv=[]):
    fire.Fire()
    return 0


if __name__ == '__main__':
    # logging.basicConfig(level='DEBUG')
    sys.exit(main())
