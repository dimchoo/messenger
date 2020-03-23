from functools import reduce

from settings import INSTALLED_MODULES


def get_server_actions():

    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_MODULES, []
    )

    sub_modules = reduce(
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules, []
    )

    action_names = reduce(
        lambda value, item: value + getattr(item, 'action_names', []),
        sub_modules, []
    )

    return {i.get('action'): i.get('controller') for i in action_names}


def get_action_controller(action_name, actions=None):
    action_names = actions or get_server_actions()
    return action_names.get(action_name)
