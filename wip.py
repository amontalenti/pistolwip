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
    tracker = _get_pivotal_tracker()
    stories = defaultdict(dict)
    for project in tracker.projects.all():
        for membership in project.memberships.all():
            initials = membership.person.initials
            for story in project.stories.all(mywork=initials):
                print "%s: #%s '%s'" % (initials, story.id, story.name)
                stories[initials][story.id] = vars(story)
    return stories

