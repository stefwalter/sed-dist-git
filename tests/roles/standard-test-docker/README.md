# Ansible role for docker image subjects

Put this role in your test_docker.yml playbook. You'll need
to have the following variables defined:

 * subjects: A docker image name
 * artifacts: An artifacts directory
 * playbooks: A playbook to run inside of the container
