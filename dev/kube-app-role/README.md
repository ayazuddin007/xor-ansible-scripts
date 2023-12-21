kube-app-role
=========

This role is responsible for configuring the manifests for deploying various artifacts on kubernetes cluster.


Role Variables
--------------

Few variables should be setted for proper exceution of the role via --extra-vars while running the playbook. They are listed as follows:
1)  ns-controlRepo: refers to the name and branch of the control repo passed in "name/branch" format
2)  Cr_groupId: refers to control repo group ID
3)  majorVersion: Major version of the artifact to be deployed
4)  artifact_id: Name of the artifact to be deployed
5)  registry_id: Registry id where the binaries reside in jfrog
6)  s1_build_number: Build number of section 1
7)  s2_build_number: Build number of section 2
8)  s3_build_number: Build number of section 3


Example Playbook
----------------

Following is an example to include the role in playbook:

    - hosts: servers
      roles:
         - kube-app-role


