from firestore import delete_full_collection
import subprocess

out = subprocess.run('rm -rf __pycache__/', shell=True)
print(out)

out = subprocess.run('ls', shell=True)
print(out)

delete_full_collection() # This fucntion delete the entire collection
