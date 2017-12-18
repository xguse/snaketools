#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide code supporting the running and automating of Snakemake rules."""

# Imports
from collections import OrderedDict
from pathlib import Path
import textwrap

import munch

from logzero import logger as log  # noqa: F401

from snaketools import errors as e


__all__ = ["apply_template", "pathify_by_key_ends", "SnakeRun", "SnakeRule", "recode_graph", "rewrite_snakefile_no_rules"]


class SnakeRun(object):
    """Initialize and manage information common to the whole run."""

    def __init__(self, cfg, snakefile):
        """Initialize common information for a run."""
        assert isinstance(cfg, dict)

        common = cfg["COMMON"]
        self.snakefile = snakefile
        self.globals = munch.Munch()
        self.cfg = cfg
        self.name = common["RUN_NAME"]
        try:
            self.interim_dir = common["INTERIM_DIR"]
        except KeyError:
            self.interim_dir = None
        self.out_dir = Path("{base_dir}/{run_name}".format(base_dir=common["OUT_DIR"],
                                                           run_name=self.name))
        self.pretty_names = {}
        self.log_dir = self.out_dir / "logs"

        self.rules = munch.Munch()



class SnakeRule(object):
    """Manage the initialization and deployment of rule-specific information."""

    def __init__(self, run, name, pretty_name=None):
        """Initialize logs, inputs, outputs, params, etc for a single rule."""
        assert isinstance(run, SnakeRun)

        if pretty_name is None:
            pretty_name = name

        self.run = run
        self.name = name.lower()
        self.pretty_name = pretty_name

        self.run.pretty_names[self.name] = pretty_name

        self.log_dir = run.log_dir / self.name
        self.log = self.log_dir / "{name}.log".format(name=self.name)
        self.out_dir = run.out_dir / self.name
        self.i = munch.Munch()  # inputs
        self.o = munch.Munch()  # outputs
        self.p = munch.Munch()  # params

        self.extra = munch.Munch()  # params

        self.run.rules[name] = self

        self._import_config_dict()

    def _import_config_dict(self):
        """Import configuration values set for this rule so they are directly accessable as attributes."""
        try:
            for key, val in self.run.cfg[self.name.upper()].items():
                self.__setattr__(key, val)
            self.cfg = True
        except KeyError:
            self.cfg = False


def apply_template(template, keywords):
    """Return a list of strings of form ``template`` with values in ``keywords`` inserted.

    Args:
        template (``str``): a string containing keywords (``{kw_name}``).
        keywords (``dict``-like): dict with keys of appropriate keyword names and values as equal length ORDERED lists
                                  with the correct values to be inserted.
    """
    # Check lengths of keywords
    list_lens = set([len(x) for x in keywords.values()])
    if len(list_lens) != 1:
        raise e.ValidationError("keywords dict must contain values of constant length.")

    formatted = []

    for i in range(len(list(keywords.values())[0])):
        args = {k: v[i] for k, v in keywords.items()}
        formatted.append(template.format(**args))

    return formatted


def pathify_this(key):
    """Return `True` if the value associated with this key should be pathified."""
    pathify_these = {"PATH",
                     "FILE",
                     "DIR"}
    return bool(key.split("_")[-1] in pathify_these)


def pathify_by_key_ends(dictionary):
    """Return a dict that has had all values with keys containing the suffixes: '_FILE', '_PATH' or '_DIR' converted to Path() instances.

    Args:
        dictionary (dict-like): Usually the loaded, processed config file as a `dict`.

    Returns:
        dict-like: Modified version of the input.
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            pathify_by_key_ends(value)
        elif key.endswith("_PATH") or key.endswith("_DIR"):
            dictionary[key] = Path(value)

    return dictionary


# DAG and rulegraph stuff
def digest_node_line(line):
    """Return OrderedDict of relevant line parts."""
    line = line.strip()

    d = OrderedDict()
    d["num"], fields = line.split('[')
    fields = fields.replace('rounded,dashed', 'rounded-dashed')
    fields = fields.rstrip('];').split(',')
    fields[-1] = fields[-1].replace('rounded-dashed', 'rounded,dashed')
    for field in fields:
        key, value = field.split('=')
        d[key.strip()] = value.strip().replace('"', '').replace("'", "")

    return d


def should_ignore_line(line, strings_to_ignore):
    """Return true if line contains a rule name in `rule_names`."""
    for string in strings_to_ignore:
        if string in line:
            return True

    return False


def recode_graph(dot, new_dot, pretty_names, rules_to_drop, color=None, use_pretty_names=True):
    """Change `dot` label info to pretty_names and alter styling."""
    if color is None:
        color = "#50D0FF"

    node_patterns_to_drop = []

    with open(dot, mode='r') as dot:
        with open(new_dot, mode='w') as new_dot:
            for line in dot:
                if '[label = "' in line:

                    # Add pretty names and single color IF pretty names are provided.
                    data = digest_node_line(line=line)
                    rule_name = data['label']

                    if use_pretty_names:
                        pretty_name = textwrap.fill(pretty_names[rule_name], width=40).replace('\n', '\\n')
                        full_name = "[{rule_name}]\\n{pretty_name}".format(rule_name=rule_name,
                                                                           pretty_name=pretty_name)
                        data['label'] = full_name
                        data['color'] = color
                    else:
                        pass

                    fields = ', '.join(['{k} = "{v}"'.format(k=k, v=v) for k, v in data.items()][1:])

                    if should_ignore_line(line, strings_to_ignore=rules_to_drop):
                        node_patterns_to_drop.append("\t{num} ->".format(num=data['num']))
                        node_patterns_to_drop.append("-> {num}\n".format(num=data['num']))
                        continue

                    new_line = """\t{num}[{fields}];\n""".format(num=data['num'], fields=fields)

                    new_dot.write(new_line)
                else:
                    if should_ignore_line(line, strings_to_ignore=node_patterns_to_drop):
                        continue
                    elif "fontname=sans" in line:
                        line = line.replace("fontname=sans", "fontname=Cantarell")
                        line = line.replace("fontsize=10", "fontsize=11")
                        new_dot.write(line)
                    else:
                        new_dot.write(line)


def rewrite_snakefile_no_rules(infile, outfile):
    """Write new file, omitting the snakemake grammar sections."""
    def rule_declaration(line):
        return line.startswith("rule")

    def startswith_indent(line):
        return line.startswith("    ")

    def get_line_after_rule(file):
        for line in file:
            if not startswith_indent(line):
                return line

    infile = Path(infile)
    outfile = Path(outfile)

    with outfile.open('w') as out, infile.open('r') as snek:

        for line in snek:
            if not rule_declaration(line):
                out.write(line)
            else:
                out.write(get_line_after_rule(line))