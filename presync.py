# Python 3.3.5 (v3.3.5:62cf4e77f785)
import os, stat, sys, P4 # P4PYTHON/NTX64/2015.1/1062785
p4 = P4.P4().connect()
p4.exception_level = 1
root = [ 'd:', 'prefetch', 'tc-p4' ]
prefetched = [] # matches
synczeroes = [] # one call
for preview in p4.run_sync("-n",sys.argv[1:]): # p4 call 1
  if 'action' in preview and 'clientFile' in preview:
    if preview['action'] in [ 'added', 'updated', 'refreshed']:
      if int(preview['fileSize']) >= 1000000:
        depotrev = preview['depotFile']+"#"+preview['rev']
        prefetch = os.sep.join(root + depotrev[2:].split('/'))
        if os.path.isfile(prefetch):
          if os.stat(prefetch).st_size == int(preview['fileSize']):
            prefetched.append((prefetch,preview['clientFile'],depotrev))
            if preview['action'] != 'added':
              synczeroes.append(preview['depotFile']+"#0")
            print(preview['action'],prefetch)
try:
  p4.run_sync(*synczeroes) # p4 call 2
except Exception:
  pass # ignore unlink / clobber (but, check the files have gone)
syncflushes = [ ] # one call
for prefetch,clientfile,depotrev in prefetched:
  if not os.path.exists(clientfile):
    client_dir = os.path.dirname(clientfile)
    if not os.path.exists(client_dir):
      try:
        os.makedirs(client_dir)
      except Exception:
        pass
    os.chmod(prefetch, stat.S_IWRITE)
    os.rename(prefetch, clientfile)
    syncflushes.append(depotrev)
p4.run_sync("-k", syncflushes) # p4 call 3
for fstat in p4.run_fstat(*syncflushes): # p4 call 4 - consider -Ol and md5 verify of 'digest', at least to begin with
  ftype = fstat['headType']
  if '+' not in ftype or 'w' not in ftype.split('+')[1]:
    os.chmod(fstat['clientFile'], stat.S_IREAD)
