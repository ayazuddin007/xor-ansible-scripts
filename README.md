# xor-ansible-scripts

This repo is used to deploy artifacts to the environment.

## Pre-requisites

Following python packages must be present in the system. They can be downloaded using pip3
- artifactory
- dohq-artifactory

## Features/Functions
- This repo will help us to deploy application/artifacts on the environment
- This script is used in section3 of our pipeline.

### To execute the ansible playbook run following command:
```bash
 ansible-playbook setup-app-demo.yml --extra-vars "@datas-${env.BUILD_NUMBER}.yaml" -e '{"namespaces":[<target-namespace>]}'
```
### To execute the python script:
```bash
python3 jfrogVersion.py group_id:artifact_id range1,range2
```
Where : 
- group_id: Group_id mentioned in pom.xml
- artifact_id: artifact-id mentioned in pom.xml
- range1,range2: lower limit and upper limits of the range
#### Example:



![image](https://user-images.githubusercontent.com/94039951/159438176-99ab6088-4330-4426-a408-437dbc73fbd0.png)


The output will give us the link to the latest manifest zip available in jfrog depending on the range given.



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





