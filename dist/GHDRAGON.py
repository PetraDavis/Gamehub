# GHDRAGON from GAMEHUB, on its own. Run it.
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
 import GHDRAGOH
 free("home loaded")
 c=GHDRAGOH.G_front()
 GHDRAGOH=None
 drop(["GHDRAGOH"])
 free("home dropped")
 if c<0:
  break
 import GHDRAGOP
 free("game loaded")
 GHDRAGOP.G_back()
 GHDRAGOP=None
 drop(["GHDRAGOP"]+["GHDRAGO"+c for c in "BCDEFVWXYZ"])
RAN=True
