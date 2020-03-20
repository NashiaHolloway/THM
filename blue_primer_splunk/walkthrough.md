# Blue Primer: Splunk
I won't go into tasks 1-4, as they should be accomplished by yourself. I wanted to show my though process of creating searches based on what information I need to find.

## Task 5: Advanced Persistent Threat
I first like to get an idea of the data I'm working with, by doing the following search:
```SQL
index=* sourcetype=* 
| dedup index sourcetype 
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
Digging deeper with the above search shows us that the same IP address makes "GET" and "POST" requests way more often than the `23.22.63.114` address. [more about request methods here](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
2. What web scanner scanned the server?

3. What is the IP address of our web server?

4. What content management system is imreallynotbatman.com using?

5. What address is performing the brute-forcing attack against our website?

6. What is the first password attempted in the attack?

7. One of the passwords in the brute force attack is James Brodsky's favorite Coldplay song. Which six character song is it?

8. What was the correct password for admin access to the content management system running imreallynotbatman.com?

9. What was the average password length used in the password brute forcing attempt rounded to closest whole integer?

10. How many seconds elapsed between the time the brute force password scan identified the correct password and the compromised login rounded to 2 decimal places?

11. How many unique passwords were attempted in teh brute force attempt?

12. What is the name of the executable uploaded by p01s0n1vy?

13. What is the MD5 hash of the executable uploaded?

14. What is the name of the file that defaced the imreallynotbatman.com website?

15. This attack used dynamic DNS to resolve the malicious IP. What fully qualified domain name (FQDN) is associated with this attack?

16. What IP address has P01s0n1vy tied to domains that are pre-staged to attack Wayne Enterprise?

17. Based on the data gathered from this attack, and common open source intelligence sources for domain names, what is the email address that is most likely associated with P01s0n1vy APT group?

18. GCPD reported that common TTPs for the P01s01vy APT group if initial compromise fails is to send a spear phishing email with custom malware attached to their intended target. This malware is usually connected to P01s0n1vy's initial attack infrastructure. Using research techniques, provide the SHA256 hash of this malware.

19. What special hex code is associated with the custom malware discussed on the previous question?

20. What does this hex code mean?

## Task 6: Ransomware

