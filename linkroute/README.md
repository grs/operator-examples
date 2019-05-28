link routing
============

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: topic1
spec:
  linkRoutes:
  - prefix: foo
    direction: in
    connection: broker
  - prefix: foo
    direction: out
    connection: broker
  connectors:
  - name: broker
    host: broker
    port: 5672
    routeContainer: true
```

```
oc run broker --env AMQ_USER=admin --env AMQ_PASSWORD=admin --image=amq-broker-7/amq-broker-72-openshift --expose=true --port 5672
```