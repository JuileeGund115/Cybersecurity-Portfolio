# Nmap VSFTPD Project

This project demonstrates a basic Nmap scanning workflow followed by exploitation using Metasploit on a vulnerable vsFTPd 2.3.4 service.

## Steps

### 🚀 Step 1: Discover if the Target is Up (Host Discovery)
```
nmap -sn 192.168.25.128 -oN scans/01-host-discovery.txt
```
![Host Discovery](screenshots/kali1.png)

### 🔥 Step 2: Full TCP Port Scan
```
nmap -p- -T4 192.168.25.128 -oN scans/02-full-port-scan.txt
```
![Full Port Scan](screenshots/kali2.png)

### Step 3: Service & Version Detection
```
nmap -sC -sV -p- 192.168.25.128 -oN scans/03-service-detection.txt
```
![Service Detection](screenshots/kali3.png)
![Service Detection](screenshots/kali4.png)

### Step 4: Vulnerability Scanning with NSE
```
nmap --script vuln -p 21,22,23,25,53,80,111,139,445,3306 192.168.25.128 -oN scans/04-vuln-scan.txt
```
![Vulnerability Scan](screenshots/kali5.png)
![Vulnerability Scan](screenshots/kali6.png)

## Tools Used

- Nmap
- Metasploit (for exploiting vsFTPd 2.3.4 backdoor)

## Notes

Educational purpose only. Do not use on unauthorized systems.
