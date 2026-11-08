# GAMEHUB - game center for the TI-84 Evo. Run this file.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
st=[0,0,0,"",""]
while True:
 gc.collect()
 import GHMENU
 mod=GHMENU.H_pick(st)
 GHMENU=None
 drop(["GHMENU"]+["GHMENU"+c for c in "BCDEF"])
 gc.collect()
 if not mod:
  break
 try:
  m=__import__(mod)
  if not getattr(m,"RAN",False):
   m.main()
 except Exception as e:
  st[3]=str(e)[:26]
  st[4]=mod
 m=None
 drop([mod]+[mod[:7]+c for c in "BCDEFHPVWXYZ"])
