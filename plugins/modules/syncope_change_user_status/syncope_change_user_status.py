#!/usr/bin/python

# Copyright (C) 2012-2013 Tirasa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
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
module: Syncope change user status

short_description: Module change status of a user on Apache Syncope

version_added: "2.4"

description:
    - "Module change status of a user on Apache Syncope"

options:
    name:
        description:
            - This is the message to send to the module. If passing 'fail me' the module will simply fail.
        required: false
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

author:
    - Matteo Alessandroni (@mat-ale)
'''

EXAMPLES = '''
# Suspend user
- name: Suspend user
  syncope_change_user_status:
    "name": ""
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "SUSPEND"

# Reactivate user
- name: Reactivate user
  syncope_change_user_status:
    "name": ""
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "REACTIVATE"

# Activate user
- name: Activate user
  syncope_change_user_status:
    "name": ""
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "ACTIVATE"

# Fail the module
- name: Test failure of the module
  syncope_change_user_status:
    "name": fail me
    "adminUser": "admin"
    "adminPwd": "password"
    "serverName": "https://syncope-vm.apache.org"
    "syncopeUser": "c9b2dec2-00a7-4855-97c0-d854842b4b24"
    "changeStatusOnSyncope": "true"
    "newStatus": "REACTIVATE"
'''

RETURN = '''
changed:
    description: The output response from the Apache Syncope endpoint
    type: str
    returned: always

message:
    description: To determine whether this module made any modifications to the target or not
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

# Custom libraries
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

def callApi(module):
    server_name = module.params['serverName']
    api_endpoint = "/syncope/rest/users/" + module.params['syncopeUser'] + "/status"
    url = server_name + api_endpoint

    headers = {'Accept':'application/json',
        'Content-Type':'application/json',
        'Prefer': 'return-content',
        'X-Syncope-Domain': 'Master'
        }
    payload = {
                "operation": "ADD_REPLACE",
                "value": "org.apache.syncope.common.lib.types.StatusPatchType",
                "onSyncope": module.params['changeStatusOnSyncope'],
                "key": module.params['syncopeUser'],
                "type": module.params['newStatus']
              }

    user = module.params['adminUser'] or 'admin'
    pwd = module.params['adminPwd'] or 'password'
    resp = open_url(url, method="POST", headers=headers, url_username=user,
        url_password=pwd, force_basic_auth=True, data=json.dumps(payload))

    resp_json = json.loads(resp.read())

    if resp_json is None or resp.status != 200:
        module.fail_json(msg="Error while changing status")

    return resp_json

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=False, default=""),
        adminUser=dict(type='str', required=True),
        adminPwd=dict(type='str', required=True),
        serverName=dict(type='str', required=True),
        syncopeUser=dict(type='str', required=True),
        newStatus=dict(type='str', required=True),
        changeStatusOnSyncope=dict(type='str', required=True)
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    result['message'] = callApi(module)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
