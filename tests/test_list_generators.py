import unittest

import craftai

from . import settings
from .data import valid_data

class TestListGenerators(unittest.TestCase):
  """Checks that the client succeeds when getting an agent with OK input"""
  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)
    cls.n_generators = 5
    cls.generators_id = ["{}_{}_{}".format(valid_data.VALID_ID, i, settings.RUN_ID)
                         for i in range(cls.n_generators)]
    cls.agent_id = valid_data.VALID_ID

  def setUp(self):
    self.client.delete_agent(valid_data.VALID_ID)
    self.client.create_agent(valid_data.VALID_GENERATOR_CONFIGURATION, self.agent_id)
    for generators_id in self.generators_id:
      self.client.delete_generator(generators_id)
      self.client.create_generator(
        valid_data.VALID_GENERATOR_CONFIGURATION,
        valid_data.VALID_GENERATOR_FILTER,
        generators_id)

  def tearDown(self):
    # Makes sure that no generator with the standard ID remains
    for generator_id in self.generators_id:
      self.client.delete_generator(generator_id)

  def test_list_generators(self):
    """list_generators should returns the list of generators in the current project."""
    generators_list = self.client.list_generators()
    self.assertIsInstance(generators_list, list)
    for generator_id in self.generators_id:
      self.assertTrue(generator_id in generators_list)
