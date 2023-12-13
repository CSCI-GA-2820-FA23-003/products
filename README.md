# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-003/products/graph/badge.svg?token=NPSQQ56DRJ)](https://codecov.io/gh/CSCI-GA-2820-FA23-003/products)
[![Build Status](https://github.com/CSCI-GA-2820-FA23-003/products/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-003/products/actions)

## Overview

This project is a demo of CICD using Tekton pipeline on an OpenShift cluster. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:
111
```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
├── test_routes.py  - test suite for service routes
└── factories.py    - product factory for test cases
```

## Running the service

The project uses Flask and to start the service, simply use:

```bash
$ flask start
```

You should be able to reach the service at: http://localhost:8000. The port that is used is controlled by an environment variable defined in the .flaskenv file which Flask uses to load it's configuration from the environment by default.

## Information about this repo

### Models

#### `Product`

| `Name`      | `Data type`             |
| ----------- | --------------------- |
| id | uuid|
| name |String |
| price | Float |
| category | String |
| inventory | Integer |
| available | Boolean |
| created_date | Date |
| modified_date | Date |

### Available Methods

| `Endpoint``          | `Methods`` | `Rule``       |
|-------------------|---------|---------------------|
| create_products   | POST    | /products           |
| delete_products   | DELETE  | /products/{product_id} |
| get_products      | GET     | /products//products/{product_id} |
| list_products     | GET     | /products           |
| purchase_products | PUT     | /products/{product_id}/purchase |
| update_product    | PUT     | /products//products/{product_id} |

## Steps for Openshift
1. Deploy the postgresql
   `oc apply -f .tekton/postgresql.yaml`
2. Deploy the pipeline
   `oc apply -f .tekton/pipeline.yaml`
3. Deploy the tasks
    `oc apply -f .tekton/tasks.yaml`

## Steps for Local Kubernetes deployment
Make sure your cluster is running. To bring up cluster use the following command:
Make cluster

Check if you etc hosts has cluster-registry defined. Check by using following command:

cat /etc/hosts
![image](https://github.com/CSCI-GA-2820-FA23-003/products/assets/81439372/3b0ae461-4463-4220-9427-2cfa7e55f7c4)

If cluster registry is not defined use following command:

sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"
After that build docker image as follows:
docker build -t products:1.0 .

Tag the image, and push it to local registry: 
docker tag products:1.0 cluster-registry:32000/products:1.0

docker push cluster-registry:32000/products:1.0

Apply to local cluster:
Kubectl apply -f k8s/.




## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
