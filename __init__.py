try:
    from .fab_tool_action import fabtoolPluginAction
    fabtoolPluginAction().register()

except Exception as e:
    import os
    import traceback 

    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'fab_tool_reg.log')
    tb = ''.join(traceback.format_exception(None, e, e.__traceback__))

    with open(log_file, 'w') as f:
        f.write(tb)
