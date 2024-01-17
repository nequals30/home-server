# Script that Writes nginx Reverse Proxy Server Blocks

There are two functions in here:

### create_one_conf
This writes the server block for a given domain and port. There are two ways of calling it from command line:

This will just show you the contents of the server block without actually writing it.
```
./create_one_conf.py service3.mydomain.com 5000
```

Adding `--write` will will write the server block to the location specified in `create_one_conf.py` (by default, `output_confs/` in this folder). 
```
./create_one_conf.py service3.mydomain.com 5000 --write
```
The output file could be `/etc/nginx/conf.d/` directly, but then it should be run with sudo permissions.

### create_all_confs
This reads through the file `services.txt` and writes the configuration files in a loop using the other function.

`services.txt` should be pipe delimited [full URL, port] like:
```
service1.mydomain.com | 5000
service2.mydomain.com | 5001
```

This function can be run without arguments `./create_all_confs.py`.

