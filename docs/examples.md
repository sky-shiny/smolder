Examples
========

Here are some contrived examples that you can run.


[github_status.json](../examples/github_status.yaml)
- connects to http://status.github.com/api/status.json on port 80 and expects to be redirected to https://status.github.com/api/status.json with a 301.
- then tests https://status.github.com/api/status.json and FAILs if github is reporting issues on their status page.
- Expect the final test of site speed to fail as 200ms is typically about half the normal page load time for https://status.github.com.

```
---
tests:
  -
    name: "Github Status"
    outcomes:
      expect_status_code: 301
      response_redirect: "https://status.github.com/api/status.json"
    inputs:
      headers:
        User-Agent: "Smolder smoke test library"
    uri: /api/status.json
  -
    inputs:
      headers:
        User-Agent: "Smolder smoke test library"
    name: "Github Status ssl"
    outcomes:
      response_json_contains:
        status: good
      response_max_time_ms: 200
    port: 443
    protocol: https
    uri: /api/status.json
```


[aws_status.json](../examples/aws_status.json)
- another contrived status page example

```
{
    "tests": [
        {
            "name": "AWS Status",
            "uri": "/",
            "inputs": {
                "headers": {
                    "User-Agent": "Smolder smoke test library"
                }
            },
            "outcomes": {
                "response_body_contains": "Service is operating normally"
            }
        }
    ]
}
```

[example_test.json](../examples/example_test.json)
- tests an RFC1918 (won't work out of the box) address by trying to PUT data to it and verifying the result.
- call non get requests with ```smolder 10.0.0.1 example_test.json --force```

```
{
    "tests": [
        {
            "name": "Status",
            "uri": "/status",
            "inputs": {
                "headers": {
                    "User-Agent": "Smolder smoke test library"
                }
            },
            "outcomes": {
                "response_body_contains": "HEALTHY"
            }
        },
        {
            "name": "Finalize verify requires auth",
            "uri": "/downloads/539e92c0-06a1-11e4-9191-0800200c9a66/finalise",
            "method": "put",
            "inputs": {
                "data": {
                    "downloadTransaction": {
                        "status": "COMPLETE"
                    }
                },
                "headers": {
                    "User-Agent": "Smolder smoke test library",
                    "Host": "bskyb.com",
                    "content-type": "Application/json"
                }
            },
            "outcomes": {
                "expect_status_code": 401
            }
        }
    ]
}
```
