# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:48:50 2022
@author: Mercteria

Usage:
Place the script under the path along with your NFT part folders.

Example:
basp
|- NFTCreating.py
|- Base
|  |- Base.png
|
|- Part1
|  |- P1_T1.png
|  |- P1_T2.png
|  |- ...
|
|- Part2
|  |- P2_T1.png
|  |- ...

If your layer order is like this:
Layer3 -> Part2
Layer2 -> part1
Layer1 -> Base
Than the order in your cond["part"] should be like:
["Layer1","Layer2","Layer3"]

Output:
1. Created NFTs saved in folder named CREATED under your base path.
2. Create history file will be saved under CREATED folder (same as yout result.)
3. If the created number reaches the maximum number of the combination, the script will stop.

"""

from PIL import Image
import random
import json
import sys
import os

### Condition
cond = {
    'basp' : os.path.abspath(os.path.dirname(sys.argv[0])), # Directory which contains part folders of your NFT.
    'history' : "Created.json", # File name of created history in json format, default : "Created.json".
    'part' : [], # Layer order of your NFT parts.
    'limit' : 100 # Limit number to be created.
}

### Combination to be excluded
# Structure : [{"Part1":"P1_typ","Part2":"P2_typ",...},{...}]
excluded = []

### Naming function
def crtnm(tot,cur):
    zlen = len(str(tot))-len(str(cur))
    nm = ("0"*zlen)+str(cur)
    return nm

### Create Result Folder
svpt = os.path.join(cond["basp"],"CREATED")
if not os.path.exists(svpt):
    os.makedirs(svpt)

### Count Control
totmax = 1
for p in cond["part"]:
    ptcnt = len([f for f in os.listdir(os.path.join(cond["basp"],p)) if f.endswith(".png")])
    totmax*=ptcnt
histp = os.path.join(svpt,cond['history'])
try:
    if os.path.exists(histp):
        f = open(histp)
        created = json.load(f)
        cnt = len(created)-1
        cond["limit"]+=cnt
        f.close()
except:
    cnt = 0
    created = []
else:
    cnt = 0
    created = []

### Prevent program from creating sample type
for exc in excluded:
    if exc not in created:
        created.append(exc)
    
### Create Image
while cnt < cond["limit"] and cnt < totmax:
    meta = {}
    basp = None
    # Parts
    for prt in cond["part"]:
        plst = [p for p in os.listdir(os.path.join(cond["basp"],prt)) if p.endswith(".png")]
        opnf = random.choice(plst)
        meta[prt] = opnf.split(".")[0]
        if not basp:
            basp = Image.open(os.path.join(cond["basp"],prt,opnf))
        else:
            apnd = Image.open(os.path.join(cond["basp"],prt,opnf))
            basp.paste(apnd, (0, 0), apnd)
    # Check existed
    if meta not in created:
        created.append(meta)
        toknid = crtnm(cond["limit"],cnt)
        basp.save(os.path.join(svpt,toknid+".png"))
        meta["id"] = toknid
        with open(os.path.join(svpt,toknid+'.json'), 'w') as fp:
            json.dump(meta, fp)
        cnt+=1

### Save created list
with open(histp, 'w') as fp:
    json.dump(created, fp)