# Faster Image Download

Source: https://nrp.ai/documentation/userdocs/running/fast-img-download

# Faster Image Download

## Spegel image cache

We’re currently using spegel on most nodes running containerd. It currently does not support CRI-O (several nodes in the cluster).

Spegel allows all nodes act as a caching proxy for images, which speeds up images downloads a lot.

UBER Kraken is now deprecated! If you used “localhost:30081” URLs, please switch back to normal ones.
