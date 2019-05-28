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

The CA cert secret needs to be copied to the other cluster(s). One way
of doing so is to export it in the context of the first cluster, then
recreate it in the context of the other clusters, e.g.:

```
oc extract secret/cluster1-selfsigned --to=/path/to/copy-of-ca
```

```
 oc create secret generic inter-router-ca --from-file=/path/to/copy-of-ca
```

Alternatively it can be viewed as yaml and edited to remove the
context specific metadata, then created in the other cluster(s).

Once available the other router can be created. The host should
reflect the route name of the inter-router listener as created by the
operator.b

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: cluster2
spec:
  issuer: inter-router-selfsigned
  sslProfiles:
  - name: inter-router-tls
    requireClientCerts: true
  interRouterConnectors:
  - host: cluster1-inter-router-myproject.127.0.0.1.nip.io
    port: 443
    verifyHostname: false # due to https://github.com/interconnectedcloud/qdr-operator/issues/16
    sslProfile: inter-router-tls
```

