
Tests
=====

Multiple tests are organised into a list of objects in a yaml or json document.  

Each test is comprised of the following options:

Options | Description | Defaults
--------|-------------|---------
name \* | name for the test | None
uri \* | /url/path/to/resource.json | None
protocol | tcp, http, https or noop | http
port | 0 - 65535 | 80
method | GET, POST, PUT, DELETE, OPTION | GET
[inputs](inputs.md) | Inputs accept all verbs that requests does, in the same format for convenience. See below for details. | None
[outcomes](outcomes.md) | Outcomes is a list of tests to run against the response. See below for details. | None

See these [examples](examples.md).

