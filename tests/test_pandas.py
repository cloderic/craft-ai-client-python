import unittest

from craft_ai.pandas import CRAFTAI_PANDAS_ENABLED

if CRAFTAI_PANDAS_ENABLED:
    import copy
    import pandas as pd

    from numpy.random import randn

    import craft_ai.pandas

    from .data import pandas_valid_data, valid_data
    from .utils import generate_entity_id
    from . import settings

    AGENT_ID = generate_entity_id("test_pandas_agent_1")
    AGENT_ID_2 = generate_entity_id("test_pandas_agent_2")
    GENERATOR_ID = generate_entity_id("test_pandas_generator")

    SIMPLE_AGENT_CONFIGURATION = pandas_valid_data.SIMPLE_AGENT_CONFIGURATION
    SIMPLE_AGENT_DATA = pandas_valid_data.SIMPLE_AGENT_DATA
    COMPLEX_AGENT_CONFIGURATION = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION
    COMPLEX_AGENT_CONFIGURATION_2 = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION_2
    COMPLEX_AGENT_DATA = pandas_valid_data.COMPLEX_AGENT_DATA
    COMPLEX_AGENT_DATA_2 = pandas_valid_data.COMPLEX_AGENT_DATA_2
    DATETIME_AGENT_CONFIGURATION = pandas_valid_data.DATETIME_AGENT_CONFIGURATION
    DATETIME_AGENT_DATA = pandas_valid_data.DATETIME_AGENT_DATA
    MISSING_AGENT_CONFIGURATION = pandas_valid_data.MISSING_AGENT_CONFIGURATION
    MISSING_AGENT_DATA = pandas_valid_data.MISSING_AGENT_DATA
    MISSING_AGENT_DATA_DECISION = pandas_valid_data.MISSING_AGENT_DATA_DECISION
    INVALID_PYTHON_IDENTIFIER_CONFIGURATION = (
        pandas_valid_data.INVALID_PYTHON_IDENTIFIER_CONFIGURATION
    )
    INVALID_PYTHON_IDENTIFIER_DATA = pandas_valid_data.INVALID_PYTHON_IDENTIFIER_DATA
    INVALID_PYTHON_IDENTIFIER_DECISION = (
        pandas_valid_data.INVALID_PYTHON_IDENTIFIER_DECISION
    )

    CLIENT = craft_ai.pandas.Client(settings.CRAFT_CFG)


class TestPandasSimpleAgent(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, AGENT_ID)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_add_agent_operations_df_bad_index(self):
        df = pd.DataFrame(randn(10, 5), columns=["a", "b", "c", "d", "e"])

        self.assertRaises(
            craft_ai.pandas.errors.CraftAiBadRequestError,
            CLIENT.add_agent_operations,
            AGENT_ID,
            df,
        )

    def test_add_agent_operations_df(self):
        CLIENT.add_agent_operations(AGENT_ID, SIMPLE_AGENT_DATA)
        agent = CLIENT.get_agent(AGENT_ID)
        self.assertEqual(
            agent["firstTimestamp"],
            SIMPLE_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            SIMPLE_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )

    def test_add_agent_operations_df_unexpected_property(self):
        df = pd.DataFrame(
            randn(300, 6),
            columns=["a", "b", "c", "d", "e", "f"],
            index=pd.date_range("20130101", periods=300, freq="T").tz_localize(
                "Europe/Paris"
            ),
        )

        self.assertRaises(
            craft_ai.pandas.errors.CraftAiBadRequestError,
            CLIENT.add_agent_operations,
            AGENT_ID,
            df,
        )


class TestPandasComplexAgent(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, AGENT_ID)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_add_agent_operations_df_complex_agent(self):
        CLIENT.add_agent_operations(AGENT_ID, COMPLEX_AGENT_DATA)
        agent = CLIENT.get_agent(AGENT_ID)
        self.assertEqual(
            agent["firstTimestamp"],
            COMPLEX_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )

    def test_add_agent_operations_df_without_tz(self):
        test_df = COMPLEX_AGENT_DATA.drop(columns="tz")
        CLIENT.add_agent_operations(AGENT_ID, test_df)
        agent = CLIENT.get_agent(AGENT_ID)
        self.assertEqual(
            agent["firstTimestamp"],
            COMPLEX_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )


