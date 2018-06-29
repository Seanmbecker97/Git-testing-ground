"""Utilities for managing issues
"""

def issue_last_modified(issue, bot_username):
    dates = [issue.created_at]
    for event in issue.get_events():
        if (not event.actor) or (event.actor.login != bot_username):
            dates.append(event.created_at)
    for comment in issue.get_comments():
        if comment.user.login != bot_username:
            dates.append(comment.created_at)
    return max(dates)


def issue_warnings(issue, bot_username):
    dates = []
    for comment in issue.get_comments():
        if comment.user.login == bot_username:
            dates.append(comment.created_at)
    return dates


def issue_last_warning(issue, bot_username):
    dates = issue_warnings(issue, bot_username)
    if len(dates) > 0:
        return max(dates)
    else:
        return None


def issue_close(issue, config, days_inactive, label):
    body = config["messages"]["closing"].format(days_inactive=days_inactive)
    issue.create_comment(body)
    issue.add_to_labels(label)
    issue.edit(state='closed')


def issue_warning(issue, config, days_inactive, deadline):
    assignee = "@" + str(issue.assignee).split("\"")[1]
    body = config["messages"]["warning"].format(assignee=assignee, days_inactive=days_inactive, deadline=deadline)
    issue.create_comment(body)


def issue_should_process(issue, config):
    if config["ignore-users"] and issue.user.login in config["ignore-users"]:
        return True
    if config["ignore-labels"]:
        for label in issue.labels:
            if label.name in config["ignore-labels"]:
                return False
    return True
