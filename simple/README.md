Default Router Deployment
=========================

The minimal router configuration is as follows:

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: simple-router
spec: {}
```

This results in a router with listeners on

* 5672 for plain AMQP, 5671 for AMQP over TLS[1],

* 8672 for console access, metrics, healthz and AMQP over websockets,

* 55671 for TLS secured inter-router connections[1]

* 45672 for connections from edge routers.

A service is created with all ports exposed. At present this is always
of type LoadBalancer.

No routes are created by default and none of the listeners are
authenticated.

The address-space is not customised in any way, i.e. all addresses are
treated as having `balanced` distribution.

Issues:

(i) inter-router is not authenticated and is using default certs
(should create a specific issuer and a specific cert)
(ii) add some default address prefixes(?)
(iii) (minor) more intuitive names for listeners and therefore ports
on service would be nice
(iv) support other service types
(v) edge router listener should be secured (same profile as
inter-router listeners?)

Questions:

(i) should we expose routes?
(ii) should authentication be enabled?

---------------------------------------------------------------------

[1] Assuming that certmanager is installed. If not then the 5671
listener is not configured and the inter router listener is on 55672
and does not use TLS.
