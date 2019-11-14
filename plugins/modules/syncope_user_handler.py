#!/usr/bin/python

# Copyright (C) 2019 Tirasa (info@tirasa.net)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Tirasa S.r.l.'
}

DOCUMENTATION = '''
---
modules: Syncope change user status
short_description: Module change status of a user on Apache Syncope
version_added: "2.4"
description:
    - "Module change status of a user on Apache Syncope"
options:
    action:
        description:
            - This is the message to send to the modules. 
              If passing 'change status' the module will change the user status.
        required: true
    adminUser:
        description:
            - Username of the Admin User to login to Syncope
        required: true
    adminPwd:
        description:
            - Password of the Admin User to login to Syncope
        required: true
    serverName:
        description:
             - Domain url of the Syncope instance
        required: true
    syncopeUser:
            description:
                 - Key of the user on Syncope whose status will be updated
            required: true
    changeStatusOnSyncope:
            description:
                 - In case the status update must be executed on Syncope too ('true') or
                   only to the resources linked to the user, if any ('false')
            required: true
    newStatus:
            description:
                 - Value of the new status (REACTIVATE | ACTIVATE | SUSPEND)
            required: true
extends_documentation_fragment:
authors:
    - Matteo Alessandroni (@mat-ale)
    - Federico Palmitesta (@FedericoPalmitesta)
'''

EXAMPLES = '''
# Suspend user
- name: Suspend user
  syncope_change_user_status:
    "action": "change status"
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "SUSPEND"
# Reactivate user
- name: Reactivate user
  syncope_change_user_status:
    "action": "change status"
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "REACTIVATE"
# Activate user
- name: Activate user
  syncope_change_user_status:
    "action": "change status"
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "ACTIVATE"
'''

RETURN = '''
changed:
    description: The output response from the Apache Syncope endpoint
    type: str
    returned: always
message:
    description: To determine whether this modules made any modifications to the target or not
    type: bool
    returned: always
'''

import requests

# Custom libraries
from ansible.module_utils.basic import *


class SyncopeUserHandler(object):

    def __init__(self):
        self.argument_spec = dict(
            action=dict(type='str', choices=['change status'], required=True),
            adminUser=dict(type='str', required=True),
            adminPwd=dict(type='str', required=True),
            serverName=dict(type='str', required=True),
            syncopeUser=dict(type='str', required=True),
            newStatus=dict(type='str', choices=['SUSPEND', 'ACTIVATE', 'REACTIVATE'], required=True),
            changeStatusOnSyncope=dict(type='str', required=True)
        )

        self.module = AnsibleModule(
            argument_spec=self.argument_spec
        )

    def change_user_status_rest_call(self):
        server_name = self.module.params['serverName']
        api_endpoint = "/syncope/rest/users/" + self.module.params['syncopeUser'] + "/status"
        url = server_name + api_endpoint

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'Prefer': 'return-content',
                   'X-Syncope-Domain': 'Master'
                   }
        payload = {
            "operation": "ADD_REPLACE",
            "value": "org.apache.syncope.common.lib.types.StatusPatchType",
            "onSyncope": self.module.params['changeStatusOnSyncope'],
            "key": self.module.params['syncopeUser'],
            "type": self.module.params['newStatus']
        }

        user = self.module.params['adminUser'] or 'admin'
        password = self.module.params['adminPwd'] or 'password'

        # seed the result dict in the object
        result = dict(
            changed=False,
            message=''
        )

        try:
            resp = requests.post(url, headers=headers, auth=(user, password), data=json.dumps(payload))
            resp_json = resp.json()

            if resp_json is None or resp is None or resp.status_code != 200:
                result['message'] = "Error while changing status"
                return result
        except Exception as e:
            res = json.load(e)
            self.module.fail_json(msg=res)

        result['message'] = resp_json

        # use whatever logic you need to determine whether or not this modules
        # made any modifications to your target
        result['changed'] = True

        # in the event of a successful modules execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        return result

    def apply(self):
        # during the execution of the modules, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        if self.module.params['action'] == 'change status':
            result = self.change_user_status_rest_call()
            if result['changed']:
                self.module.exit_json(**result)
            else:
                self.module.fail_json(msg=result['message'])
        else:
            self.module.fail_json(msg='The provided action is not supported')


def main():
    change_status = SyncopeUserHandler()
    change_status.apply()


if __name__ == '__main__':
    main()
