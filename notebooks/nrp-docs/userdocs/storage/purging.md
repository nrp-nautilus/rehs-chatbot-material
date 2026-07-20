# Purging

Source: https://nrp.ai/documentation/userdocs/storage/purging

# Purging

Please purge any unused data. Our storage must not be used as long-term archival storage .

In cephFS and RBD (not S3) if you simply run rm -rf <folder> on a folder with many (more than 10,000) files, it might crash the metadata server or will be too slow.

The best way to delete many files is to run find , since it will not try to scan the whole folder and will be deleting files as it finds those:

```
find some_folder -type f -delete
```

This will delete all files in the folder, but leave empty folders. If you don’t have too many folders, you can simply run rm -rf folder .

If you still have multiple (thousands) empty folders, you can run:

```
find some_folder/* -depth -type d -delete
```
