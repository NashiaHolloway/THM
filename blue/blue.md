# Blue
3/15/20

## Task 1: Recon
nmap scan: `nmap -sV -sC -oN blue_nmap.txt 10.10.150.229`

OS: Windows 7 Pro Service Pack 1; computer name is Jon-PC

Interesting Ports: 445 (SMB), 3389 (RDP)

nmap vuln scan: `nmap -Pn --script vuln -oN blue_vuln.txt 10.10.150.229`

Vulnerabilities: CVE-2012-0152 (RDP DoS), CVE-2012-0002 (RDP RCE), MS17-010 (Eternalblue)

We'll attempt to exploit the eternalblue vulnerability in SMBv1.

## Task 2: Gain Access
Starting metasploit (>msfconsole) and running a search for MS17-010 gives us the path to the exploit we're going to run: exploit/windows/smb/ms17_010_eternalblue. We only need to set the RHOST in order to use it. Running the exploit gives us a reverse shell. Easy peasy.

## Task 3: Escalate
Use the shell to meterpreter to upgrade shells (post/multi/manage/shell_to_meterpreter). Set the session ID to upgrade. Once finished, in a command shell, verify we're system with `whoami` command. List all processes with `ps` and take note of a process running as system (2648, conhost.exe). In the meterpreter shell, run `migrate 2648` to move into the conhost.exe process.

## Task 4: Cracking
After running `hashdump` in the meterpreter shell, the only non-default user is Jon: `Jon:1000:aad3b435b51404eeaad3b435b51404ee:ffb43f0de35be4d9917ac0cc8ad57f8d:::`. We copy his hash into a text file (ffb43f0de35be4d9917ac0cc8ad57f8d) and name it password.hash. To crack it, we use hashcat with the `-m 1000` switch to signify an NTLM password. We use the rockyou.txt found in `usr/share/manage/wordlsits/`. The password is found to be `alqfna22`.
