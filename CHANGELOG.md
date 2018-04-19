# Changelog #

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/craft-ai/craft-ai-client-python/compare/v1.11.0...HEAD) ##
### Added ###

- Introducing `reduce_decision_rules` (available through `from craftai import reduce_decision_rules`) a function that reduces a list of decision rules to a single rule per property.
- Introducing `format_property`, `format_decision_rules` (available through `from craftai import format_property, format_decision_rule, format_decision_rules`) respectively able to nicely format a property value, or several decision rules into a human readable string.

## [1.11.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.10.0...v1.11.0) - 2018-04-13 ##
### Changed ###

- It is no longer possible to compute a tree at a future timestamp, tests have been adapted to reflect that.
- tz-naive DatetimeIndex are no longer supported, from now it must be tz-aware.
- For learning (add_operations), you must provide a timezone column is order to generate features (time_of_day, ...).
- For decisions, you can provide a timezone column (multiple timezones supported). Otherwise, craft will use the datetimeindex tz.

### Fixed ###

- Fix an error occurring in the pandas client when the provided DataFrame included non-scalar values.
- The decoding of the craft ai JWT token is now resilient to spaces around the token string.
- Timezone are now used to generate features and to compute decisions.
- Fix a bug when the decisions_df was empty.

## [1.10.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.9.0...v1.10.0) - 2018-02-14 ##
### Fixed ###

- `client.decide` now properly handles _advanced_ property types such as `periodic`.

## [1.9.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.8.0...v1.9.0) - 2017-11-06 ##
### Added ###

- `client.get_decision_tree` now transparently retries computation up to the given `cfg.decisionTreeRetrievalTimeout`.

### Fixed ###

- `client.get_decision_tree` now properly returns timeout sent by the API as `errors.CraftAiLongRequestTimeOutError`.

## [1.8.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.7.1...v1.8.0) - 2017-10-24 ##
### Added ###
- Support new format for timezone offsets: +/-hhmm, +/-hh and some abbreviations(CEST, PST, ...). Check the [documentation](https://beta.craft.ai/doc/http#context-properties-types) for the complete list.

## [1.7.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.7.0...v1.7.1) - 2017-10-13 ##
### Added ###
- Add new function `client.get_state_history` retrieving a agent's state history. Take a look a the [documentation](https://beta.craft.ai/doc/python#retrieve-state-history) for further informations. This function is also available in the _pandas_ version.

### Fixed ###
- Fix the interpreter error messages to fit the [test suite](https://github.com/craft-ai/craft-ai-interpreter-test-suite) expectations.

## [1.7.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.6.0...v1.7.0) - 2017-10-13 ##

## [1.6.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.5.0...v1.6.0) - 2017-08-22 ##
### Added ###
- `client.get_operations_list` takes two new optional parameters defining time bounds for the desired operations.

### Changed ###
- `client.get_operations_list` handles the pagination automatically, making as many requests as necessary to the API.

## [1.5.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.4.1...v1.5.0) - 2017-08-02 ##
### Added ###
- Finally adding a changelog file (yes this one).
- Adding a helper script to maintain the changelog.
- Checking agent name at the agent creation to prevent erroneous behavior with the api route.

## [1.4.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.4.0...v1.4.1) - 2017-07-19 ##
### Changed ###
- The _pandas_ version of the decision operation no longer raises `CraftAiNullDecisionError`, it instead returns such errors in a specific column of the returned `DataFrame`.
- Now enforcing the usage of double-quotes in the code.

## [1.4.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.3.1...v1.4.0) - 2017-07-13 ##
### Added ###
- The decision operation now raises a specific error, `CraftAiNullDecisionError`, when a tree can't predict any value for a given context.

## [1.3.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.3.0...v1.3.1) - 2017-07-10 ##
### Fixed ###
- The distributed package now actually includes `craftai.pandas`.

## [1.3.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.3...v1.3.0) - 2017-07-09 ##
### Added ###
- New specialized version of the library that understands [Pandas](https://pandas.pydata.org) `DataFrame`, this specialized version of the client can be imported as such: `import Client from craftai.pandas`.

### Changed ###
- Simplifying the import scheme, it is now possible to import the client class with `import Client from craftai`; the previous behavior still works.

## [1.2.3](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.2...v1.2.3) - 2017-06-06 ##
### Fixed ###
- Deactivating some tests on agent creation failure to overcome a temporary regression on the API side.

## [1.2.2](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.1...v1.2.2) - 2017-06-06 ##
### Fixed ###
- `client.add_operations` now returns a proper count of the added operations in every cases.

## [1.2.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.0...v1.2.1) - 2017-04-13 ##
### Fixed ###
- The decision now properly takes into account that `day_of_week` belongs to [0,6] and not [1,7].

## [1.2.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.1.0...v1.2.0) - 2017-04-13 ##
### Added ###
- Automated linting of the code using [pylint](https://www.pylint.org).
- Introducing a script to automatically update the version from `craftai/__init__.py`.
- Simplifying the build scripts using `make`.

## [1.1.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.0.1...v1.1.0) - 2017-04-04 ##
### Added ###
- Client creation now extracts the right API url, the `owner` and the `project` from the given `token`.

### Changed ###
- Improve the `README.rst` generation to have a beautiful :lipstick: page on PyPI.
- Unifying the case of the error classes.

## [1.0.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.0.1...v1.0.0) - 2017-03-23 ##
_no changes_

## 1.0.0 - 2017-03-22 ##
- Initial **final** version of the Python client.
