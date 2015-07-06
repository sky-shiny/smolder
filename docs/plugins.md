Plugins
=======

Place your custom plugins in ~/.smolder_plugins.  They will be loaded in addition to the builtin plugins.

Smolder uses [yapsy](https://yapsy.readthedocs.org/en/latest/) for our plugin system.

Plugins are comprised of two files: a .yapsy-plugin config file and the plugin python file referenced in the .yapsy file.

The plugin python file is comprised of a Plugin class and a run method, which is expected to call req.pass_test or req.fail_test with the pass or failure message.

Here is an example [plugin](../charcoal/response_redirect.py.
