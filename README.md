# home-server
Some scripts I run on my home server. Each set of scripts has a folder, and each is designed to be a stand-alone and self-contained. Each folder has a README explaining it.

The numbered scripts run automatically via cron, while the utility scripts are run manually.

---
## Scheduled Scripts
The scheduled scripts run out of the `orchestration` folder, and my crontab looks like this:
```
MY CRONTAB
```

### 1. Logger
This creates a markdown file with a placeholder for each script run by cron. As scripts run, it logs their success or error messages. At the end, it gets turned into an HTML page that is hosted on my server, so I can see how things went.

### 2. Local Backup
This incrementally copies everything from my main hard drive onto my backup drive. Since using `rsync` with the `--delete` flag is scary, this script has a bunch of guard-rails around things that could go wrong.

---
## Utilities

### nginxServerBlocks
This takes a pipe-separated list of services and ports, like `service1.mydomain.com | 5000`, and turns them into reverse proxy server blocks for nginx.
