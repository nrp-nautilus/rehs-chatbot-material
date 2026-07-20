# CPU Throttling

Source: https://nrp.ai/documentation/userdocs/running/cpu-throttling

# CPU Throttling

The jobs are running in linux cgroups, and CPU limits are enforced by those. There’s a number of issues still pending that result in decreased performance if limits are not set right.

In general case, when the application can limit itself in the number of cores used, the request can be set to that number and limit to any higher number. This will accomodate all spikes that may occur. You should avoid setting the limit much higher than request and then constantly consuming more cores than request, as this will make the OS unstable in case there’s not enough cores left for the system. The scheduling desicions are always based on the request, not limit.

Google best practices for requests and limits

The grafana pod monitoring dashboard shows throttling for pods, and there’s an open ticket discussing what it means and how to make it more informative, but also highlighting the pending problems with throttling: https://github.com/kubernetes-monitoring/kubernetes-mixin/issues/108 .

In general requesting full cores and using Guaranteed QoS (request == limit) seems to help avoid throttling.

Some more links to issues still open: 1 , 2

CPU manager blog post
