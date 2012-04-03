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

def duplicate_story(project_id, story_id):
    tracker = _get_pivotal_tracker()
    project = tracker.projects.get(project_id)
    story = project.stories.get(story_id)
    new = tracker.Story()
    copy_fields = (
        "name", "story_type", 
        "requested_by", "owned_by", 
        "description"
    )
    for field in copy_fields:
        setattr(new, field, getattr(story, field))
    new = project.stories.add(new)
    new.add_note("duplicated from https://www.pivotaltracker.com/story/show/%r" % story_id)
    # duplicate tasks
    for task in story.tasks.all():
        newtask = tracker.Task()
        newtask.description = task.description
        new.tasks.add(newtask)


if __name__ == "__main__":
    "tester"
    duplicate_story(490731, 27490111)
