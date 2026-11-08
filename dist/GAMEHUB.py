# GAMEHUB - game center for the TI-84 Evo. Run this file.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
# a game that stopped with an error last time can leave its files in memory
# (and stale, even after new ones are sent): clear every GH file first
drop([k for k in sys.modules if k[:2]=="GH"])
st=[0,0,0,"",""]
# the menu and the game are only touched inside these small functions:
# when a function returns, nothing is left pointing at the menu or the game,
# so dropping them really frees their memory (at the top level a leftover
# reference could keep the whole menu in memory under the game)
def pick():
 import GHMENU
 return GHMENU.H_pick(st)
def play(mod):
 m=__import__(mod)
 if not getattr(m,"RAN",False):
  m.main()
while True:
 gc.collect()
 mod=pick()
 drop(["GHMENU"]+["GHMENU"+c for c in "BCDEF"])
 gc.collect()
 if not mod:
  break
 try:
  play(mod)
 except Exception as e:
  st[3]=str(e)[:26]
  st[4]=mod
 drop([mod]+[mod[:7]+c for c in "ABCDEFHPQSTVWXYZ"])
