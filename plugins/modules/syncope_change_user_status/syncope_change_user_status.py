#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_test

short_description: This is my test module

version_added: "2.4"

description:
    - "This is my longer description explaining my test module"

options:
    name:
        description:
            - This is the message to send to the test module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
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
                "onSyncope": "true",
                "key": module.params['syncopeUser'],
                "type": module.params['newStatus']
              }

    user = module.params['adminUser'] or 'admin'
    pwd = module.params['adminPwd'] or 'password'
    resp = open_url(url, method="POST", headers=headers, url_username=user,
        url_password=pwd, force_basic_auth=True, data=json.dumps(payload))

    resp_json = json.loads(resp.read())
    print(resp_json)

    if resp_json is None or resp.status != 200:
        module.fail_json(msg="Error %s" % env_name)

    return resp_json

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        adminUser=dict(type='str', required=True),
        adminPwd=dict(type='str', required=True),
        serverName=dict(type='str', required=True),
        syncopeUser=dict(type='str', required=True),
        newStatus=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        result=''
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

    result['result'] = callApi(module)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
