import tarfile
import os
import hashlib
import mmap
import argparse

parser = argparse.ArgumentParser("SparkEVO Arduino Package generator")
parser.add_argument("version", help="Package version")
args = parser.parse_args()

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


version = args.version
tarname = "SparkEVO-ArduinoCore-tinyAVR-" + version + ".tar.gz"
if os.path.exists(tarname):
    os.remove(tarname)

with tarfile.open(tarname,"w:gz", dereference=True, format=tarfile.GNU_FORMAT) as tar:
    files = os.listdir("./megaavr")
    for file in files:
        print(os.path.basename(file))
        if file == "extras" or file == ".":
            continue
        tar.add("./megaavr/" + file, arcname="SparkEVO-ArduinoCore-tinyAVR/" + os.path.basename(file), recursive=True)

print()
print("\"name\": \"SparkEVO tinyAVR Boards (32-bits ARM Cortex-M0+)\",")
print("\"architecture\": \"megaavr\",")
print("\"version\": \"" + version + "\",")
print("\"category\": \"SparkEVO\",")
print("\"help\": {\"online\": \"https://sparkevo.racing/\"},")
print("\"url\": \"https://sparkevo.racing/resources/internal/arduino-board-index/boards/" + tarname + "\",")
print("\"archiveFileName\": \"" + tarname + "\",")
print("\"checksum\": \"SHA-256:" + sha256sum(tarname) + "\",")
print("\"size\": \"" + str(os.path.getsize(tarname)) + "\",")
print()