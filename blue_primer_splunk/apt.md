# Blue Primer: Splunk - Part1
I won't go into tasks 1-4, as they should be accomplished by yourself. I wanted to show my though process of creating searches based on what information I need to find. Also, I started out using the "main" index, and switched to "botsv1", so if one search doesn't work, try the other index.

## Task 5: Advanced Persistent Threat
I first like to get an idea of the data I'm working with, by doing the following search:
```SQL
index=* sourcetype=* 
| dedup sourcetype 
| table sourcetype
```
Making sure our time picker is set to "All Time", we see that there is only one index: `main`, and 21 different sourcetypes.

**What IP is scanning our web server?**

There is a sourcetype for `iis`, which is a Microsoft web server, so we'll start there. Looking at the fields, we get a `c_ip`, which is the address of the client that accessed the server. 
```SQL
index="main" sourcestype="iis"
| stats count by c_ip
```
This search shows us that the `40.80.148.42` IP address hit the web server 20967 times, which is way more than the other 4 IP addresses that touched the server.
```SQL
index="main" sourcetype="iis"
| stats count by c_ip cs_method
```
Digging deeper with the above search shows us that the same IP address makes "GET" and "POST" requests way more often than the `23.22.63.114` address. [More about request methods here](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol)

**What web scanner scanned the server?**

`Acunetix` scanned the server. This can be seen in the last search. In searching that `cs_method`, Acunetic came up as a website vulnerability scanner.

**What is the IP address of our web server?**

By adding the `s_ip` field to our search after `cs_method` in stats count, we see out source IP is `192.168.250.70`.

**What content management system is imreallynotbatman.com using?**

