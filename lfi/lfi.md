# LFI

> Nashia Holloway | May 11th, 2020

## Enumeration

Similar to the Inclusion box (probably should've done this one first), we have a LFI vulnerability.

`http://10.10.156.96/home?page=../../../../etc/passwd` shows the passwd file at the bottom of the webpage (have to scroll). There's the user Falcon, but we need the password. Hashes are kept in /etc/shadow and we have access, fortunately. So we can attempt to crack Falcon's password hash.

```
sudo john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

## Initial Access

I put the shadow line in the "hash" file for John to crack. We have success and can now ssh into the box as the Falcon user.

## Privilege Escalation

The Falcon user can run `journalctl` with sudo privs, allowing us to get root.

```
sudo journalctl
!/bin/sh
```

