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
import os
import pytest
import uuid
import getpass
from mlt.utils.process_helpers import run
from test_utils.e2e_commands import CommandTester
from test_utils.files import create_work_dir


# Expose the namespace value per test to be used in tearing down 
# the remaining resources, important to have in case tests fail.
def app_parameters(workdir):
    # setup the test session parameters
    app_name = str(uuid.uuid4())[:10]
    app_params = {
        'app_name': app_name,
        'workdir': workdir,
        'namespace': getpass.getuser() + '-' + app_name
    }
    return app_params

# tear down remaining resources
def sess_teardown(namespace):
    try:
        run(["kubectl", "--namespace", namespace, "delete", "-f", "k8s"])
    except SystemExit:
    #this means that the namespace and k8s resources are already deleted 
        pass


# NOTE: you need to deploy first before you deploy with --no-push
# otherwise you have no image to use to make new container from

@pytest.mark.parametrize('template',
                         filter(lambda x: os.path.isdir(
                             os.path.join('mlt-templates', x)),
                             os.listdir('mlt-templates')))
def test_simple_deploy(template):
    with create_work_dir() as workdir:
        app_params = app_parameters(workdir)
        commands = CommandTester(app_params)
        commands.init(template)
        commands.build()
        commands.deploy()
        commands.undeploy()
        sess_teardown(app_params['namespace'])


def test_no_push_deploy():
    with create_work_dir() as workdir:
        app_params = app_parameters(workdir)
        commands = CommandTester(app_params)
        commands.init()
        commands.build()
        commands.deploy()
        commands.deploy(no_push=True)
        commands.undeploy()
        sess_teardown(app_params['namespace'])


def test_watch_build_and_deploy_no_push():
    with create_work_dir() as workdir:
        app_params = app_parameters(workdir)
        commands = CommandTester(app_params)
        commands.init()
        commands.build(watch=True)
        commands.deploy()
        commands.deploy(no_push=True)
        commands.undeploy()
        sess_teardown(app_params['namespace'])

