# Local Backup
This script will incrementally sync a main drive with a backup drive, allowing for deletion. Since using `rsync` with the `--delete` flag is scary, this script has a bunch of guard-rails around things that could go wrong.

The main drive is specified by `main_directory` in the `config.txt`. The backup drive is `backup_directory`.

I have a fear of erasing a lot of data, so if the two drives are different from eachother by a certain amount (as specified by `max_diff_gb`, the script will fail and throw an error.

If successfull, the script will return a message like:
```
main: 1351.2GB, backup: 1351.21GB. rsync added: 0 files, deleted: 0 files, transfer: 0.0 GB
```
