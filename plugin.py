from plugins import popquiz

def handle_plugin_request(plugin_name, data, session):
    if plugin_name == 'popquiz':
        popquiz.handle(data, session)
    else:
        raise Exception("Unsupported Plugin!")
