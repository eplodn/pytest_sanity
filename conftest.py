import pytest
import os
import sys
python_ver = sys.version_info

@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    print("\n*** Now in pytest_collection_modifyitems ***", flush=True)
    deselect_non_sanity(config, items)

@pytest.fixture(scope='session', autouse=True)
def env(request):
    #print("Now before yield", flush=True)
    yield
    #print("Now after yield", flush=True)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    print("\n*** Now in pytest_sessionfinish ***", flush=True)
    if python_ver.major == 3 and python_ver.minor >= 9:
        from _pytest.main import ExitCode
        EXIT_NOTESTSCOLLECTED = ExitCode.NO_TESTS_COLLECTED
        EXIT_OK = ExitCode.OK
    else:
        from _pytest.main import EXIT_NOTESTSCOLLECTED, EXIT_OK

    if exitstatus == EXIT_NOTESTSCOLLECTED:
        print("*** No tests were collected, declaring a success nonetheless. ***", flush=True)
        session.exitstatus = EXIT_OK

def deselect_non_sanity(config, items):
    if 'SANITY_ONLY' not in os.environ:
        print('*** SANITY_ONLY not found in env, proceeding as usual ***')
        return items

    keep, discard = [], []

    for item in items:
        to_keep = False
        for mark in item.iter_markers_with_node():
            _, mark_ = mark
            name = mark_.name
            print(f"*** processing mark {name}... ***")
            kwargs = mark_.kwargs
            sanity = kwargs.get('sanity', False)
            if sanity is True:
                print(f"*** Found sanity=True, keeping ***")
                to_keep = True
        if to_keep:
            keep.append(item)
        else:
            discard.append(item)
    print("Keep: ========" + "\n".join([x.nodeid for x in keep]) + " ======== ")
    print("Discard: ========" + "\n".join([x.nodeid for x in discard]) + " ======== ")

    items[:] = keep
    config.hook.pytest_deselected(items=discard)
    return items

