# Blue Primer: Splunk - Part2

I'll be sticking with the "botsv1" index for part 2.

## Task 6: Ransomware

**What was the most likely IP address of we8105desk on 24AUG2016?**

We don't yet know what sourcetype will be best, so we need to gather more info to move foreward.

```SQL
index="botsv1" we8105desk
| dedup sourcetype
| table sourcetype
```
We get 8 results. Checking the suricata sourcetype, there are 2 DNS events. The destination IP is the answer: `192.168.250.100`.

**What is the name of the USB key inserted by Bob Smith?**

To find USB data, we can take the previous search and swap out the computer name for "USB". There are 4 sourcetypes. 

The friendlyname value will give us the name of the USB plugged in. Checking the `WinRegistry` sourcetype will give us the answer.

```SQL
index="botsv1" sourcetype="winregistry" "friendlyname"
```
There are 2 results. Looking at the first one, the `registry_value_field` shows the answer is `MIRANDA_PRI`. Take a note of the time this event occurs: 24 Aug 2016 at 16:42:17.

**After the USB insertion, a file execution occurs that is the initial Cerber infection. This file execution created two additional processes. What is the name of the file?**

```SQL
index="botsv1" sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational" Miranda
```
Searching part of the USB name within the Sysmon events shows the file executed pretty quickly: `Miranda_Tate_unveiled.dotm`. Dotm extensions are for macro-enabled documents. 

**During the initial Cerber infection a VB script is run. The entire script from this execution, pre-pended by the name of the launching .exe, can be found in a field in Splunk. What is the length in characters of this field?**

Visual Basic scripts have the extension .vbs. It looks like the script can be seen in the command line field of the sysmon data.

```SQL
index="botsv1" sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational" .vbs
| eval len=len(CommandLine)
| table CommandLine len
```

**Bob Smith's workstation (we8105desk) was connected to a file server during the ransomware outbreak. What is the IP address of the file server?**


**What is the first suspicious domain visited by we8105desk on 24AUG2016?**


**The malware downloads a file that contains the Cerber ransomware cryptor code. What is the name of that file?**


**The parent process ID of 121214.tmp?**


**Amongst the Suricata signatures that detected the Cerber malware, what signature ID alerted the fewewst number of times?**


**The Cerber ransomware encrypts files located in Bob Smith's Windows profile. How many .txt files does it encrypt?**


**How many distinct PDFs did the ransomware encrypt on the remote file server?**


**What FQDN does the Cerber ransomware attempt to direct the user to a the end of its encryption phase?**
