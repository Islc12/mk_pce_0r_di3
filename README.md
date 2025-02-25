### John the Ripper formatting automation script

-------------------------------------------------------------------------------------------------------------------------------------------

### Disclaimer

This project includes the `rockyou.txt` wordlist for use with John the Ripper for educational and security testing purposes only.
Unauthorized use of this script or the wordlist to attack systems without permission is illegal and unethical. The creator of this
repository is not responsible for any misuse of the provided tools. Ensure you have explicit permission from the owner of any system you
are testing.

By using this repository, you agree to use it responsibly and comply with all relevant laws and regulations.

-------------------------------------------------------------------------------------------------------------------------------------------

Author: Rich Smith

Written: Dec 2024

Contact: richrsmith@proton.me

-------------------------------------------------------------------------------------------------------------------------------------------

### Installation and setup instructions:
```
$ git clone https://github.com/Islc12/mk_pce_0r_di3.git
$ cd mk_pce_0r_di3
$ chmod u+x config.sh
$ ./config.sh
```

### Running the script:
```
$ cd mk_pce_0r_di3
$ ./john_automate.py
```

-------------------------------------------------------------------------------------------------------------------------------------------

### How to use:
Usage is fairly simple for this script, you'll be presented with a series of prompts before the script begins to run. The first prompt will
ask about the hash file(s) you wish to use, input one or one hundred, just ensure that files are separated by a space. The second prompt
will ask about wordlists and which you'd like to run. Selecting (1) picks the default John the Ripper wordlist and can take quite a long
time to run, this is here because John provides us that utility and I don't want to take anything away from the original developers. Choice
(2) lets us run the gold standard for wordlists, the rockyou word list. Choice (3) allows us to input a custom wordlist, if we select (3)
then we're immediately prompted for the input of that wordlist. -NOTE- users have the option to add multiple wordlists in this script, it
will check them against the hash file(s) one by one, parsing each time through all available formats. The third and final prompt asks about
forking the processor. If you know what this part does I doubt I'd have to explain it to you, if you don't know what it does, choose the
default setting and save your system from potentially overheating. After this just sit back and let John the Ripper do its thing. When John
finishes running any and all cracked hashes will be shown to standard output. As John already does, cracked hashes are stored in
~/.john/john.pot in case you need to go back and view them at a later time.

This script was written as means to automate the formatting process within John the Ripper. John boasts an impressive number of 
formatting options available to the user, however, an issue with this is if the user is attempting to break a large number of hashes
with multiple format types within the same (or multiple files) John may not be able to run without specifiying the `--format-<format type>`
option. Leaving users to have to go back and manually run the program wasting valuble time and resources. This script allows the user
to run John the Ripper without having to manually run these various formats against a single or even multiple files. 

The script has also been modified to give the user the ability to input a custom wordlist (or multiple wordlists), use the default 
John wordlist, or even just use the industry standard rockyou.txt wordlist.. 

Additionally more functionality has been given the script allowing the user to change the processor fork of John. 
At this time I have not added checks to that functionality so it is up to the user to know what the maximum for is their 
system in capable of if they choose to use the "custom" option. Otherwise using the "high performance" option will give the script the
power to determine maximum system capabilities. Likewise if the user choose the utilize the "low performance" option this will utilize the
default fork value which is 1. Truth be told there isn't a signficant difference between the default and a fork of 8, in fact it without
proper cooling I probably wouldn't recommend altering the fork value. 

One key aspect that I did be sure to add to this program is the ability to use \*nix style globbing. I detest having to type out complex
named directories or files, and like many I'll often mistype these complex names, simply adding globbing was a way for me to keep some
of my own sanity when typing out long and complex directory/file names.

-------------------------------------------------------------------------------------------------------------------------------------------

### Future Changes:
-ADD dyanimc formatting option - help for this can be found in the /usr/share/doc/john/DYNAMIC\_SCRIPTING README file.

-ADD more wordlists to the wordlist selection tab, this will require me to package these custom wordlists with the script.

-ADD dynamic modification to the format list, this will ensure as John the Ripper developers continue to work on the program this 
    script will be capable of keeping the format list up to date without manual modification.
