# CylanceGlobalList

Based on a current Cylance Global List functionality, it [only supports SHA256 format](https://docs.blackberry.com/en/unified-endpoint-security/cylance--products/blackberry-on-prem-administration-guide/Global_Lists/Add_a_Global_List_Entry). Of course, issue starts when it comes to adding relevant hashes (often times not SHA256), since the only option to find SHA256 equivalent (if there is such) as well as its coverage & detection status – is by going to VirusTotal and manually copy/pasting… while as of now, unfortunately, nothing being offered by the vendor - Balckberry/Cylance in that regard.. which is sad, especially often times considering engine versions difference (VT vs local endpoint) and a huge amount of hashes to be verified.

Anyways, to automate above, this simple python script does the following:

- as an input takes a file with a list of hashes (various formats)
- queries Virus Total (API V2), looking for ‘sha256’ JSON field in reply.
- if SHA256 hash from the input was not found in VT ('No matches found') - script will still display that SHA256 hash (makes sense to consider it for Global List).
- if SHA256 hash from the input was found in VT, AND/OR a non-SHA256 hash has SHA256 equivalent in VT – next, script checks JSON fields related to Cylance, looking for ‘Not found’ and ‘Undetected’ scenarios (also candidates for Global list).
- in case of ‘Unable to process file type’ / ‘Timeout’ / ’Confirmed timeout’ statuses, regardless of hashes - since we can’t be 100% sure how Cylance treats them, whether those are indeed hash format or maybe other handling issues, such hashes are not displayed.

There are no prerequisites other than list of hashes as an input.txt, python and those two libraries installed:
```
pip install requests
```
```
pip install pywin32
```

Usage:
```
python vt.py -h
```
```
python vt.py -k Virus Total personal API key -i input.txt
```
![Screenshot](demo.png)
