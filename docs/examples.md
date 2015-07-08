Examples
========

Here are some contrived examples that you can run.


[../examples/github_status.json](github_status.json)
- connects to http://status.github.com/api/status.json on port 80 and expects to be redirected to https://status.github.com/api/status.json with a 301.
- then tests https://status.github.com/api/status.json and FAILs if github is reporting issues on their status page.
- Expect the final test of site speed to fail as 200ms is typically about half the normal page load time for https://status.github.com.

```
smolder status.github.com github_status.json
```

[../examples/aws_status.json](aws_status.json)
- another contrived status page example

```
smolder status.aws.amazon.com aws_status.json
```

[../examples/example_test.json](example_test.json)
- tests an RFC1918 (won't work out of the box) address by trying to PUT data to it and verifying the result.

```
smolder 10.0.0.1 example_test.json --force
```


[../examples/soa_test.json](soa_test.json)
- tests an https endpoint which has an issue with it's certificate
```
smolder 173.223.194.219 soa_test.json
```

