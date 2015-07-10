Plugins
=======

Place your custom plugins in ~/.smolder_plugins.  They will be loaded in addition to the builtin plugins.

Smolder uses [yapsy](https://yapsy.readthedocs.org/en/latest/) for our plugin system.

Plugins are comprised of two files: a .yapsy-plugin config file and the plugin python file referenced in the .yapsy file.

The python file is comprised of a Plugin class and a _run_ method, which is expected to call pass_test or fail_test with the pass or failure message on the object it receives when it runs.

A plugin will only be run if the name of the plugin is listed as an outcome in [outcomes](outcomes.md)

Here is an example [plugin](../charcoal/response_redirect.py).
