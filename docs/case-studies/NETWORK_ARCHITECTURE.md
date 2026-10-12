# Network Engineering Case Study
### Enterprise Multi-Branch Network with High Availability

**Domain:** Network architecture, routing, segmentation and operational resilience  
**Core tools:** EVE-NG · MikroTik RouterOS v7 · OSPF · VLANs · VRRP · Firewall · Syslog · NTP  
**Source:** [Enterprise Multi-Branch Network](https://github.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability)

---

## The problem

A headquarters and remote offices need secure, manageable network connectivity without a flat broadcast domain or fragile gateway design. This project models **one headquarters and two branch offices in EVE-NG**, combining routing, departmental segmentation and redundant gateways.

## Architecture at a glance

![Network architecture diagram](https://raw.githubusercontent.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability/main/topology/Enterprise-Network.png)

- **Headquarters:** departmental and server VLANs with inter-VLAN routing.
- **WAN / routing:** OSPF backbone **Area 0**, with branches using **Areas 10 and 20** in the documented design.
- **Branch sites:** locally segmented users and printers.
- **Availability:** VRRP active/standby gateway configuration.
- **Operations:** centralized DHCP/relay, source NAT, firewall rules, SSH hardening, Syslog and NTP.

## How it was implemented

| Layer | Implementation |
| :--- | :--- |
| Layer 2 | 802.1Q VLAN segmentation and trunk/access behavior |
| Layer 3 | Multi-area OSPF and inter-VLAN gateway routing |
| Availability | Virtual gateway with VRRP |
| Security | Stateful firewall rules and management hardening |
| Operations | DHCP, NAT, remote logging, time synchronization |
| Test coverage | Connectivity, addressing, routing, gateway behavior and configuration review |

## Validation and evidence

The repository includes **RouterOS configuration files, screenshots, documentation and a dedicated project-validation phase**. These give reviewers implementation detail beyond a conceptual diagram.

Specific high-availability timing values reported in the repository are *lab claims under its simulation configuration*; they are not independently benchmarked here and should not be generalized to production environments.

## What this demonstrates

The engineering work covers more than connecting routers: it connects **IP planning, routing domains, policy boundaries, gateway redundancy and operational visibility** into one documented lab.

## Evidence & implementation

- [Full network project repository](https://github.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability)
- [RouterOS configuration files](https://github.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability/tree/main/configs)
- [Architecture and test documentation](https://github.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability/tree/main/docs)
- [Network topology drawing](https://github.com/Neloy4321/Enterprise-Multi-Branch-Network-with-High-Availability/blob/main/topology/Enterprise-Network.png)

**Scope:** This is a **simulated enterprise network lab**. It is not a production deployment or a claim of continuous business-network operation.

---

[← Profile](../../README.md) · [All public projects](../PROJECT_ATLAS.md) · [Data case study](./DATA_PIPELINE.md)
