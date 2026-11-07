# GHCRYPT from GAMEHUB, on its own. Run it.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
# memory meter: prints how much memory is free at each step, so if this
# stops with a memory error the last lines say where
def free(step):
 gc.collect()
 try:
  print(step,gc.mem_free())
 except Exception:
  print(step)
while True:
 free("start")
 import GHCRYPTH
 free("home loaded")
 c=GHCRYPTH.G_front()
 GHCRYPTH=None
 drop(["GHCRYPTH"])
 free("home dropped")
 if c<0:
  break
 import GHCRYPTP
 free("game loaded")
 GHCRYPTP.G_back()
 GHCRYPTP=None
 drop(["GHCRYPTP"]+["GHCRYPT"+c for c in "BCDEF"])
RAN=True
