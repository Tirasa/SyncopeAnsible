import unittest
import json

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from unittest.mock import patch

from plugins.modules.syncope_user_handler import SyncopeUserHandler


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):  # pylint: disable=unused-argument
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):  # pylint: disable=unused-argument
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_succeeded_post(*args, **kwargs):
    return MockResponse([], 200)


def mock_failed_post(*args, **kwargs):
    return MockResponse([], 500)


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)  # pylint: disable=protected-access


class TestMyModule(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def set_default_args(self):
        return dict({
            'action': 'change status',
            'adminUser': 'admin',
            'adminPwd': 'pwd',
            'serverName': 'url',
            'syncopeUser': 'id',
            'newStatus': 'SUSPEND',
            'changeStatusOnSyncope': True
        })

    @patch('plugins.modules.syncope_user_handler.requests.post', side_effect=mock_succeeded_post)
    def test_change_status_success(self, mock_post):
        module_args = {}
        module_args.update(self.set_default_args())
        set_module_args(module_args)
        my_obj = SyncopeUserHandler()
        result = my_obj.change_user_status_rest_call()
        self.assertTrue(result['changed'])

    @patch('plugins.modules.syncope_user_handler.requests.post', side_effect=mock_failed_post)
    def test_change_status_failure(self, mock_post):
        module_args = {}
        module_args.update(self.set_default_args())
        set_module_args(module_args)
        my_obj = SyncopeUserHandler()
        result = my_obj.change_user_status_rest_call()
        self.assertFalse(result['changed'])
