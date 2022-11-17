# k8s-arangodb-token-updater
Implementation of automatic ArangoDb jwt-token update in a Kubernetes cluster

To collect metrics and monitor ArangoDB, authentication with a jwt-token is required. This repository contains an implementation for automatically updating the ArangoDB jwt-token in a Kubernetes cluster.

The token is contained in the Secret object:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: arangodb-token
type: Opaque
data:
  token: '<base64-encoded-token>'
```

To access ArangoDB you need `USERNAME`, `PASSWORD` and `URI`, which will also be stored in the `Secret` object (`arango_secret.yaml`):

```yaml
data:
  PASSWORD: '<base64-encoded-string>'
  URI: '<base64-encoded-string>'
  USERNAME: '<base64-encoded-string>'
```
The update of the token will be run on a schedule using `CronJob` (`cronjob.yaml`), which will run the docker container with the script `arango_token_updater.py`. For the script to work, you must specify the name `Secret` in which to store the jwt-token that you want to update:

```yaml
command: ["python3", "./arango_token_updater.py", "--secret", "arangodb-token"]
```

as well as the name `Secret` which contains the credentials for authorization in ArangoDB:

```yaml
envFrom:
- secretRef:
    name: arangodb-secret
```

The `Jobs` will be run on behalf of a specially created `ServiceAccount` (`role.yaml`).

Once the `Secret` with token has been created and we have made sure that it is successfully updated, we can create a `ServiceMonitor` object for Prometheus to collect metrics, in which to specify the data for authorization:


```yaml
endpoints:
  - bearerTokenSecret:
      key: token
      name: arangodb-token
    path: /_admin/metrics/v2
    port: metrics
    interval: 1m
    scrapeTimeout: 30s
```
