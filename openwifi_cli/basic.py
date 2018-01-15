""" auxiliry classes and functions for openwifi cli """

import json

import click
import requests

class JsonParsable(click.ParamType):
    """ represents a json type for click """

    name = 'json'

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except ValueError:
            self.fail('%s is not a valid json string.' % value, param, ctx)

def generate_show(group, path):
    """ generate and decorate a basic show action """

    @group.command()
    @click.pass_context
    @click.argument('uuids', nargs=-1, required=False)
    def show(ctx, uuids):
        """ show action """

        do_loop_requests(ctx, uuids, requests.get, path)

def generate_delete(group, path):
    """ generate and decorate a basic delete action """

    @group.command()
    @click.pass_context
    @click.argument('uuids', nargs=-1)
    def delete(ctx, uuids):
        """ delete action """

        do_loop_requests(ctx, uuids, requests.delete, path)

def do_loop_requests(ctx, uuids, req_func, path):
    """ do a request action over a list of inputs """

    jar = ctx.obj['cookies']
    server = ctx.obj['server']

    ctx.obj['result'] = []
    for uuid in uuids:
        nodes_request = req_func(server+path+'/'+uuid, cookies=jar)
        append_check_for_json(ctx.obj['result'], nodes_request)

    if not uuids:
        nodes_request = requests.get(server+path, cookies=jar)
        append_check_for_json(ctx.obj['result'], nodes_request)

    json_pretty_print(ctx.obj['result'])

def generate_basic_functions(group, path, options, has_mod=True):
    """ add basic actions to a group """

    generate_show(group, path)
    generate_delete(group, path)

    @group.command()
    @click.pass_context
    def add(ctx, **kwargs):
        """ add action """

        jar = ctx.obj['cookies']
        server = ctx.obj['server']

        nodes_request = requests.post(server+path, cookies=jar, json=kwargs)
        ctx.obj['result'] = get_json_if_possible(nodes_request)

        json_pretty_print(ctx.obj['result'])

    def decorate_with_options(func, ignore_prompt=False, prompt=True):
        """ decorate an action with parameters and options """

        for option in options:
            if isinstance(option, dict):
                option_name = option['name']

                try:
                    option_type = option['type']
                except KeyError:
                    option_type = str
                try:
                    if not ignore_prompt:
                        option_prompt = option['prompt']
                    else:
                        option_prompt = False
                except KeyError:
                    option_prompt = True

                func = click.option(option_name, prompt=option_prompt, type=option_type)(func)
            else:
                func = click.option(option, prompt=prompt)(func)
        return func

    decorate_with_options(add)

    if has_mod:
        @group.command()
        @click.pass_context
        @click.argument('ids', nargs=-1)
        def mod(ctx, ids, **kwargs):
            """ modify action """

            kwargs = dict(filter(lambda x: x[1] != None, kwargs.items()))
            jar = ctx.obj['cookies']
            server = ctx.obj['server']

            ctx.obj['result'] = []
            for cur_id in ids:
                nodes_request = requests.post(server+path+'/'+cur_id, cookies=jar, json=kwargs)
                append_check_for_json(ctx.obj['result'], nodes_request)

            json_pretty_print(ctx.obj['result'])

        decorate_with_options(mod, True, False)

def get_json_if_possible(request):
    """ returns request text as json if possible """
    try:
        return request.json()
    except json.decoder.JSONDecodeError:
        return request.text

def append_check_for_json(result, request):
    """ appends request text to result if possible """
    try:
        result.append(request.json())
    except json.decoder.JSONDecodeError:
        result.append(request.text)

def json_pretty_print(result):
    """ pretty print as json """
    result = json.dumps(result, sort_keys=True, indent=4)
    click.echo(result)
