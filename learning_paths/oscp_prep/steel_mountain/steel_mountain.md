# Steel Mountain

> Nashia Holloway | April 30th, 2020

## Task 1 Introduction

**1. Who is the employee of the month?**

`Bill Harper` is the employee of the month. I was going to do a reverse image search, but looking at the source code had the name there as the image. Plus, I've see Mr. Robot.

## Task 2 Initial Access

**1. What is the other port running a web server on?**

```
nmap -sC -sV -A $IP -oN initial.nmap
```

`8080`

**2. For the other web server, what file server is running?**

NAvigating to $IP:8080 returns a landing page for HFS. Googling HFS returns a [website](https://www.rejetto.com/hfs/). The file server is a `rejetto http file server`.

**3. What is the CVE number to exploit this file server?**

The version number is 2.3

```
searchsploit rejetto http file server 2.3
```

There are 4 results. The CVE related this this exploit is `2014-6287`

**4. Use metasploit to get an initial shell. What is the user flag?**

`search 2014-6287` to find the exploit. Set variables, and run it. The user flag is in C:\Users\bill\Desktop.

## Task 3 Privilege Escalation

Follow the steps.
