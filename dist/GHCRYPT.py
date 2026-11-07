# GHCRYPT from GAMEHUB, on its own. Run it.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
while True:
 gc.collect()
 import GHCRYPTH
 c=GHCRYPTH.G_front()
 GHCRYPTH=None
 drop(["GHCRYPTH"])
 gc.collect()
 if c<0:
  break
 import GHCRYPTP
 GHCRYPTP.G_back()
 GHCRYPTP=None
 drop(["GHCRYPTP"]+["GHCRYPT"+c for c in "BCDEF"])
RAN=True
