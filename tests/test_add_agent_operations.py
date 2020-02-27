import unittest

import copy
import craft_ai

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data

NB_OPERATIONS_TO_ADD = 2000


class TestAddOperationsSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting an agent with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = craft_ai.Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_add_agent_operations")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        self.client.delete_agent(self.agent_id)

    def test_add_agent_operations_with_correct_input(self):
        """add_agent_operations should succeed when given correct input data

        It should give a proper JSON response with a `message` fields being a
        string.
        """
        resp = self.client.add_agent_operations(
            self.agent_id, valid_data.VALID_OPERATIONS_SET
        )

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)

    def test_add_agent_operations_with_many_operations(self):
        """add_agent_operations should succeed when given lots of operations

        It should give a proper JSON response with a `message` fields being a
        string.
        """
        operations = copy.deepcopy(valid_data.VALID_OPERATIONS_SET[:])
        operation = operations[-1]
        timestamp = operation["timestamp"]
        length = len(operations)

        while length < NB_OPERATIONS_TO_ADD:
            operation["timestamp"] = timestamp + length
            operations.append(operation.copy())
            length = length + 1

        resp = self.client.add_agent_operations(
            self.agent_id,
            sorted(operations, key=lambda operation: operation["timestamp"]),
        )

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)


class TestAddOperationsFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent with bad
    input"""

    @classmethod
    def setUpClass(cls):
        cls.client = craft_ai.Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_add_agent_operations")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        self.client.delete_agent(self.agent_id)

    def test_add_agent_operations_with_invalid_agent_id(self):
        """add_agent_operations should fail when given a non-string/empty string ID

        It should raise an error upon request for operations posting
        for an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_OPERATIONS_SET,
            )

    def test_add_agent_operations_with_empty_operations_set(self):
        """add_agent_operations should fail when given an empty set of operations

        It should raise an error upon request for posting an empty set of
        operations to an agent's configuration.
        """
        for ops_set in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                self.agent_id,
                invalid_data.UNDEFINED_KEY[ops_set],
            )

    def test_add_agent_operations_with_invalid_operation_set(self):
        """add_agent_operations should fail when given an invalid set of operations

        It should raise an error upon request for posting an invalid set of
        operations to an agent's configuration.
        """
        for ops_set in invalid_data.INVALID_OPS_SET:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                self.agent_id,
                invalid_data.INVALID_OPS_SET[ops_set],
            )