import itertools
import re

import sys

from utils import load_yaml

REPLACE_REGEX = re.compile(r'{([^}]+)}')


def get_process_sorted_args(proc):
    cmd = proc['command']
    return REPLACE_REGEX.findall(cmd)


def get_cartesian_prod(process, usages):
    sorted_args = get_process_sorted_args(process)
    arrays = [usages[arg] for arg in sorted_args[::1]]
    return [list(i) for i in itertools.product(*arrays)]


def get_command(process, args):
    cmd = process['command']
    return re.sub(r'{[^{}]*}', '{}', cmd).format(*args)


def get_process(document, process_id):
    return next(process for process in document['processes'] if process['id'] == process_id)


def main():
    document = load_yaml(sys.argv[1])
    # pretty_print(document)

    tasks_map = {}

    for recipe in document['recipes']:
        for process in document['processes']:
            process_id = process['id']

            usages = recipe['uses'][process_id]
            cartesian_prod = get_cartesian_prod(process, usages)
            commands = [get_command(process, args) for args in cartesian_prod]

            for i, command in enumerate(commands):
                task = {
                    'command': command,
                    'recipe': recipe['id'],
                    'process': process_id,
                    'id': '%s-%s-%d' % (process_id, recipe['id'], i)
                }

                map_key = (task['process'], task['recipe'])
                tasks = tasks_map.get(map_key)
                if tasks:
                    tasks.append(task)
                else:
                    tasks_map[map_key] = [task]

    for recipe in document['recipes']:
        for process in document['processes']:
            process_deps_ids = process.get('deps') or []
            if not process_deps_ids:
                continue
            current_process_tasks = tasks_map.get((process['id'], recipe['id']))

            for process_dep_id in process_deps_ids:
                key = (process_dep_id, recipe['id'])
                tasks_deps = tasks_map.get(key)

                for current_process_task in current_process_tasks:
                    if not current_process_task.get('deps'):
                        current_process_task['deps'] = []
                    current_process_task['deps'].extend(map(lambda t: t['id'], tasks_deps))

    print('tasks:')
    for tasks in tasks_map.values():
        for task in tasks:
            print('  - id: %s' % (task['id']))
            print('    command: %s' % (task['command']))
            print('    deps: %s' % (task.get('deps') or []))


if __name__ == '__main__':
    main()
