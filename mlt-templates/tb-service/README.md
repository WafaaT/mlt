# TensorBoard MLT Application

A Tensorboard service in kubernetes cluster.

This template requires that the directory path to the TensorFlow job
results you need to view be set in the `tbjob` YAML file in
`k8s-templates` using `mlt config set template_parameters.path <value>`.

Some `env` variables may be required to allow access to the storage system.