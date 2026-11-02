import os
import sys
from hashlib import sha256

def compute(fname):
    with open(fname, 'rb') as fp:
        chksum = sha256(fp.read()).hexdigest()
    return chksum


def verify(fname, chksum):
    return chksum == compute(fname)

def main(rootdir):
    sumfile = f'{sha256(rootdir.encode()).hexdigest()}.sums'
    if os.path.isfile(sumfile):
        # Verification mode
        print("Sum File exists entering verification mode")
        integer = True
        checked = []
        with open(sumfile) as fp:
            sums = fp.read().splitlines()
        for line in sums:
            s = line.split(' ')[0]
            fpath = " ".join(line.split(' ')[1:])
            if not os.path.isfile(fpath):
                print(f'File "{fpath}" is missing')
                integer = False

            elif not verify(fpath, s):
                print(f'File "{fpath}" has changed')
                integer = False


            checked.append(fpath)

        for r, d, f in os.walk(rootdir):
            for file in f:
                fpath = f"{r}/{file}"
                if not os.path.isfile(fpath):
                    continue
                if fpath not in checked:
                    print(f'File "{fpath}" has been added')
                    integer = False

        if integer:
            print("All files have integrity")
        else:
            print("[!] Not all files have integrity")

    else:
        # Computing mode
        print("Sum File does not exists entering compute mode")
        for r, d, f in os.walk(rootdir):
            for file in f:
                fpath = f"{r}/{file}"
                if not os.path.isfile(fpath):
                    continue
                with open(sumfile, "a") as fp:
                    fp.write(f"{compute(fpath)} {fpath}\n")



if __name__ == "__main__":
    main(sys.argv[1])

# Model: chksum fpath