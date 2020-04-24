# Linux Fundamentals

I've already done the first three rooms for this and didn't take notes. Better late than never.

## Common Linux Privesc

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