```SQL
index ="main" sourcetype="iis" imreallynotbatman.com
| dedup cs_Referer
| table cs_Referer
```
Looking at the [`cs_referer`](https://www.techopedia.com/definition/1583/referrer) data, we see that [`joomla`](https://www.joomla.org/about-joomla.html) which after googling what it is, is the content management system.

**What address is performing the brute-forcing attack against our website?**

Switching gears, the sourcetype `stream:http` looks as though it'll give us the data we need to answer the next few questions. Between POST and GET requests, brute forcing passwords will most likely be carried out with POST requests. Looking at the search from the first question, `40.80.148.42` makes the most POST requests, but it isn't the answer. `23.22.63.114` is the only other host that makes POST requests, and this is the answer. But why? The only thing I can think of is that brute forcing the password didn't take that many tries. And now that I think of it, the other IP address had a lot of "debugging" and "vulnerability scanning" methods, making me think an admin was using it to make sure the web server was patched. I'm on the fence at this point as to whether or not the 40.80 IP is malicious or not. But then again, an admin would probably run those tools within the environment, not externally.

**What is the first password attempted in the attack?**

Looking through the `stream:http` fields, `src_content` looks the most promising. It has username and password information in it. Let's get crazy and try to do some [regex](https://www.rexegg.com/regex-quickstart.html) to extract what we need, so we don't have to look at all that other junk.

```SQL
index="botsv1" sourcetype="stream:http" src_ip="23.22.63.114" form_data!\=""
| rex field=form_data "username=(?<uname>[^&]+)\\&"
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| table src_ip uname pass dest_ip endtime
| sort endtime
```
The above regex can be made into one line, so a good exercise would be trying to figure out how to do that. (read: I didn't feel like doing it, but you can). To extract the username, the expression reads: From the `form_data` field, put whatever is after "usrname=" into the `uname` field, grabbing everything that isn't an `&`. Stop looking for a match when you reach an `&`.

Extracting the password is the same, however, at the end there is an asterisk meaning there may be "zero or more" `&`'s to grab. This takes into account that some of the data in `form_data` ends after "passwd" and sometimes it continues on to a string of letters and numbers.

Sorting by the `endtime` shows us that the first password attempted is `12345678`

**One of the passwords in the brute force attack is James Brodsky's favorite Coldplay song. Which six character song is it?**

Building off the last search, we can show which passwords are 6 characters in length.

```SQL
index="botsv1" sourcetype="stream:http" src_ip="23.22.63.114" form_data!\=""
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| eval chars=len(pass)
| where chars = 6
| sort pass
```
This search limits us to only 6 character long passwords, but there are still 213 of them. I tried looking up who James Brodsky is with no luck, and tried to figure out how to search a page by character count, with no luck either. I resorted to manually going through the [list of Coldplay songs](https://en.wikipedia.org/wiki/List_of_songs_recorded_by_Coldplay) and checking if I saw any in Splunk. It helped that both lists were in alphabetical order. The only two were "Voodoo" and "Yellow". The answer is the latter. (haha, a lesson in differentiating "former" and "latter").

**What was the correct password for admin access to the content management system running imreallynotbatman.com?**

The Joomla content management system running imnotreallybatman.com sits at `192.168.250.70`. 

```SQL
index="botsv1" sourcetype="stream:http" dest_ip="192.168.250.70" uri="*administrator*"
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| where pass!\=""
| table dest_ip pass uri
```
Upon completing this search my eye automatically finds `batman`. Seems fitting that this is the right answer given the name of the website. It is the right answer, but let's pretent we just make an educated guess and build a more solid case as to why.

```SQL
index="botsv1" sourcetype="stream:http" dest_ip="192.168.250.70" uri="*administrator*"
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| where pass!\=""
| stats count(uri) AS uri by pass
| table pass uri
| sort -uri``
This search give us solid proof. The password `batman` was the most used password, meaning the attacker probably tried it once, bruteforcing, and once they saw it worked, logged in with it again.

**What was the average password length used in the password brute forcing attempt rounded to closest whole integer?**

```SQL
index="botsv1" sourcetype="stream:http" src_ip="23.22.63.114" form_data!\=""
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| eval chars=len(pass)
| stats avg(chars) as average by dest_ip
| table average
```
The answer is `6`.

**How many seconds elapsed between the time the brute force password scan identified the correct password and the compromised login rounded to 2 decimal places?**

To answer this, we can use part of the last search. We know the conpromised password was "batman", so we'll have to narrow the search on that and look at the `_time` field.

```SQL
index="botsv1" sourcetype="stream:http"
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| search pass="batman"
| stats earliest(_time) as first_try, latest(_time) as second_try
| eval diff=second_try - first_try
| table first_try second_try diff
```
The difference in seconds rounded to 2 decimal places is `92.17`.

**How many unique passwords were attempted in the brute force attempt?**

```SQL
index="botsv1" sourcetype="stream:http"
| rex field=form_data "passwd=(?<pass>[^&]+)\\&*"
| dedup pass
| stats count by pass
| stats sum(count)
```
Deduping the password field gives us all the unique entries. Counting the entries only gives us 1 per password (since they're all unique), then calculating the sum gives us the total of all uniqie passwords: `412`.

**What is the name of the executable uploaded by p01s0n1vy?**

The compromised host was `192.168.250.70` where the content management sits. I'm not sure the sourectype we've been using is the best one for the job, so we're going to reassess.

```SQL
index=botsv1 sourcetype=* *.exe*
| dedup sourcetype
| table sourcetype
```
Switching to "Smart Mode" makes this search faster. We get 8 results. Poking through them, it looks like `fgt_utm` and `suricata` are our best options. Looking them up, the [Fortinet Unified Thream Management (UTM)](https://www.fortinet.com/products/smallbusiness/utm/overview.html) is where `ftg_utm` comes from. [Suricata](https://suricata-ids.org/) is an intrusion detection system. Just because of the order I searched, I found the answer using the `ftg_utm` sourcetype, but looking through Suricata, you could also get the answer through there.

```SQL
index="botsv1" sourcetype="fgt_utm" filename="*.exe" dstip="192.168.250.70"
| table filename dstip
```
The answer is `3791.exe`.

**What is the MD5 hash of the executable uploaded?**

Using the above search, another field under that sourcetype is `file_hash`. Unfortunately, it doesn't look like an MD5 hash (too long). I'm guessing it's a SHA256 one. We have to take another approach. Looking through the list of sourcetypes associated with `3791.exe`, we have 5 options.

```SQL
index=botsv1 sourcetype=* *3791.exe*
| dedup sourcetype
| table sourcetype
```
Sysmon is always a good source of information related to processes. Plus, I've already looked through the others.

```SQL
index="botsv1" sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational" process_name="3791.exe"
| sort _time
| table process_name MD5 _time
```
This search doesn't give us our final answer because there are too many different hashes for the `3791.exe` process. We need to find the first instance of the process and that'll give us our hash. Even sorting by time doesn't help, because there are multiple hashes in one second.

The Sysmon event code 1 is for process creation. Adding that little bit of information gives us our answer.

```SQL
index="botsv1" sourcetype="XMLWinEventLog:Microsoft-Windows-Sysmon/Operational" process_name="3791.exe" EventCode=1
| table process_name MD5
```

**What is the name of the file that defaced the imreallynotbatman.com website?**

For this question, it's important to think about the order of events of the attack. The web server was first compromised and an executable was executed. From there, the compromised server reaches out to an external site to GET a file (the file that defaces the imnotreallybatman.com website). 

```SQL
index="botsv1" sourcetype="stream:http" src_ip="192.168.250.70"
| table dest_ip request site
```
6 requests are to `update.joomla.org`, and 2 are for the `prankglassinebracket.jumpingcrab.com:1337` (anything having to do with 1337 or variations thereof should be suspicious in security related events) for a jpeg file.

**This attack used dynamic DNS to resolve the malicious IP. What fully qualified domain name (FQDN) is associated with this attack?**

The answer is shown with the previous search: `prankglassinebracket.jumpingcrab.com`.

**What IP address has P01s0n1vy tied to domains that are pre-staged to attack Wayne Enterprise?**

This answer can also be seen with the last search: `23.22.63.114`.

**Based on the data gathered from this attack, and common open source intelligence sources for domain names, what is the email address that is most likely associated with P01s0n1vy APT group?**

Popping the domain name into [ThreatCrowd](www.threatcrowd.org) gives domain names and associated IP addresses for it. We pivot to Po1s0n1vy.com and from there we can pivot to Wyncorpinc.com (related to the batman theme). The email adress associated with this domain is the answer: `Lillian.Rose@po1s0n1vy.com`.

**GCPD reported that common TTPs for the P01s01vy APT group if initial compromise fails is to send a spear phishing email with custom malware attached to their intended target. This malware is usually connected to P01s0n1vy's initial attack infrastructure. Using research techniques, provide the SHA256 hash of this malware.**

We can use [ThreatMiner](www.threatminer.org) to find the SHA256 hash. Searching on the `23.22.63.114` IP address show the MD5 of the associated malware. Clicking that link leads us to the hash we need.

**What special hex code is associated with the custom malware discussed on the previous question**

Staying on the same page, we can click the "Related resources" link for VirusTotal. Under the "Community" tab, there is a comment that holds the hex code.

**What does this hex code mean?**

Popping it into hex to ASCII converter gives you the answer: "Steve Brant's Beard is a powerful thing. Find this message and ask him to buy you a beer!!!"

## Task 6: Ransomware

