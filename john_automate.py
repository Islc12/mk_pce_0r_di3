#!/usr/bin/env python3

import os
import subprocess
import glob
import time

sys_fork = subprocess.check_output(["nproc", "--all"], text=True).strip()

format_types = [
    "descrypt", "bsdicrypt", "md5crypt", "md5crypt-long", "bcrypt", "scrypt", "LM", "AFS",
    "tripcode", "AndroidBackup", "adxcrypt", "agilekeychain", "aix-ssha1", "aix-ssha256",
    "aix-ssha512", "andOTP", "ansible", "argon2", "as400-des", "as400-ssha1", "asa-md5",
    "AxCrypt", "AzureAD", "BestCrypt", "BestCryptVE4", "bfegg", "Bitcoin", "BitLocker",
    "bitshares", "Bitwarden", "BKS", "Blackberry-ES10", "WoWSRP", "Blockchain", "chap",
    "Clipperz", "cloudkeychain", "cq", "CRC32", "cryptoSafe", "sha1crypt",
    "sha256crypt", "sha512crypt", "Citrix_NS10", "dahua", "dashlane", "diskcryptor",
    "Django", "django-scrypt", "dmd5", "dmg", "dominosec", "dominosec8", "DPAPImk",
    "dragonfly3-32", "dragonfly3-64", "dragonfly4-32", "dragonfly4-64", "Drupal7",
    "eCryptfs", "eigrp", "electrum", "EncFS", "enpass", "EPI", "EPiServer", "ethereum",
    "fde", "Fortigate256", "Fortigate", "FormSpring", "FVDE", "geli", "gost", "gpg",
    "HAVAL-128-4", "HAVAL-256-3", "hdaa", "hMailServer", "hsrp", "IKE", "ipb2",
    "itunes-backup", "iwork", "KeePass", "keychain", "keyring", "keystore",
    "known_hosts", "krb4", "krb5", "krb5asrep", "krb5pa-sha1", "krb5tgs", "krb5-17",
    "krb5-18", "krb5-3", "kwallet", "lp", "lpcli", "leet", "lotus5", "lotus85", "LUKS",
    "MD2", "mdc2", "MediaWiki", "monero", "money", "MongoDB", "scram", "Mozilla",
    "mscash", "mscash2", "MSCHAPv2", "mschapv2-naive", "krb5pa-md5", "mssql",
    "mssql05", "mssql12", "multibit", "mysqlna", "mysql-sha1", "mysql", "net-ah",
    "nethalflm", "netlm", "netlmv2", "net-md5", "netntlmv2", "netntlm", "netntlm-naive",
    "net-sha1", "nk", "notes", "md5ns", "nsec3", "NT", "o10glogon", "o3logon",
    "o5logon", "ODF", "Office", "oldoffice", "OpenBSD-SoftRAID", "openssl-enc",
    "oracle", "oracle11", "Oracle12C", "osc", "ospf", "Padlock", "Palshop", "Panama",
    "PBKDF2-HMAC-MD4", "PBKDF2-HMAC-MD5", "PBKDF2-HMAC-SHA1", "PBKDF2-HMAC-SHA256",
    "PBKDF2-HMAC-SHA512", "PDF", "PEM", "pfx", "pgpdisk", "pgpsda", "pgpwde", "phpass",
    "PHPS", "PHPS2", "pix-md5", "PKZIP", "po", "postgres", "PST", "PuTTY", "pwsafe",
    "qnx", "RACF", "RACF-KDFAES", "radius", "RAdmin", "RAKP", "rar", "RAR5",
    "Raw-SHA512", "Raw-Blake2", "Raw-Keccak", "Raw-Keccak-256", "Raw-MD4", "Raw-MD5",
    "Raw-MD5u", "Raw-SHA1", "Raw-SHA1-AxCrypt", "Raw-SHA1-Linkedin", "Raw-SHA224",
    "Raw-SHA256", "Raw-SHA3", "Raw-SHA384", "restic", "ripemd-128", "ripemd-160",
    "rsvp", "RVARY", "Siemens-S7", "Salted-SHA1", "SSHA512", "sapb", "sapg", "saph",
    "sappse", "securezip", "7z", "Signal", "SIP", "skein-256", "skein-512", "skey",
    "SL3", "Snefru-128", "Snefru-256", "LastPass", "SNMP", "solarwinds", "SSH",
    "sspr", "Stribog-256", "Stribog-512", "STRIP", "SunMD5", "SybaseASE",
    "Sybase-PROP", "tacacs-plus", "tcp-md5", "telegram", "tezos", "Tiger",
    "tc_aes_xts", "tc_ripemd160", "tc_ripemd160boot", "tc_sha512", "tc_whirlpool",
    "vdi", "OpenVMS", "vmx", "VNC", "vtp", "wbb3", "whirlpool", "whirlpool0",
    "whirlpool1", "wpapsk", "wpapsk-pmk", "xmpp-scram", "xsha", "xsha512", "zed",
    "ZIP", "ZipMonster", "plaintext", "has-160", "HMAC-MD5", "HMAC-SHA1",
    "HMAC-SHA224", "HMAC-SHA256", "HMAC-SHA384", "HMAC-SHA512", "dummy", "crypt"
    # "dynamic_n" - see /usr/share/doc/john/DYNAMIC_SCRIPTING README file for usage on this
    # for now we'll just not include this in the script, perhaps we'll adjust later on
    ]

