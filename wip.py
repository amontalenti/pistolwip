import pyvotal
from datetime import datetime
from collections import defaultdict
from logging import getLogger

from settings import PIVOTAL_TOKEN

log = getLogger("wip")

def _get_pivotal_tracker():
    tracker = pyvotal.PTracker(token=PIVOTAL_TOKEN)
    return tracker

def stories_by_user():
    """get stories for each user using the mywork: search"""
    tracker = _get_pivotal_tracker()
    stories = defaultdict(dict)
    for project in tracker.projects.all():
        for membership in project.memberships.all():
            initials = membership.person.initials
            for story in project.stories.all(mywork=initials):
                stories[initials][story.id] = vars(story)
                print "%s: #%s '%s'" % (initials, story.id, story.name)
    return dict(stories)

def current_stories():
    """get current iteration stories"""
    tracker = _get_pivotal_tracker()
    stories = defaultdict(dict)
    for project in tracker.projects.all():
        for iteration in project.iterations.all():
            # filter= parameter doesn't seem to work on iterations.all(), mismatch with
            # documentation. However, we can determine latest iterations using start/finish
            # TODO: fix pyvotal to support this
            print iteration.start, iteration.finish
    return dict(stories)

