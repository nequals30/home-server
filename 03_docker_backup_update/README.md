# Docker Backup and Update
This script loops through a bunch of docker stacks, updates them, and backs up specific volumes to a specified directory, and prunes unused images.

### Configuration
It's configured via the `config.txt` file in this folder, as follows:

```
stacks_directory = /path/to/stacks/						# loops through all stacks in this folder
backup_destination_directory = /path/to/destination/	# backs up volumes to here
username = user											# chowns them as this user
```

### backup.txt
This script will only operate on stack folders which contains a `backup.txt` file. My docker stacks folder is organized like this:
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
The `backup.txt` file contains a list of volumes that get backed up:
```
backup: volume1
any lines that don't start with `backup:` are ignored
backup: volume2
```
If you want this script to update a stack without backing up any of it's volumes, just create a blank `backup.txt` file in that stack's folder.

### What it does
For each stack, it will:
1) Down the containers with `docker compose down`
2) `rsync` any volumes specified in the `backup.txt` file to the backup destination (which is specified in this folder's `config.txt` as `backup_destination_directory`).
3) Run `chown -R username:username` on the data in the backup destination. This is because some volumes require `sudo` permissions to read, and I wanted to strip that out.
4) Update the stack using `docker compose pull`
5) Up the stack using `docker compose up -d`

Finally, it will run `docker image prune -f`.
