---
layout: page
title: Infrastructure
permalink: /infrastructure/
---

# Infrastructure

IKYEASight runs on two self-hosted Ubuntu Server machines connected via a local network, with Nginx acting as a dual reverse proxy to expose both Odoo instances to the internet.

---

## Hardware

| Server | Role | Specs |
|---|---|---|
| Old Laptop | STG (Gateway) + DEV Proxy | 2GHz Dual-Core, 8GB RAM, 100GB storage |
| Local Machine | DEV Server (192.168.1.249) | — |

---

## Network Topology

```mermaid
flowchart TB
    title["Architecture: Dual-Server Reverse Proxy (stg + dev)"]
    style title fill:none,stroke:none,font-size:20px

    internet((Internet))

    subgraph Router [AT&T Router]
        direction TB
        public_ip([Public IP: X.X.X.X])
        nat[Port Forwarding: 80/443]
    end

    subgraph stg_server ["STG Server — Gateway"]
        direction TB
        nginx_stg[Nginx stg.craft2orbit.xyz]
        nginx_dev_proxy[Nginx dev.craft2orbit.xyz]
        odoo_stg[(Odoo STG)]
    end

    subgraph dev_server [DEV Server — 192.168.1.249]
        direction TB
        nginx_local[Nginx Local]
        odoo_dev[(Odoo DEV)]
    end

    internet --> public_ip
    public_ip --> nat

    nat -->|Traffic for stg| nginx_stg
    nat -->|Traffic for dev| nginx_dev_proxy

    nginx_stg -->|Localhost:8069| odoo_stg

    nginx_dev_proxy -- "SSL Terminated<br/>Forward to LAN" --> nginx_local
    nginx_local -->|Localhost:8069| odoo_dev

    classDef server fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef proxy fill:#e1f5fe,stroke:#01579b;
    classDef db fill:#fff3e0,stroke:#ffb300;

    class stg_server,dev_server server;
    class nginx_stg,nginx_dev_proxy,nginx_local proxy;
    class odoo_stg,odoo_dev db;
```

---

## Ubuntu Server Setup

1. Create a bootable USB with Rufus using the Ubuntu Server 24.04 image
2. Enable UEFI boot and install with:
   - Server hostname
   - Username and password
   - OpenSSH enabled
3. Connect via SSH: `ssh username@server-ip`
4. Enable Wi-Fi if needed

---

## Odoo Installation

```mermaid
%%{init: {'flowchart': {'rankSpacing': 20, 'nodeSpacing':20}}}%%
flowchart TB
    subgraph GlobalContainer [Odoo Installation]
        direction TB

        subgraph Section1 [Postgres]
            pg_install["sudo apt install postgresql -y<br/>
                sudo -u postgres createuser -s odoo"]

            pg_auth["/etc/postgresql/16/main/pg_hba.conf <br/>
                - Syntax: host database user address auth-method
                - local all all trust
                - host all all 127.0.0.1/32 trust
                - host all all 0.0.0.0/0 trust
                - sudo systemctl restart postgresql"]

            pg_conf["/etc/postgresql/16/main/postgresql.conf<br/>
                - listen_addresses = '*'
                - netstat -nlt | grep 5432
                - tcp 0 0 0.0.0.0:5432 0.0.0.0:* LISTEN"]
        end

        subgraph Section2 [Odoo]
            odoo_install["Dependencies<br/>
                sudo apt install git python3-pip
                build-essential python3-dev
                python3-venv libpq-dev
                libsasl2-dev libldap2-dev
                libssl-dev python-ldap"]

            odoo_folderStructure["Folder Structure and Ownership<br/>
                - sudo mkdir /opt/odoo
                - sudo adduser --system --group<br/>--home=/opt/odoo --shell=/bin/bash odoo
                - sudo chown odoo:odoo /opt/odoo
                - sudo chmod 775 /opt/odoo"]

            odoo_cloningAndRequirements["Cloning and requirements installation<br/>
                - git clone https://github.com/odoo/odoo<br/> --depth 1 --branch 18.0 odoo
                - cd /opt/odoo/odoo
                - python3 -m venv venv
                - source venv/bin/activate
                - pip install -r requirements.txt"]

            odoo_conf["sudo nano /etc/odoo.conf<br/>
                [options]
                db_user = odoo
                db_password = &lt;YOUR_DB_PASSWORD&gt;
                admin_passwd = &lt;YOUR_ODOO_MASTER_PASSWORD&gt;
                xmlrpc_interface = 0.0.0.0
                addons_path = /opt/odoo/odoo/addons,/opt/odoo/custom_addons
                data_dir = /var/lib/odoo"]
        end

        subgraph Section3 [Services Setup]
            postgres["sudo apt install postgresql
                    /lib/systemd/system/postgresql.service"]

            odoo["/etc/systemd/system/odoo.service<br/>
                [Unit]<br/>
                Description=Odoo 18/19<br/>
                Requires=postgresql.service<br/>
                After=network.target postgresql.service<br/>
                [Service]<br/>
                Type=simple<br/>
                User=odoo<br/>
                ExecStart=/opt/odoo/odoo/venv/bin/python3<br/> /opt/odoo/odoo/odoo-bin -c /opt/odoo/odoo.conf<br/>
                [Install]<br/>
                WantedBy=multi-user.target"]

            systemctl["sudo systemctl daemon-reload<br/>
                    sudo systemctl enable odoo<br/>
                    sudo systemctl start odoo<br/>
                    sudo systemctl start postgresql"]
        end

        subgraph Section4 [Browser Access]
            local["http://your_server_ip:8069"]
            public["https://dev.craft2orbit.xyz/"]
        end
    end

    style GlobalContainer fill:none,stroke:#333,stroke-width:2px
    style Section1 fill:#e1f5fe;
    style Section2 fill:#e8f5e9;
    style Section3 fill:#fff3e0;
    style Section4 fill:#f3e5f5;

    pg_install -.- postgres
    pg_install --- pg_auth
    pg_install --- pg_conf
    pg_install -.- odoo_conf
    postgres --- odoo
    postgres --- systemctl
    odoo --- systemctl
    systemctl -.- local
    systemctl --- nginx
    odoo_install --- odoo_folderStructure
    odoo_folderStructure --- odoo_cloningAndRequirements
    odoo_cloningAndRequirements --- odoo_conf

    classDef smallNode padding:5px,font-size:10.5px,font-weight:bold,text-align:left;
    class pg_install,pg_auth,pg_conf,odoo_install,odoo_folderStructure,odoo_cloningAndRequirements,odoo_conf,postgres,odoo,systemctl smallNode
```

---

## Nginx Configuration

See the full dual-server Nginx reverse proxy configuration in [dev_nginx_dual_server_reverse_proxy.md](https://github.com/otalfredo8/ikyeasight/blob/main/docs/dev_nginx_dual_server_reverse_proxy.md).

**Key domains:**
- `stg.craft2orbit.xyz` → STG Odoo (localhost:8069 on gateway server)
- `dev.craft2orbit.xyz` → DEV Odoo (192.168.1.249:8069 via proxy)
