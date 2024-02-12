# home-server
Some scripts I run on my home server.

---
## Scheduled Scripts

### 1. Logger
This creates a markdown file placeholder. As automated scripts run, it logs them to this markdown file. Then, the markdown file gets turned into an HTML page that is hosted on my server, so I can quickly see if my scripts are running.

---
## Utilities

### nginxServerBlocks
This takes a pipe-separated list of services and ports, like `service1.mydomain.com | 5000`, and turns them into reverse proxy server blocks for nginx.
