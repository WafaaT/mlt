#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

from mock import MagicMock
from test_utils.files import create_work_dir
from mlt.utils.process_helpers import run, run_popen
import uuid
import getpass
import inspect
import pytest
import sys
import os
import shutil


# enable test_utils to be used in tests via `from test_utils... import ...
sys.path.append(os.path.join(os.path.dirname(__file__), 'test_utils'))


MODULES = ('mlt.tests',)
MODULES_REPLACE = ('tests.unit', 'mlt')


def patch_setattr(module_names, module_replace, monkeypatch, path, m):
    """ Credit for this goes mostly to @megawidget
    do not call this directly -- assumes the fixture's caller is two stacks up
    and will correspondingly guess the module path to patch
    `path` can be:
        1. an object, if it's defined in the module you're testing
        2. a name, if it's imported in the module you're testing
        3. a full path a la traditional monkeypatch
    """
    if hasattr(path, '__module__'):
        monkeypatch.setattr('.'.join((path.__module__, path.__name__)), m)
        return
    elif any(path.startswith(i+'.') for i in module_names):
        # full path.  OK.
        monkeypatch.setattr(path, m)
    else:
        # assume we're patching stuff in the file the test file is supposed to
        # be testing
        fn = inspect.getouterframes(inspect.currentframe())[2][1]
        fn = os.path.splitext(os.path.relpath(fn))[0]
        module = fn.replace(os.path.sep, '.').replace('test_', '').replace(
            *module_replace)
        try:
            monkeypatch.setattr('.'.join((module, path)), m)
        except AttributeError:
            # handle mocking builtins like `open`
            if sys.version_info.major == 3:
                builtin = 'builtins'
            else:
                builtin = '__builtin__'
            # NOTE: `path` should be just the builtin, like `open`
            # usage: patch('open')
            monkeypatch.setattr("{}.{}".format(builtin, path), m)


@pytest.fixture
def patch(monkeypatch):
    """allows us to add easy autouse fixtures by patching anything we want
       Usage: return something like this in a @pytest.fixture
       - patch('files.fetch_action_arg', MagicMock(return_value='output'))
       Without the second arg, will default to just MagicMock()
    """
    def wrapper(path, mock=None):
        m = mock if mock is not None else MagicMock()
        patch_setattr(MODULES, MODULES_REPLACE, monkeypatch, path, m)
        return m

    return wrapper

@pytest.fixture
def session_setup_teardown():
    """ pytest setup and teardown."""
    with create_work_dir() as workdir:
        sess_setup = dict()
        sess_setup['workdir'] = workdir
        sess_setup['app_name'] = str(uuid.uuid4())[:10]
        sess_setup['namespace'] = getpass.getuser() + '-' \
                                  + sess_setup['app_name']

    yield sess_setup
    
    # remove directory when done
    shutil.rmtree(sess_setup['workdir'])
    # tear down remaining resources
    current_namespace = run_popen("kubectl get jobs --namespace={}".format(
        sess_setup['namespace']), shell=True).wait()
    if current_namespace != 0:
        run(["kubectl", "--namespace", sess_setup['namespace'],
             "delete", "-f", "k8s"])

