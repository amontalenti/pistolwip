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

def current_stories(project_name):
    """get current iteration stories"""
    tracker = _get_pivotal_tracker()
    for project in tracker.projects.all():
        if project.name == project_name:
            for story in stories_in_iteration(project.current_iteration_number):
                yield story

def stories_in_iteration(iteration_id):
    tracker = _get_pivotal_tracker()
    for project in tracker.projects.all():
        for iteration in project.iterations.all():
            if iteration.id == iteration_id:
                for story in iteration.stories:
                    yield story

def bulk_story_op(iteration_id, 
                  story_action,     
                  story_filter=lambda s: True, 
                  edit=False):
    """
    bulk edit stories in a single iteration.
    
    story_filter is a function that returns True if story should be edited

    story_action is a function that operates on each matched story

    if edit is True, then story is also saved after each iteration; useful for
    bulk edit operations where story_action chagnes the story
    """
    for story in stories_in_iteration(iteration_id):
        if story_filter(story):
            story_action(story)
            if edit:
                print "saving %r" % story.id
                story.save()
    return None

def duplicate_story(project_id, story_id):
    tracker = _get_pivotal_tracker()
    project = tracker.projects.get(project_id)
    story = project.stories.get(story_id)
    new = tracker.Story()
    copy_fields = (
        "name", "story_type", 
        "requested_by", "owned_by", 
        "description",
        "labels",
        "estimate"
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

def split_story(project_id, story_id):
    """splits a story into two stories, one kept in current iteration 
    and one scheduled for top of the backlog."""
    # 1. duplicate_story
    # 2. relocate duplicated story to top of backlog


if __name__ == "__main__":
    "tester"
    #duplicate_story(490731, 27490111)
    #current_stories()
    #for story in current_stories("Parse.ly"):
    #    print story.id, story.name
