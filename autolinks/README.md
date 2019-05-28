autolinks
=========

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: queue
spec:
  addresses:
  - prefix: foo
    waypoint: true
  autoLinks:
  - address: foo
    direction: in
    connection: broker
  - address: foo
    direction: out
    connection: broker
  connectors:
  - name: broker
    host: broker2
    port: 5672
    routeContainer: true
```


```
oc run broker2 --env AMQ_USER=admin --env AMQ_PASSWORD=admin --image=amq-broker-7/amq-broker-72-openshift --expose=true --port 5672
```
