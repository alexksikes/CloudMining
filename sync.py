import os

cmd = "rsync -Puzav --exclude='medline/data-full/' --exclude='sph-logs' /projects/scripts/cloudmining/ ale@greenland:/projects/scripts/cloudmining/"
os.system(cmd)
