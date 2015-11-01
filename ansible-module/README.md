Smoke tests in Ansible
======================

Running smolder tests from inside ansible is a very effective way of testing a distributed system.

The github_status.yaml example in this directory uses connection: local to run locally for an easy example.

You can use the full power of delegate_to and separate playbooks,
 with distinct "hosts" tags to fully test a complex system.


```
ansible-playbook --module-path ansible-module/ ansible-module/github_status.yaml -i ansible-module/hosts -k
```

Add the module to your modules path with the MODULES_PATH variable, or the --module-path argument.
  
Both ansible and smolder need to be installed in your virtualenv.  

Ansible doesn't support python3, smolder supports both, so you will need the python2.7 variant installed to use
the smolder module.