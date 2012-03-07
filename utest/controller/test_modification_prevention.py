import unittest
from robotide.controller.basecontroller import _BaseController
from robotide.controller.commands import _Command
from robotide.controller.filecontrollers import TestCaseFileController, ResourceFileController


class _Controller(_BaseController):

    modifiable = False

    def is_modifiable(self):
        return self.modifiable


class _ModifyingCommand(_Command):

    executed = False

    def execute(self, context):
        self.executed = True


class ModificationPreventionTestCase(unittest.TestCase):

    def setUp(self):
        self._command = _ModifyingCommand()
        self._controller = _Controller()

    def test_modification_prevented(self):
        self._execution_prevented()

    def test_modification_allowed(self):
        self._controller.modifiable = True
        self._execution_allowed()

    def test_nonmodifying_command_is_not_prevented(self):
        self._command.modifying = False
        self._execution_allowed()

    def test_nonmodifying_command_and_modifications_allowed(self):
        self._command.modifying = False
        self._controller.modifiable = True
        self._execution_allowed()

    def test_test_case_file_modifications_are_prevented_when_file_is_read_only(self):
        self._use_testcasefilecontroller()
        self._controller.is_readonly = lambda: True
        self._execution_prevented()

    def test_test_case_file_modifications_are_allowed_when_file_is_not_read_only(self):
        self._use_testcasefilecontroller()
        self._controller.is_readonly = lambda: False
        self._execution_allowed()

    def test_test_case_file_modifications_are_allowed_when_file_does_not_exist(self):
        self._use_testcasefilecontroller()
        self._controller.exists = lambda: False
        self._execution_allowed()

    def test_resource_file_modifications_are_prevented_when_file_is_read_only(self):
        self._use_resourcefilecontroller()
        self._controller.is_readonly = lambda: True
        self._execution_prevented()

    def test_resource_file_modifications_are_allowed_when_file_is_not_read_only(self):
        self._use_resourcefilecontroller()
        self._controller.is_readonly = lambda: False
        self._execution_allowed()

    def test_resource_file_modifications_are_allowed_when_file_does_not_exist(self):
        self._use_resourcefilecontroller()
        self._controller.exists = lambda: False
        self._execution_allowed()

    def _use_resourcefilecontroller(self):
        self._create_ctrl(ResourceFileController)

    def _use_testcasefilecontroller(self):
        self._create_ctrl(TestCaseFileController)

    def _create_ctrl(self, clazz):
        data = lambda:0
        data.source = ''
        data.directory = ''
        self._controller = clazz(data)
        self._controller.exists = lambda: True

    def _execution_prevented(self):
        self._controller.execute(self._command)
        self.assertFalse(self._command.executed)

    def _execution_allowed(self):
        self._controller.execute(self._command)
        self.assertTrue(self._command.executed)

if __name__ == '__main__':
    unittest.main()