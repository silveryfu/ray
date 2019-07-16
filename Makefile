SHELL := /bin/bash

# create test clusters
.PHONY: ec2, delete-ec2

ec2:
	cd ./hack/ec2; python3 -m build.kube.cluster up

show-ec2:
	cd ./hack/ec2; bash ./get_clusters.sh

delete-ec2:
	cd ./hack/ec2; python3 -m build.kube.gen_spec $(CLUSTERID); python3 -m build.kube.cluster down