class TestPandasMissingAgent(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(MISSING_AGENT_CONFIGURATION, AGENT_ID)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_add_agent_operations_df_missing_agent(self):
        CLIENT.add_agent_operations(AGENT_ID, MISSING_AGENT_DATA)
        agent = CLIENT.get_agent(AGENT_ID)
        self.assertEqual(
            agent["firstTimestamp"],
            MISSING_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            MISSING_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )


class TestPandasSimpleAgentWithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, SIMPLE_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_get_agent_operations_df(self):
        df = CLIENT.get_agent_operations(AGENT_ID)

        self.assertEqual(len(df), 300)
        self.assertEqual(len(df.dtypes), 5)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2013-01-01 04:59:00", tz="Europe/Paris"),
        )

    def test_get_agent_states_df(self):
        df = CLIENT.get_agent_states(AGENT_ID)

        self.assertEqual(len(df), 180)
        self.assertEqual(len(df.dtypes), 5)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2013-01-01 04:58:20", tz="Europe/Paris"),
        )

    def test_tree_visualization(self):
        tree1 = CLIENT.get_agent_decision_tree(
            AGENT_ID, DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        craft_ai.pandas.utils.create_tree_html(tree1, "", "constant", None, 500)

    def test_display_tree_raised_error(self):
        tree1 = CLIENT.get_agent_decision_tree(
            AGENT_ID, DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        self.assertRaises(
            craft_ai.pandas.errors.CraftAiError,
            craft_ai.pandas.utils.display_tree,
            tree1,
        )


class TestPandasSimpleAgentWithOperations(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_get_decision_tree_with_pdtimestamp(self):
        # test if we get the same decision tree
        decision_tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, pd.Timestamp(valid_data.VALID_TIMESTAMP, unit="s", tz="UTC")
        )
        ground_truth_decision_tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, valid_data.VALID_TIMESTAMP
        )
        self.assertIsInstance(decision_tree, dict)
        self.assertNotEqual(decision_tree.get("_version"), None)
        self.assertNotEqual(decision_tree.get("configuration"), None)
        self.assertNotEqual(decision_tree.get("trees"), None)
        self.assertEqual(decision_tree, ground_truth_decision_tree)


class TestPandasComplexAgentWithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, COMPLEX_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_get_agent_operations_df_complex_agent(self):
        df = CLIENT.get_agent_operations(AGENT_ID)

        self.assertEqual(
            df["b"].notnull().tolist(),
            [True, True, False, False, True, False, False, False, False, False],
        )

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 3)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2013-01-10 00:00:00", tz="Europe/Paris"),
        )

    def test_decide_from_contexts_df(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        test_df = COMPLEX_AGENT_DATA
        test_df_copy = test_df.copy(deep=True)
        df = CLIENT.decide_from_contexts_df(tree, test_df)

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 6)
        self.assertTrue(test_df.equals(test_df_copy))
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2013-01-10 00:00:00", tz="Europe/Paris"),
        )

        # Also works as before, with a plain context
        output = CLIENT.decide(tree, {"a": 1, "tz": "+02:00"})

        self.assertEqual(output["output"]["b"]["predicted_value"], "Pierre")

    def test_decide_from_contexts_df_zero_rows(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        test_df = COMPLEX_AGENT_DATA.iloc[:0, :]
        test_df_copy = test_df.copy(deep=True)
        df = CLIENT.decide_from_contexts_df(tree, test_df)

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(len(df), 0)
        self.assertTrue(test_df.equals(test_df_copy))


class TestPandasComplexAgent2WithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, COMPLEX_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_decide_from_contexts_df_null_decisions(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )

        test_df = pd.DataFrame(
            [["Jean-Pierre", "+02:00"], ["Paul"]],
            columns=["b", "tz"],
            index=pd.date_range("20130201", periods=2, freq="D").tz_localize(
                "Europe/Paris"
            ),
        )
        test_df_copy = test_df.copy(deep=True)

        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 2)
        self.assertTrue(test_df.equals(test_df_copy))

        self.assertTrue(pd.notnull(df["a_predicted_value"][0]))
        self.assertTrue(pd.notnull(df["a_predicted_value"][1]))


class TestPandasComplexAgent3WithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, COMPLEX_AGENT_DATA_2)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_decide_from_contexts_df_with_array(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, COMPLEX_AGENT_DATA_2.last_valid_index().value // 10 ** 9
        )

        test_df = pd.DataFrame(
            [["Jean-Pierre", "+02:00"], ["Paul"]],
            columns=["b", "tz"],
            index=pd.date_range("20130201", periods=2, freq="D").tz_localize(
                "Europe/Paris"
            ),
        )
        test_df_copy = test_df.copy(deep=True)

        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 2)
        self.assertTrue(test_df.equals(test_df_copy))
        self.assertTrue(pd.notnull(df["a_predicted_value"][0]))
        self.assertTrue(pd.notnull(df["a_predicted_value"][1]))


class TestPandasMissingAgentWithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(MISSING_AGENT_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, MISSING_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_decide_from_missing_contexts_df(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID, MISSING_AGENT_DATA.last_valid_index().value // 10 ** 9, "2"
        )

        df = CLIENT.decide_from_contexts_df(tree, MISSING_AGENT_DATA_DECISION)

        self.assertEqual(len(df), 2)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2013-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2013-01-02 00:00:00", tz="Europe/Paris"),
        )

        # Also works as before, with a context containing an optional value
        output = CLIENT.decide(tree, {"b": {}, "tz": "+02:00"})

        self.assertTrue(pd.notnull(output["output"]["a"]["predicted_value"]))

        # Also works as before, with a context containing a missing value
        output = CLIENT.decide(tree, {"b": None, "tz": "+02:00"})

        self.assertTrue(pd.notnull(output["output"]["a"]["predicted_value"]))


class TestPandasDatetimeAgentWithData(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(DATETIME_AGENT_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, DATETIME_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_datetime_states_df(self):
        df = CLIENT.get_agent_states(AGENT_ID)

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 4)
        self.assertEqual(df["myTimeOfDay"].tolist(), [2, 3, 6, 7, 4, 5, 14, 15, 16, 19])

    # This test is commented because of the current non-deterministic behavior of craft ai.
    # def test_datetime_decide_from_contexts_df(self):
    #   tree = CLIENT.get_agent_decision_tree(AGENT_ID,
    #                                   DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9)

    #   test_df = pd.DataFrame(
    #     [
    #       [1],
    #       [3],
    #       [7]
    #     ],
    #     columns=["a"],
    #     index=pd.date_range("20130101 00:00:00",
    #                         periods=3,
    #                         freq="H").tz_localize("Asia/Shanghai"))
    #   test_df_copy = test_df.copy(deep=True)

    #   df = CLIENT.decide_from_contexts_df(tree, test_df)
    #   self.assertEqual(len(df), 3)
    #   self.assertEqual(len(df.dtypes), 6)
    #   self.assertEqual(df["b_predicted_value"].tolist(), ["Pierre", "Paul", "Jacques"])
    #   self.assertTrue(test_df.equals(test_df_copy))


class TestPandasAgentWithInvalidIdentifier(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.create_agent(INVALID_PYTHON_IDENTIFIER_CONFIGURATION, AGENT_ID)
        CLIENT.add_agent_operations(AGENT_ID, INVALID_PYTHON_IDENTIFIER_DATA)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)

    def test_decide_from_python_invalid_identifier(self):
        tree = CLIENT.get_agent_decision_tree(
            AGENT_ID,
            INVALID_PYTHON_IDENTIFIER_DATA.last_valid_index().value // 10 ** 9,
            "2",
        )

        test_df = INVALID_PYTHON_IDENTIFIER_DECISION.copy(deep=True)
        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 3)
        self.assertEqual(len(df.dtypes), 8)


class TestPandasGeneratorWithOperation(unittest.TestCase):
    def setUp(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.delete_agent(AGENT_ID_2)
        CLIENT.delete_generator(GENERATOR_ID)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, AGENT_ID)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, AGENT_ID_2)
        CLIENT.add_agent_operations(AGENT_ID, valid_data.VALID_OPERATIONS_SET)
        CLIENT.add_agent_operations(AGENT_ID_2, valid_data.VALID_OPERATIONS_SET)
        generator_configuration = copy.deepcopy(
            valid_data.VALID_GENERATOR_CONFIGURATION
        )
        generator_configuration["filter"] = [AGENT_ID, AGENT_ID_2]
        CLIENT.create_generator(generator_configuration, GENERATOR_ID)

    def tearDown(self):
        CLIENT.delete_agent(AGENT_ID)
        CLIENT.delete_agent(AGENT_ID_2)
        CLIENT.delete_generator(GENERATOR_ID)

    def test_get_generator_decision_tree_with_pdtimestamp(self):
        # test if we get the same decision tree
        decision_tree = CLIENT.get_generator_decision_tree(
            GENERATOR_ID, pd.Timestamp(valid_data.VALID_TIMESTAMP, unit="s", tz="UTC")
        )
        ground_truth_decision_tree = CLIENT.get_generator_decision_tree(
            GENERATOR_ID, valid_data.VALID_TIMESTAMP
        )
        self.assertIsInstance(decision_tree, dict)
        self.assertNotEqual(decision_tree.get("_version"), None)
        self.assertNotEqual(decision_tree.get("configuration"), None)
        self.assertNotEqual(decision_tree.get("trees"), None)
        self.assertEqual(decision_tree, ground_truth_decision_tree)
