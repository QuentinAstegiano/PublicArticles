import sys
import os


def find_specific_parent(pattern, current=None):
    if current is None:
        return find_specific_parent(pattern, os.path.dirname(__file__))
    else:
        splitted = current.split(os.sep)
        if pattern == splitted[-1]:
            return current
        else:
            if len(splitted) == 1:
                return None
            else:
                return find_specific_parent(pattern, os.sep.join(splitted[0:-1]))


def get_parent_sibling(parent, sibling_name):
    parent = find_specific_parent(parent)
    return os.sep.join([os.path.dirname(parent), sibling_name])


sys.path.append(get_parent_sibling("test", "main"))
