
Tests
=====

Multiple tests are organised into a list of objects in a yaml or json document.  

Each test is comprised of the following options:

Options | Description
-------------|------------
name \* | name for the test
uri \* | /url/path/to/resource.json
protocol | tcp, http, https or noop
port | 0 - 65535
method | GET, POST, PUT, DELETE, OPTION
[inputs.md](inputs) | Inputs accept all verbs that requests does, in the same format for convenience. See below for details.
[outcomes.md](outcomes) | Outcomes is a list of tests to run against the response. See below for details.

See these [examples.md](examples).

