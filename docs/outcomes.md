Outcomes
========

Outcomes are where the logic goes.  We verify the response from the server against these defined outcomes.

Pass or fail scenarios are defined below.

Outcomes | Description
----------------------|-----------------------------
response_body_contains | PASS if string in body.
response_body_doesnt_contain | FAIL if string in body.
response_max_time_ms | FAIL if response takes longer than int.
response_json_contains | FAIL if json response at path doesn't match.
expect_status_code | FAIL if response status code differs from int.
response_redirect | FAIL if string not in response location header.
response_headers | FAIL if the headers received from the request doesn't contain the list of headers provided.
response_header_values | FAIL if the *values* of the headers in the test don't match the values in the response.
response_header_value_contains | FAIL if the value of the headers in the response do not match a given regexp pattern.
show_body | output the body to stdout.
colour_output  | Colour PASS/FAIL

