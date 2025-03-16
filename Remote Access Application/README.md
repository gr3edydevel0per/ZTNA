# OwlGuard - Secure Remote Access Application

## Overview
**OwlGuard** is an application designed to provide secure remote access to enterprise resources. It ensures **strong authentication**, **device posture validation**, and **device authorization**  with **multi-factor authentication**to mitigate security risks.

## Features
- **User Authentication** – Secure login via the desktop application.
- **Device Compliance Check** – Assesses system security before granting access.
- **Automated VPN Setup** – Fetches user-specific configurations and connects via OpenVPN.
- **Centralized Management** – Allows administrators to monitor users and manage access.
- **Certificate-Based Security** – Uses EasyRSA for strong encryption and authentication.

## Workflow
1. **User Login** – The user provides credentials via the OwlGuard application.
2. **Device Posture Evaluation** – The application checks compliance (e.g., OS updates, antivirus status, security policies).
3. **Access Decision** – If the device meets security standards, the VPN configuration is retrieved.
4. **Secure VPN Connection** – OpenVPN Connect is launched for establishing a secure tunnel.
5. **Device Authorization** - Server checks whether the request if comming from authorized device or not
6. **Access Monitoring** – Administrators can oversee active connections and revoke access if necessary.




<img src="https://raw.githubusercontent.com/gr3edydevel0per/ZTNA/refs/heads/main/Remote%20Access%20Application/Assets/images/login.png">


<img src="https://raw.githubusercontent.com/gr3edydevel0per/ZTNA/refs/heads/main/Remote%20Access%20Application/Assets/images/landing.jpg">

<img src="https://raw.githubusercontent.com/gr3edydevel0per/ZTNA/refs/heads/main/Remote%20Access%20Application/Assets/images/con.png">
