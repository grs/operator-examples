Custom Listeners
================

If a user wants to:

* change ports used to connect to the router network
* expose a port for access to clients outside the cluster[1]
* prevent certain listeners from being created

they need to define the list of listeners. Similarly, if they want to
change the port used for inter-router connections, control whether tls
is used for the inter-router listener, or expose the inter-router
listener for access to routers outside the cluster[1], they need to
define the inter-router listener(s)[2].

e.g. custom ports for all listeners:

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: custom-ports
spec:
  listeners:
  - name: amqp
    port: 6666
  - name: amqps
    port: 7777
    sslProfile: default
  - name: console
    port: 8888
    http: true
  interRouterListeners:
  - name: inter-router
    port: 5555
    sslProfile: default
```

e.g. no console or websockets access:

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: no-console
spec:
  listeners:
  - name: amqp
    port: 5672
  - name: amqps
    port: 5671
    sslProfile: default
```

e.g. exposing ports through routes (note that exposing through a route
requires the listener either talk http or tls):

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: exposed-ports
spec:
  listeners:
  - name: amqp
    port: 5672
  - name: amqps
    port: 5671
    sslProfile: default
    expose: true
  - name: console
    port: 8080
    http: true
    expose: true
  sslProfiles:
  - name: inter-router
    requireClientCerts: true
  interRouterListeners:
  - name: inter-router
    port: 55672
    expose: true
    sslProfile: inter-router
```

Issues:

* Can't alter HTTP port as the liveness- and readiness- listeners are
  hard coded to use it. Need to separate those out and/or provide a
  separate way to select the port they use.

Questions:

* Exposing ports seems like a common thing to do yet at present it
  requires all the listeners to be defined. On the other had exposing
  the interface probably is something that should be explicit, at
  least unless the listener in question is secured. Should the
  decision to expose the listener be separated from the definition of
  the listener? Or should we secure listeners by default allowing us
  to (more) safely expose them by default also?


[1] At least via an openshift route. Other options here are for the
service to be of type NodePort or LoadBalancer, but details here vary
I think on different kubernetes platforms.

[2] Though in theory you could have more than one inter-router
listener, in practice there isn't usually much need to do so.