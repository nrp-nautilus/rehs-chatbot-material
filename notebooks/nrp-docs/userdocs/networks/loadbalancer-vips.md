# LoadBalancer VIPs

Source: https://nrp.ai/documentation/userdocs/networks/loadbalancer-vips

# LoadBalancer VIPs

MetalLB manages two address pools, both advertised via BGP to UCSD Prism (AS 26397).

## IPv4

### Quick start

No extra fields are needed. LoadBalancer type defaults to IPv4:

```
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: my-namespace
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 443
      targetPort: 8443
```

### Pin a specific address

```
spec:
  type: LoadBalancer
  loadBalancerIP: 67.58.49.70
```

Pick an address in 67.58.49.48-63 or 67.58.49.64-95 . Check with cluster admins before reserving one.

## IPv6

### Quick start

Add ipFamilyPolicy and ipFamilies to your Service spec:

```
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: my-namespace
spec:
  type: LoadBalancer
  ipFamilyPolicy: SingleStack
  ipFamilies:
    - IPv6
  selector:
    app: my-app
  ports:
    - port: 443
      targetPort: 8443
```

MetalLB auto-assigns an address from 2607:f720:1720:E100::/64 . Find it with:

```
kubectl get svc my-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### Pin a specific address

```
spec:
  type: LoadBalancer
  loadBalancerIP: 2607:f720:1720:e100::10
  ipFamilyPolicy: SingleStack
  ipFamilies:
    - IPv6
```

### Dual-stack (IPv4 + IPv6)

```
spec:
  type: LoadBalancer
  ipFamilyPolicy: PreferDualStack
  ipFamilies:
    - IPv4
    - IPv6
```

### Application requirements

Your app must explicitly bind to the IPv6 socket. Most servers default to IPv4 only.

nginx

```
server {
  listen 443 ssl;
  listen [::]:443 ssl;  # required for IPv6
}
```

Django

```
python manage.py runserver [::]:8000
```

For production deployments, bind the application server to IPv6 as well. For example, with Gunicorn:

```
gunicorn myproject.wsgi:application --bind [::]:8000
```

FastAPI

```
uvicorn main:app --host :: --port 8000
```

Node.js

```
app.listen(8080, '::')  // '::' binds both IPv4 and IPv6
```

Go

```
http.ListenAndServe("[::]:8080", handler)
```

## Constraints

- ICMP (ping) does not work for MetalLB VIPs in BGP mode. Use TCP/UDP only.

- Calico’s global policy permits inbound on ports 443 and 22 by default. Other ports need an existing matching GlobalNetworkPolicy or a new exception.

- IPv4 VIPs are globally reachable through UCSD’s aggregate 67.58.49.x route. The /32 host routes are only used inside UCSD for last-hop forwarding.

- IPv6 /128 host routes are advertised globally via UCSD’s BGP upstream.

## Verify a route is advertised

```
# Check assigned VIP
kubectl get svc my-service

# IPv4: confirm BGP advertisement
kubectl exec -n metallb-system <speaker-pod> -- \
  vtysh -c "show bgp ipv4 unicast"

# IPv6: confirm BGP advertisement
kubectl exec -n metallb-system <speaker-pod> -- \
  vtysh -c "show bgp ipv6 unicast"
```

Your VIP should appear as a /32 for IPv4 or /128 for IPv6. Run the command on both speaker pods if you need to confirm both speaker nodes are advertising it.
