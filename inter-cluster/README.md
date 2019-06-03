inter-cluster router network secured with mutual TLS
====================================================

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: cluster1
spec:
  sslProfiles:
  - name: inter-router-tls
    requireClientCerts: true
  interRouterListeners:
  - name: inter-router
    port: 55672
    expose: true
    sslProfile: inter-router-tls
```

The other cluster will need a certificate issued by the
inter-router-ca for cluster1. This can be generated (in cluster1)
with:

```
---
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: cluster1-inter-router-ca-issuer
spec:
  ca:
    secretName: cluster1-inter-router-tls-ca
---
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
  name: cluster2-inter-router-tls
spec:
  commonName: cluster2-inter-router-default.apps.grs-cluster2.devcluster.openshift.com
  issuerRef:
    name: cluster1-inter-router-ca-issuer
  secretName: cluster2-inter-router-tls
---

```

The secret then needs to be copied to the other cluster, e.g.

```
mkdir /tmp/cluster2-inter-router-tls
oc extract secret/cluster2-inter-router-tls --to=/tmp/cluster2-inter-router-tls
```

then in the other cluster context:

```
oc create secret generic cluster2-inter-router-tls --from-file=/tmp/cluster2-inter-router-tls
```

Once the secret is available on the other cluster, the other router
can be created. The host should reflect the route name of the
inter-router listener as created by the operator.

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: cluster2
spec:
  sslProfiles:
  - name: inter-router-tls
    credentials: cluster2-inter-router-tls
    caCert: cluster2-inter-router-tls
  interRouterConnectors:
  - host: cluster1-inter-router-myproject.127.0.0.1.nip.io
    port: 443
    verifyHostname: false # due to https://github.com/interconnectedcloud/qdr-operator/issues/16
    sslProfile: inter-router-tls
```

