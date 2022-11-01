#!/usr/bin/env python
import io
import shlex
import subprocess
from multiprocessing.pool import ThreadPool

from colorama import Fore, Style
from flask import json
from pygments import highlight, lexers, formatters


def listen_stream(stream):
    output = ""
    with io.TextIOWrapper(stream, encoding="utf-8") as file:
        for line in file:
            if line != '':
                output += line
            else:
                break
    return output


def execute_task(task_info: dict) -> dict:
    shell_mode = task_info.get('shell')
    default_args = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE
    }

    # noinspection PySimplifyBooleanCheck
    if shell_mode == False:
        print(f'Running command: {Fore.GREEN}%s{Style.RESET_ALL} in %s mode' % (task_info["command"], "environment"))
        process = subprocess.Popen(shlex.split(task_info["command"]), shell=False, **default_args)
    else:
        print(f'Rqunning command: {Fore.GREEN}%s{Style.RESET_ALL} in %s mode' % (task_info["command"], "shell"))
        process = subprocess.Popen(task_info["command"], shell=True, **default_args)

    thread_pool = ThreadPool(processes=2)
    async_stdout_call = thread_pool.apply_async(listen_stream, args=(process.stdout,))
    async_stderr_call = thread_pool.apply_async(listen_stream, args=(process.stderr,))

    process.wait()

    task_output = {
        "requestedJSON": task_info,
        "return_code": process.poll(),
        "stdout": async_stdout_call.get(),
        "stderr": async_stderr_call.get()
    }

    output_formatted = json.dumps(task_output, sort_keys=True, indent=2)
    colorful_json = highlight(output_formatted, lexers.JsonLexer(), formatters.TerminalFormatter())
    print("Output:", colorful_json)

    return task_output
