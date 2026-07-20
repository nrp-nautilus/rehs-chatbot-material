# Ceph FS / RBD

Source: https://nrp.ai/documentation/userdocs/storage/ceph

# Ceph FS / RBD

## Best Practices for File Access in shared filesystems

Use Unique Files: Always create or use unique files rather than sharing the same file to minimize conflicts.

Avoid Long-Lived Open Handles: Close files as soon as you are done working with them to prevent holding locks longer than necessary.

Favor Copy Operations: If multiple clients need to work with the same data, consider using a copy of the file rather than the original.

## Avoiding Write Conflicts in shared filesystems

When using CephFS, it is crucial not to open the same file for write from multiple parallel clients. Doing so can lead to:

File Locking Issues: Concurrent writes can lock the file, potentially blocking other clients.

Data Corruption: Simultaneous writes to a single file can corrupt the file system or the data contained within.

## Recommended Strategies to Avoid Conflicts:

File Versioning: Implement a versioning system for files that multiple clients may need to update.

Locking Mechanisms: Utilize designated locking mechanisms to control access to shared resources if required for specific applications.

Coordination Among Clients: Use coordination protocols or systems to manage write access among different clients.

## Ceph filesystems data use

Credit: Ceph data usage

General ceph grafana dashboard

## Currently available storageClasses:

Ceph shared filesystem ( CephFS ) is the primary way of storing data in nautilus and allows mounting same volumes from multiple PODs in parallel ( ReadWriteMany ).

Ceph block storage allows RBD (Rados Block Devices) to be attached to a single pod at a time ( ReadWriteOnce ). Provides fastest access to the data, and is preferred for all datasets not needing shared access from multiple pods .

## UCSD NVMe CephFS filesystem policy

The filesystem is very fast and small. We expect all data on it to be used for currently running computation and then promptly deleted. We reserve the right to purge any data that’s staying there longer than needed at admin’s discretion without any notifications.
