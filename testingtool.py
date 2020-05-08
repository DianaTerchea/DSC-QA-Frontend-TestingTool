import json


if __name__ == '__main__':
    from TestingTool.testsuite import TestSuite
    from TestingTool.scenario import Scenario

    with open("TestingTool/tests/google_login.json", "r") as f:
        scenario = Scenario.from_json(f.read())
    result = scenario.run()
    if result.result:
        print("Scenario {} completed successfully!".format(scenario.name))
    else:
        print("Scenario {} failed, reason:\n{}".format(scenario.name, json.dumps(result.data, indent=2)))
