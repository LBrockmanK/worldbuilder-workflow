#!/usr/bin/env python3
"""Check that plugins are enabled for a session root. Reads only; writes nothing.

A plugin counts as enabled when the session root's effective selection (its
committed .claude/settings.json with .claude/settings.local.json merged over
it) enables it, or when the user-level settings enable it and the session root
does not disable it. No selection recorded at the session root still stops.

Usage: check_enablement.py --session-root <dir> [--user-settings <file>] <plugin>...
Exit 0: all enabled. Exit 1: a stop condition. Exit 2: unreadable settings file.
"""
import argparse
import json
import os
import sys


class SettingsError(Exception):
    pass


def load(path):
    """Return the settings object at path; {} when the file is absent."""
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding='utf-8-sig') as f:
            data = json.load(f)
    except (OSError, ValueError) as exc:
        raise SettingsError(f'{path}: not readable JSON ({exc})')
    if not isinstance(data, dict):
        raise SettingsError(f'{path}: not a JSON object')
    return data


def plugin_map(settings, path):
    plugins = settings.get('enabledPlugins')
    if plugins is None:
        return None
    if not isinstance(plugins, dict):
        raise SettingsError(f'{path}: enabledPlugins is not an object')
    return plugins


def values_for(plugins, name):
    return [v for k, v in plugins.items()
            if k.split('@', 1)[0] == name and isinstance(v, bool)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--session-root', required=True)
    ap.add_argument('--user-settings',
                    default=os.path.join(os.path.expanduser('~'), '.claude',
                                         'settings.json'))
    ap.add_argument('plugins', nargs='+', help='plugin names, no @marketplace')
    args = ap.parse_args(argv)

    claude_dir = os.path.join(args.session_root, '.claude')
    committed_path = os.path.join(claude_dir, 'settings.json')
    local_path = os.path.join(claude_dir, 'settings.local.json')
    try:
        committed = plugin_map(load(committed_path), committed_path)
        local = plugin_map(load(local_path), local_path) or {}
        user = plugin_map(load(args.user_settings), args.user_settings) or {}
    except SettingsError as exc:
        print(f'Settings file problem: {exc}. Fix or remove that file, then run again.')
        return 2

    if committed is None:
        print(f'No plugin selection is recorded at {args.session_root}. '
              f'Run fleet:setup at {args.session_root}.')
        return 1

    project = dict(committed)
    project.update(local)
    ok = True
    disabled = False
    for name in args.plugins:
        p_vals = values_for(project, name)
        u_vals = values_for(user, name)
        if False in p_vals:
            verdict, layer = 'disabled', 'project'
            disabled = True
        elif True in p_vals:
            verdict, layer = 'enabled', 'project'
        elif True in u_vals and False not in u_vals:
            verdict, layer = 'enabled', 'user'
        else:
            verdict, layer = 'missing', '-'
        if verdict != 'enabled':
            ok = False
        print(f'{name}\t{verdict}\t{layer}')
    if ok:
        return 0
    msg = (f'Not every plugin is enabled. Run fleet:setup at '
           f'{args.session_root} and enable the missing plugins.')
    if disabled:
        msg += (' A plugin is disabled at the session root: clear the disable '
                'through fleet:setup, never by editing settings by hand.')
    print(msg)
    return 1


if __name__ == '__main__':
    sys.exit(main())
