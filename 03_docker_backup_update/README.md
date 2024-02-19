# Docker Backup and Update

This loops though the folder containing all the docker stacks (as specified in `config.txt` as `stacks_directory`).

In each the folder for each service, there should be a `backup.txt` file with instructions on what to back up. If a `backup.txt` file exists, this script will do the following:
1) Down the container with `docker compose down`
2) `rsync` any volumes specified in the `backup.txt` file to the destination specified in `config.txt` as `backup_destination_directory`. See more info below.
3) Update the stack using `docker compose pull`
4) Up the stack using `docker compose up -d`

Finally, it will run `docker image prune -f`.

### backup.txt
My dockers folder is organized like this:
```
├── service1
│   ├── backup.txt
│   └── compose.yaml
├── service2
│   ├── backup.txt
│   └── compose.yml
└── service 3
    ├── backup.txt
    └── compose.yml
```
Each `backup.txt` looks like:
```
backup: volume1
backup: volume2
NOTE ANY LINES THAT DONT START WITH BACKUP WILL BE IGNORED
```
Only the volumes specified in `backup.txt` will be backed up to the destination directory.
