authentication
==============

Currently only TLS client certs are supported for authentication.

```
apiVersion: interconnectedcloud.github.io/v1alpha1
kind: Interconnect
metadata:
  name: authenticated
spec:
  listeners:
  - name: amqps
    port: 5671
    sslProfile: default
    authenticatePeer: true
    saslMechanisms: EXTERNAL
    expose: true
  - name: http
    port: 8080
    http: true
  sslProfiles:
  - name: default
    mutualAuth: true
```


Questions:

* Is TLS client certs only acceptable for GA? (Means secure non-tls
  communication is not possible).

* What about console? Require cert to be installed in browser? Or use
  oauth-proxy? Or support a password for the console (this would
  impact websockets also).

* Authorisation is currently out of scope. Is that ok?