changing address semantics
==========================

To define some part of the address space to be multicast:

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: multicast-example
spec:
  addresses:
  - prefix: foo
    distribution: multicast
  - pattern: "*/bar"
    distribution: multicast
```