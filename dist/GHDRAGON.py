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
# a run that stopped with an error can leave the game's files in memory
# (and stale, even after new ones are sent): clear every GH file first
drop([k for k in sys.modules if k[:2]=="GH" and k!=__name__])
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
 try:
  import GHDRAGOP
  free("game loaded")
  GHDRAGOP.G_back()
 finally:
  GHDRAGOP=None
  drop([k for k in sys.modules if k[:2]=="GH" and k!=__name__])
RAN=True
