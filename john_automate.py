#!/usr/bin/env python3

import os
import subprocess
import glob

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
        2. Rockyou wordlist (/usr/share/wordlists/rockyou.txt)
        3. Custom wordlist(s)""")
        choice = int(input("Your choice: "))
        wordlist_target = []

        if choice == 1:
            wordlist_target = None  # Default John wordlist
        elif choice == 2:
            rockyou_path = "/usr/share/wordlists/rockyou.txt"
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


        print("""Select a fork option:
        1. Default
        2. Fork 2
        3. Fork 4
        4. Other""")

        selection = int(input("Your Choice: "))
        
        if selection == 1:
            fork = None # Default John fork
        elif selection == 2:
            fork = 2
        elif selection == 3:
            fork = 4
        elif selection == 4:
            fork = int(input("Enter the amount of fork you wish to you: "))
        else:
            print("Invalid choice. Exiting.")
            exit(1)

        return target_files, wordlist_target, fork

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def john_format(target_files, wordlist_target, fork):
    format_types = [
        "descrypt", "bsdicrypt", "md5crypt", "md5crypt-long", "bcrypt", "scrypt", "LM", "AFS",
        "tripcode", "AndroidBackup", "adxcrypt", "agilekeychain", "aix-ssha1", "aix-ssha256",
        "aix-ssha512", "andOTP", "ansible", "argon2", "as400-des", "as400-ssha1", "asa-md5",
        "AxCrypt", "AzureAD", "BestCrypt", "BestCryptVE4", "bfegg", "Bitcoin", "BitLocker",
        "bitshares", "Bitwarden", "BKS", "Blackberry-ES10", "WoWSRP", "Blockchain", "chap",
        "Clipperz", "cloudkeychain", "dynamic_n", "cq", "CRC32", "cryptoSafe", "sha1crypt",
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
        ]

    for target_file in target_files:
        print(f"\nProcessing: {target_file}")
        for formats in format_types:
            command = ["john", f"--format={formats}", target_file]
            if fork:
                command.extend([ f"--fork={fork}"])
            if wordlist_target:
                for wordlist in wordlist_target:
                    command.extend([f"--wordlist={wordlist}"])

            john_process = subprocess.run(command, text=True, capture_output=True)

            if john_process.returncode != 0 and "No password hashes left" not in john_process.stdout:
                print(f"Error using format {formats} on {target_file}: {john_process.stderr}")

def john_show(target_files):
    print("\nFinal cracked hashes:")
    for target_file in target_files:
        john_output = subprocess.run(["john", "--show", target_file], text=True, capture_output=True)
        print(john_output.stdout.strip())

if __name__ == "__main__":
    target_files, wordlist_target, fork = john_init()
    john_format(target_files, wordlist_target, fork)
    john_show(target_files)
