What it does
============

It wraps the "requests" python library inserting headers, authentication etc and
making your requests to a host: provided as a command line argument.

It checks the response from the server for expected status-codes/body/header/dpath-json
contents and passes or fails the test based on definition.

Can be used to specify and pass/fail on performance of api response.

A copy/paste curl equivalent of the request is included in the output for
convenience.

Easily introduced into a CI/CD deploy pipeline.

Without --force, any API requests that are not GET's will be skipped as a safety
mechanism to ensure we're not overwriting or creating data unconciously.

