import sys
import os
import re

def has_abba(s):
    for i in range(len(s) - 3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
            return True
    return False

def parse_ip(line):
    # distinct parts
    parts = re.split(r'\[|\]', line)
    # parts[0], parts[2], ... are supernets
    # parts[1], parts[3], ... are hypernets
    supernets = parts[::2]
    hypernets = parts[1::2]
    return supernets, hypernets

def supports_tls(line):
    supernets, hypernets = parse_ip(line)
    
    # Check hypernets first - if ANY has ABBA, return False
    for h in hypernets:
        if has_abba(h):
            return False
            
    # Check supernets - if ANY has ABBA, return True
    for s in supernets:
        if has_abba(s):
            return True
            
    return False

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    count = 0
    for line in lines:
        if supports_tls(line):
            count += 1
    return count

def get_abas(s):
    abas = set()
    for i in range(len(s) - 2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            abas.add((s[i], s[i+1]))
    return abas

def supports_ssl(line):
    supernets, hypernets = parse_ip(line)
    
    found_abas = set()
    for s in supernets:
        found_abas.update(get_abas(s))
        
    for a, b in found_abas:
        bab = f"{b}{a}{b}"
        for h in hypernets:
            if bab in h:
                return True
    return False

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    count = 0
    for line in lines:
        if supports_ssl(line):
            count += 1
    return count

def run_example():
    print("Part 1 Examples:")
    examples = [
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True)
    ]
    for ip, expected in examples:
        result = supports_tls(ip)
        print(f"IP: {ip}, TLS: {result} (expected {expected})")
        
    print("\nPart 2 Examples:")
    examples_p2 = [
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True)
    ]
    for ip, expected in examples_p2:
        result = supports_ssl(ip)
        print(f"IP: {ip}, SSL: {result} (expected {expected})")

if __name__ == "__main__":
    print("Testing examples:")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())
