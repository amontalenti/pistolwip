from wip import _get_pivotal_tracker, stories_by_user
from nose.tools import assert_equal, assert_not_equal, assert_true, \
        assert_false, assert_raises, assert_in, assert_is, assert_is_not, \
        assert_is_not_none, assert_sequence_equal, assert_set_equal, \
        assert_list_equal, assert_dict_equal, assert_items_equal

def test_connection():
    tracker = _get_pivotal_tracker()
    assert_is_not_none(tracker)
    i = 0
    try:
        for project in tracker.projects.all():
            i += 1
            pass
    except:
        assert_false(True, "no exceptions should occur while iterating projects in connection")
    assert_true(i > 0, "more than one project should exist")

def test_stories_by_user():
    stories = stories_by_user()
    assert_is_not_none(stories)
    assert_true(len(stories) > 0, "at least one story should exist in story map")
    

