# Blaster

> Nashia Holloway | May 8th, 2020

## Task 2 Activate Forward Scanners and Launch Proton Torpedoes

Ports 80 and 3389 are open. Navigating to the website, there is an IIS windows server running. 

```
gobuster dir -u http://10.10.129.197 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
```
Reveals the `/retro` directory. Turns out this is basically the same as the "retro" box I just did, so I'll stop taking notes now.