def resolve_files(input_paths):
    resolved_paths = []
    for path in input_paths:
        resolved_paths.extend(glob.glob(os.path.expanduser(path.strip())))
    return resolved_paths

def john_init():
    try:
        # Input hash files
        hash_files = input("Enter the hash files you wish to use, separated by spaces: ").split()
        target_files = resolve_files(hash_files)

        if not target_files:
            print("No valid hash files found.")
            exit(1)

        # Select wordlist
        print("""Choose a wordlist:
        1. John the Ripper Default wordlist
        2. Rockyou wordlist
        3. Custom wordlist(s)""")
        choice = int(input("Your choice: "))
        wordlist_target = []

        if choice == 1:
            wordlist_target = None  # Default John wordlist
        elif choice == 2:
            rockyou_path = "rockyou.txt"
            if os.path.exists(rockyou_path):
                wordlist_target = [rockyou_path]
            else:
                print("Rockyou wordlist not found.")
                exit(1)
        elif choice == 3:
            custom_wordlists = input("Enter custom wordlist paths, separated by spaces: ").split()
            wordlist_target = resolve_files(custom_wordlists)
            if not wordlist_target:
                print("No valid wordlists found.")
                exit(1)
        else:
            print("Invalid choice. Exiting.")
            exit(1)


        print(f"""Select a fork option:
        1. Default
        2. System {sys_fork}
        3. Other""")

        selection = int(input("Your Choice: "))
        
        if selection == 1:
            fork = None # Default John fork
        elif selection == 2:
            fork = sys_fork
        elif selection == 3:
            fork = int(input("Enter the amount to fork processor: "))
        else:
            print("Invalid choice. Exiting.")
            exit(1)

        return target_files, wordlist_target, fork

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def check_formats(target_files):
    for target_file in target_files:
        command = ["john", "--show=formats"] + target_files
        output = subprocess.check_output(command, text=True)

    matching_formats = []
    for line in output.splitlines():
        for formats in format_types:
            if formats in line:
                matching_formats.append(formats)

    # Remove duplicates (if a format appears multiple times)
    matching_formats = list({formats for formats in matching_formats})
    return matching_formats

def john_format(target_files, wordlist_target, fork, matching_formats):
    #count = 0
    #counter = len(wordlist_target) * len(target_files) * len(matching_formats)
    start_time = time.time()

    for wordlist in wordlist_target:
        print(f"\nProcessing...")
        for target_file in target_files:
            for index, matches in enumerate(matching_formats, start=1):
                wordlist_args = [f"--wordlist={wordlist}"]
                command = ["john", f"--format={matches}", target_file] + wordlist_args
                elapsed_time = time.time() - start_time
                mins = int(elapsed_time // 60)
                secs = int(elapsed_time % 60)
                print(f"\rTotal Time: {mins:03}:{secs:02}, Processing format: {index}/{len(matching_formats)}", end='', flush=True)
                if fork:
                    command.append([f"--fork={fork}"])
                
                john_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = john_process.communicate()

                if "No password hashes left" in stdout:
                    continue
                
                if john_process.returncode != 0 and "No password hashes left" not in stdout:
                    print(f"Error using format {matches} on {target_file}: {stderr}")

def john_show(target_files):
    print("""
\n----------------------------------------------------------------------------\n
Final cracked hashes:\n""")
    for target_file in target_files:
        john_output = subprocess.run(["john", "--show", target_file], text=True, capture_output=True)
        print(john_output.stdout.strip())
        print("\n----------------------------------------------------------------------------\n")
if __name__ == "__main__":
    target_files, wordlist_target, fork = john_init()
    matching_formats = check_formats(target_files)
    john_format(target_files, wordlist_target, fork, matching_formats)
    john_show(target_files)
