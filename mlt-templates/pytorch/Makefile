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

.PHONY: dependencies

all: main

main: main.py
	@echo "Should run linting and tests before submitting application"

build:
	docker pull pytorch/pytorch:v0.2
	docker tag pytorch/pytorch:v0.2 ${CONTAINER_NAME}

status:
	@kubectl get pods --namespace ${NAMESPACE} -o wide -a -l job-name=${JOB_NAME}