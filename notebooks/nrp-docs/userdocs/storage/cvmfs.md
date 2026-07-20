# CVMFS

Source: https://nrp.ai/documentation/userdocs/storage/cvmfs

# CVMFS

CVMFS is a distributed filesystem that allows you to mount software repositories and datasets on your local machine. It is used to distribute software and data across the grid, and is widely used in the High Energy Physics community.

### OSDF Origins

We host a number of OSDF origins in the cluster, that can be used to distribute read-only data, f.e. software packages or datasets. You can contact us to place data on origins.

The data is stored in a single server spinning drives JBOD, with RAID 50.

Credit: Origins space

Caches and origins map

### Using OSG caches and origins data via CVMFS

To attach the CVMFS volume which can mount all repos, create the PVC (taken from https://github.com/cvmfs-contrib/cvmfs-csi/tree/master/example ):

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cvmfs
spec:
  accessModes:
  - ReadOnlyMany
  resources:
    requests:
      # Volume size value has no effect and is ignored
      # by the driver, but must be non-zero.
      storage: 1
  storageClassName: cvmfs
```

Then attach it to your pod:

```
apiVersion: v1
kind: Pod
metadata:
  name: cvmfs-all-repos
spec:
  containers:
   - name: idle
     image: busybox
     imagePullPolicy: IfNotPresent
     command: [ "/bin/sh", "-c", "trap : TERM INT; (while true; do sleep 1000; done) & wait" ]
     volumeMounts:
       - name: my-cvmfs
         mountPath: /my-cvmfs
         # CVMFS automount volumes must be mounted with HostToContainer mount propagation.
         mountPropagation: HostToContainer
  volumes:
   - name: my-cvmfs
     persistentVolumeClaim:
       claimName: cvmfs
```

If you need to mount a specific repo, add the subPath to the pod mount:

```
     volumeMounts:
       - name: my-cvmfs
         # It is possible to mount a single CVMFS repository by specifying subPath.
         subPath: alice.cern.ch
         mountPath: /my-alice-cvmfs
         mountPropagation: HostToContainer
```

- ams.cern.ch

- atlas.cern.ch

- belle.cern.ch

- clicdp.cern.ch

- cms.cern.ch

- config-osg.opensciencegrid.org

- connect.opensciencegrid.org

- cvmfs-config.cern.ch

- eic.opensciencegrid.org

- gluex.osgstorage.org

- gwosc.osgstorage.org

- icecube.opensciencegrid.org

- icecube.osgstorage.org

- larsoft-ib.opensciencegrid.org

- larsoft.opensciencegrid.org

- nexo.opensciencegrid.org

- oasis.opensciencegrid.org

- sdsc-nrp-osdf-origin.osgstorage.org

- sft.cern.ch

- singularity.opensciencegrid.org

- snoplus.egi.eu

- sphenix.opensciencegrid.org

- spt.opensciencegrid.org

- stash.osgstorage.org

- unpacked.cern.ch

- veritas.opensciencegrid.org
