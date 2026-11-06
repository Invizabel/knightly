import argparse
import re
import json
import sys
import urllib.request

# C Source Code Scanner
def knightly(content):
    out = {}
    mal = {r"gets\s?\(": "fgets",
           r"sprintf\s?\(": "snprintf",
           r"strcpy\s?\(": "strlcpy"}

    for i, j in enumerate(content):
        for key, value in mal.items():
            if re.search(key, j):
                flaw = key.split("\\")[0]
                out.update({f"Line {i + 1}": {"Flaw": flaw, "Fix": value}})

    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type = str)
    parser.add_argument("--url", type = str)
    parser.add_argument("--out", type = str)
    args = parser.parse_args()

    if args.filename and args.url:
        print("Only one option allowed")
        sys.exit()

    elif not args.filename and not args.url:
        print("Please choose one option (--filename=example.c or --url=http://example.com/hello.c)")
        sys.exit()

    elif args.filename:
        content = []
        with open(args.filename, "r") as file:
            for line in file:
                new_line = line.strip("\n")
                content.append(new_line)

        out = knightly(content)
        if len(out) == 0:
            print("Looks good")
            if args.out:
                with open(args.out, "w") as file:
                    file.write(out)
        else:
            out = json.dumps(out, indent = 4)
            print(out)
            if args.out:
                with open(args.out, "w") as file:
                    file.write(out)

    elif args.url:
        request = urllib.request.Request(args.url)
        content = urllib.request.urlopen(request, timeout=10).read().decode().split("\n")
        
        out = knightly(content)
        if len(out) == 0:
            print("Looks good")
            if args.out:
                with open(args.out, "w") as file:
                    file.write(out)
        else:
            out = json.dumps(out, indent = 4)
            print(out)
            if args.out:
                with open(args.out, "w") as file:
                    file.write(out)