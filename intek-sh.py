#!/usr/bin/env python3
import os
import sys
import string
import subprocess
from argparse import ArgumentParser


def export_command(inputs):
    ascii = string.ascii_lowercase + string.ascii_uppercase
    if len(inputs) == 1:
        pass
    else:
        arguments = inputs[1:]
        for argument in arguments:
            if '=' in argument:
                argument_list = argument.split('=')
                if not argument_list[0]:
                    pass
                else:
                    os.environ[argument_list[0]] = argument_list[1]
            else:
                os.environ[argument] = ""


def printenv_command(inputs):
    if len(inputs) == 1:
        for key in os.environ:
            print(key + '=' + os.environ[key])
    else:
        argument = inputs[1]
        try:
            print(os.environ[argument])
        except KeyError:
            pass


def cd_command(inputs):
    if len(inputs) == 1:
        try:
            os.chdir(os.environ['HOME'])
        except KeyError:
            print('intek-sh: cd: HOME not set')
    else:
        argument = inputs[1]
        current_location = os.getcwd()
        father_dir = os.path.dirname(os.getcwd())
        if not argument:
            os.chdir(os.environ['HOME'])
        elif argument == '.':
            pass
        elif argument == '..':
            os.chdir(os.path.abspath(father_dir))
        else:
            path = current_location + '/' + argument
            if not os.path.exists(path):
                print('intek-sh: cd: ' + argument +
                      ': No such file or directory')
            elif os.path.isfile(path):
                print('intek-sh: cd: ' + argument +
                      ': Not a directory')
            else:
                os.chdir(path)


def unset_command(inputs):
    if len(inputs) == 1:
        pass
    else:
        argument = inputs[1]
        try:
            if argument in os.environ:
                del os.environ[argument]
            else:
                pass
        except Exception:
            print('intek-sh: unset: ' + argument +
                  ': cannot unset: readonly variable')


def exit_command(inputs):
    print('exit')
    if len(inputs) == 2 and not inputs[1].isdigit():
        print('intek-sh: exit:')


def get_command_list():
    command_list = []
    try:
        source = os.environ['PATH']
        source = source.split(':')
        for item in source:
            if os.path.exists(item):
                app_list = os.listdir(item)
                if app_list:
                    for app in app_list:
                        command_list.append(app)
    except KeyError:
        pass
    return command_list


def execution_builtins(command, inputs):
    if command == 'exit':
        exit_command(inputs)
    elif command == 'unset':
        unset_command(inputs)
    elif command == 'cd':
        cd_command(inputs)
    elif command == 'printenv':
        printenv_command(inputs)
    elif command == 'export':
        export_command(inputs)


def execution_external(command, inputs, command_list):
    if command in command_list:
            subprocess.run(inputs)
    elif './' in command:
        files = os.listdir(os.getcwd())
        if command[2:] not in files:
            print('intek-sh: ' + command + ': No such file or directory')
        else:
            try:
                subprocess.run(inputs)
            except PermissionError:
                print('intek-sh: ' + command + ': Permission denied')
    else:
        print('intek-sh: ' + command + ': command not found')


def command_loop():
    global builtins_list
    while True:
        try:
            command_list = get_command_list()
            inputs = input('intek-sh$ ')
            raw_inputs = inputs.strip().split(' ')
            inputs = []
            for item in raw_inputs:
                if item:
                    inputs.append(item)
            if not inputs:
                pass
            else:
                command = inputs[0]
                if 'exit' in inputs:
                    execution_builtins(command, inputs)
                    break
                else:
                    if not command:
                        pass
                    if command in builtins_list:
                        execution_builtins(command, inputs)
                    else:
                        execution_external(command, inputs, command_list)
        except EOFError:
            break


if __name__ == '__main__':
    builtins_list = ['cd', 'printenv', 'export', 'unset', 'exit']
    command_loop()
