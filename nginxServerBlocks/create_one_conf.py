#!/usr/bin/env python3
import argparse
"""
Generates an NGINX server block configuration for the given domain and port.
You can run it from command line like, to test that it works:

this will just print the output:
./create_one_conf.py service.mydomain.com 5002

this will actually write it to the file:
./create_one_conf.py service.mydomain.com 5002 --write
"""

def create_one_conf(domain, port, write_to_file):
    out_path = "output_confs/"

    subdomain = domain.split('.')[0]
    conf_file_path = f"{out_path}/{subdomain}.conf"

    conf_contents = f"""
server {{
    listen 80;
    listen [::]:80;
    server_name {domain};
    return 301 https://$server_name$request_uri;
}}

server {{

        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        server_name {domain};

        ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;

        ssl_session_cache shared:le_nginx_SSL:1m;
        ssl_session_timeout 1440m;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";

        location / {{
                proxy_pass http://localhost:{port}/;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }}
}}
"""
    if write_to_file:
        with open(conf_file_path, 'w') as conf_file:
            conf_file.write(conf_contents)
            print(f"Configuration for {subdomain} saved to {conf_file_path}")

    return conf_contents


def main():
    parser = argparse.ArgumentParser(description='Generate NGINX server block configurations.')
    parser.add_argument('domain', type=str, help='Domain name for the service')
    parser.add_argument('port', type=int, help='Port number where the service is running')
    parser.add_argument('--write', action='store_true', help='Writes output to file instead of printing it')
    
    args = parser.parse_args()

    conf = create_one_conf(args.domain, args.port, args.write)
    if not(args.write):
        print(conf)

if __name__ == "__main__":
    main()

