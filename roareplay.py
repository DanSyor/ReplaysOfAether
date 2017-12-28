# coding: utf-8
import sys
import struct
import os
import datetime
import argparse


log = print
# log = lambda x: None

def strnum0(i,l):
    iStr = i if isinstance(i,str) else str(i)
    return '0'*(l-len(iStr))+iStr

def frames2readableTime(f):
    sec = f // 60 + (1 if f%60 >= 30 else 0)
    min = sec // 60
    hou = min // 60
    sec = sec % 60
    min = min % 60
    return (str(hou)+":" if hou > 0 else "") + strnum0(min,2)+":"+strnum0(sec,2)

def removeExtraBlanks(s):
    x = len(s)-1
    while s[x] == " " and x >= 0:
        x -= 1
    return s[:x+1]

roaCharacter = {
   # 0 = "locked" (spin all characters)
   # 1 = sandbag? (random icon)
     2: {"name": "Zetterburn", "colorCodeLength": 8*4},
     3: {"name": "Orcane",     "colorCodeLength": 4*4},
     4: {"name": "Wrastor",    "colorCodeLength": 8*4},
     5: {"name": "Kragg",      "colorCodeLength": 7*4},
     6: {"name": "Forsburn",   "colorCodeLength": 11*4},
     7: {"name": "Maypul",     "colorCodeLength": 8*4},
     8: {"name": "Absa",       "colorCodeLength": 8*4},
     9: {"name": "Etalus",     "colorCodeLength": 5*4},
    10: {"name": "Ori",        "colorCodeLength": 8*4},
    11: {"name": "Ranno",      "colorCodeLength": 8*4},
    12: {"name": "Clairen",    "colorCodeLength": 11*4}
}


class RoAPlayer(object):
    def __init__(self, **kw):
        self.active = False
        self.type = 5
        self.setName("")
        self.setTag("")
        self.charID = 2
        
        if not "replaystream" in kw.keys():
            return self
        else:
            self.parseStream(**kw)
    
    def summary(self):
        if not self.active:
            return ""
        tag = removeExtraBlanks(self.tag)
        return removeExtraBlanks(self.name)+ ((" ("+tag+")") if tag else "")+" as "+roaCharacter[self.charID]["name"]
    
    def normName(self):
        self.name = self.name[0:32] + " "*(32-len(self.name))
    
    def setName(self, name):
        self.name = name
        self.normName()
    
    def normTag(self):
        self.tag = self.tag[0:6] + " "*(6-len(self.tag))
    
    def setTag(self, tag):
        self.tag = tag
        self.normTag()
    
    def parseStream(self, **kw):
        if "replaystream" in kw.keys():
            self.stream = kw["replaystream"]
        line = self.stream.readline()
        self.active = line[0] != "0"
        if self.active:
            self.type = line[0]
            self.name = line[1:33]
            self.tag = line[33:39]
            self.charID = int(line[39:41])
            k = roaCharacter[self.charID]["colorCodeLength"]
            self.skinInfo = line[41:50] # incorrect there's also team info and maybe other things but will keep as is until further investigation
            self.colorCode = line[50:50+k]
            
            '''k = 0
            l = len(line)-2
            while line[l-k] == " ":
                k +=1
            self.k = k
            self.unk = line[39:39+33-k]
            log(self.unk)
            self.colorCode = line[39+33-k:39+33-k+28]
            log(str(k)+'#'+str(39+33-k)+'#'+self.colorCode+'#')'''
            
            self.moves = self.stream.readline().split('\n')[0]
        else:
            self.type = "0"
        # line p: [H (if human player)/n (from 1 to 9, for CPU level)][Player's name (top) (32 chars, but currently limited to 19?)][Player's tag (6 chars)][char id (2 chars)][9 chars related to skin][k (depends on character) chars for skin color code][50-k spaces]/0 if not a player
        # line p+1: "instructions" if human, empty if CPU (inexistant if not a player)
    
    def writeStream(self, **kw):
        if "replaystream" in kw.keys():
            self.stream= kw["replaystream"]
        self.stream.write('\n')
        if self.active:
            self.stream.write(self.type)
            self.stream.write(self.name)
            self.stream.write(self.tag)
            #self.stream.write(self.unk)
            self.stream.write(strnum0(self.charID,2))
            self.stream.write(self.skinInfo)
            self.stream.write(self.colorCode)
            self.stream.write(' '*(50-len(self.colorCode)) +"\n")
            self.stream.write(self.moves)
        else:
            self.stream.write("0")
            
    def getCharacter(self):
        return roaCharacter[self.charID]["name"]

roaStage = {
     1: "Treetop Lodge"
,    2: "Fire Capital"
,    3: "Air Armada"
,    4: "The Rock Wall"
,    5: "Merchant Port"
,    7: "Blazing Hideout"
,    8: "Tower of Heaven"
,    9: "Tempest Peak"
,   10: "Frozen Fortress"
,   11: "Aetherial Gates"
,   12: "Endless Abyss"
,   14: "The CEO Ring"
,   15: "The Spirit Tree"
,   17: "Neo Fire Capital"
,   18: "The Swampy Estuary"
}

        
        # id stage
        # 00 Locked
        # 01 Treetop Lodge                   x
        # 02 Fire Capital                    x
        # 03 Air Armada                      x
        # 04 The Rock Wall                   x
        # 05 Merchant Port                   x
        # 06 Treetop Lodge (unused)          
        # 07 Blazing Hideout                 x
        # 08 Tower of Heaven                 x
        # 09 Tempest Peak                    x
        # 10 Frozen Fortress                 x
        # 11 Aetherial Gates                 x
        # 12 Endless Abyss                   x
        # 13 Unavailable (Air Armada alt?)   
        # 14 The CEO Ring                    x
        # 15 The Spirit Tree                 x
        # 16 Stage name (Air Armadashit)
        # 17 Unavailable (random)
        # 18 Unavailable (Fire Capital)
        # 19 Unavailable (Air Armada)
        # 20 Unavailable (Rock Wall)
        # 21 Unavailable (Merchant Port)
        # 22 Unavailable (Treetop)
        # 23 Unavailable (Hideout)
        # 24 Unavailable (Tower)
        # 25 Unavailable (Tempest)
        # 26 Unavailable (Fortress)
        # 27 Unavailable (Gates)
        # 28 Unavailable (Abyss)
        # 29 (no name: Scrap Armada)
        # 30 (no name: Ring)

        
class RoAReplay(object):
    def __init__(self, **kw):
        '''if not "path" in kw.keys():
            return self
        else:'''
        self.starred = False
        self.version = "1.2.2"
        self.date = datetime.datetime.now()
        self.setName("Forged replay")
        self.setDescription("")
        self.unk0_3 = "000"
        self.frames = 0
        self.mode = 0
        self.aether = False
        self.stageID = 1
        self.stocks = 3
        self.timer = 8
        self.kbScaling = 2
        self.teams = False
        self.teamAttack = False
        self.topVisible = False
        self.scoreLeft = 0
        self.scoreRight =0
        self.players = []
        if "path" in kw.keys():
            self.path = kw["path"]
            self.parsePath()
            
        if "star" in kw.keys():
            self.starred = kw["star"]
        if "date" in kw.keys():
            self.date = kw["date"]
        if "name" in kw.keys():
            self.setName(kw["name"])
        if "description" in kw.keys():
            self.name = kw["description"][0:140] + " "*(140-len(kw["name"]))
    
    def summary(self):
        playersDesc = ""
        for p in self.players:
            if p.active:
                playersDesc = playersDesc+"\n"+p.summary()
        desc = removeExtraBlanks(self.description)
        return removeExtraBlanks(self.name) +((" ["+desc+"]") if desc else "")+"\n"+roaStage[self.stageID]+"\t"+self.displayLength()+"\t"+str(self.scoreLeft)+"-"+str(self.scoreRight)+playersDesc
    
    def normName(self):
        self.name = self.name[0:32] + " "*(32-len(self.name))
    
    def setName(self, name):
        self.name = name
        self.normName()
        
    def normDescription(self):
        self.description = self.description[0:140] + " "*(140-len(self.description))
    
    def setDescription(self, description):
        self.description = description
        self.normDescription()
    
    def parsePath(self, **kw):
        if "path" in kw.keys():
            self.path = kw["path"]
        #log(os.path.basename(self.path))
        
        with open(self.path,"r") as replay:
            line = replay.readline()
            self.starred = line[0] == "1"
            self.version = str(int(line[1:3]))+"."+str(int(line[3:5]))+"."+str(int(line[5:7]))
            self.date = datetime.datetime(int(line[17:21]),int(line[15:17]),int(line[13:15]),int(line[7:9]),int(line[9:11]),int(line[11:13]))
            self.name = line[21:53]
            self.description = line[53:193]
            self.unk0_3 = line[193:196]
            self.frames = int(line[196:202])
            self.mode = int(line[202])
            # line 1: starred/unstarred (1/0), version (010201 = 1.2.1), date (hhmmssddMMYYYY), name (32 chars), description (140 chars), 000 (???), frames (6 chars), mode (0 = local, 1 = exhib, 2 = friendly, 3 = ranked)
            line = replay.readline()
            self.aether = line[0] == "1"
            self.stageID = int(line[1:3])
            self.stocks = int(line[3:5])
            self.timer = int(line[5:7])
            self.kbScaling = int(line[7])
            self.teams = line[8] == "1"
            self.teamAttack = line[9] == "1"
            #self.unk = line[8:10]
            self.topVisible = line[10] == "1"
            self.scoreLeft = int(line[11:14])
            self.scoreRight = int(line[14:17])
            # line 2: aether mode enabled (1) or disabled (0), stage id (2 chars), stock count (2 chars), timer (2 chars), kb scaling (1 char) (x(in/)) (2 = x1), teams [1=yes], teamattack (1=on), show/hide scores/names on top, score P1/team1 (3 chars), score P2 (3 chars)

            self.players = []
            self.players.append(RoAPlayer(replaystream=replay))
            self.players.append(RoAPlayer(replaystream=replay))
            self.players.append(RoAPlayer(replaystream=replay))
            self.players.append(RoAPlayer(replaystream=replay))
    
    def writePath(self, **kw):
        if "path" in kw.keys():
            self.path = kw["path"]
        with open(self.path,"w") as replay:
            replay.write('1' if self.starred else '0')
            version = self.version.split('.')
            for i in range(0,3):
                replay.write(strnum0(version[i],2))
            replay.write(strnum0(self.date.hour,2))
            replay.write(strnum0(self.date.minute,2))
            replay.write(strnum0(self.date.second,2))
            replay.write(strnum0(self.date.day,2))
            replay.write(strnum0(self.date.month,2))
            replay.write(strnum0(self.date.year,4))
            replay.write(self.name)
            replay.write(self.description)
            replay.write(self.unk0_3)
            replay.write(strnum0(self.frames,6))
            replay.write(str(self.mode))
            replay.write('\n')
            replay.write('1' if self.aether else '0')
            replay.write(strnum0(self.stageID,2))
            replay.write(strnum0(self.stocks,2))
            replay.write(strnum0(self.timer,2))
            replay.write(str(self.kbScaling))
            #replay.write(self.unk)
            replay.write('1' if self.teams else '0')
            replay.write('1' if self.teamAttack else '0')
            replay.write('1' if self.topVisible else '0')
            replay.write(strnum0(self.scoreLeft,3))
            replay.write(strnum0(self.scoreRight,3))
            for player in self.players:
                player.writeStream(replaystream=replay)
    
    def getStageName(self):
        return roaStage[self.stageID]
    
    def star(self):
        self.starred = True
    
    def unstar(self):
        self.starred = False
    
    def toggleStar(self):
        self.starred = not self.starred
    
    def hideTop(self):
        self.topVisible = False
    
    def showTop(self):
        self.topVisible = True
    
    def toggleTopVisibility(self):
        self.topVisible = not self.topVisible
    
    def switchPlayers(self, p1, p2):
        self.players[p1-1], self.players[p2-1] = self.players[p2-1], self.players[p1-1]
    
    def displayLength(self):
        return frames2readableTime(self.frames)

class RoASet(object):
    def __init__(self,**kw):
        self.games = []
        self.sortKey = -1
        self.name = ""
        self.trueSet = False
        self.finalScore=0,0
        if "path" in kw.keys():
            self.trueSet = True
            info = os.path.basename(kw["path"]).split(".")
            self.sortKey = int(info[0])
            self.name = info[1]
            fs = info[2].split("-")
            self.finalScore = (int(fs[0]),int(fs[1]))
            print("Processing set: "+self.name+" ("+info[2]+")")
            # yes: what's just above is hideous
            for (p,dir,files) in os.walk(kw["path"]):
                for file in files:
                    self.games.append(RoAReplay(path=os.path.join(p,file)))
        self.games.sort(key = lambda replay: replay.date)
        for game in self.games:
            game.unstar()
        self.player1 = ""
        self.player2 = ""
        if len(self.games)>0:
            self.games[0].star()
            self.player1 = self.games[0].players[0].name
            self.player2 = self.games[0].players[1].name
        for game in self.games:
            if self.player1 != game.players[0].name or self.player2 != game.players[1].name:
                print(removeExtraBlanks(self.player1) + " vs " + removeExtraBlanks(self.player2) + " expected")
                print("Got " + removeExtraBlanks(game.players[0].name) + " vs " + removeExtraBlanks(game.players[1].name))
                print("Stopping work with this set")
                self.trueSet = False
                #return
                break
        if not self.trueSet:
            print("Recap of matches in set")
            for game in self.games:
                print(game.summary())
                print()
            return
        else:
            print(removeExtraBlanks(self.player1) + " vs " + removeExtraBlanks(self.player2) + ", "+str(len(self.games))+ " games")
            print()
        # score = 0,0
        #for i in range(len(self.games)):
        i = 1
        for game in self.games:
            #desc = self.name+ " [Game "+ str(i+1) "]"
            desc = self.name+ " [Game "+ str(i) + "]"
            desc += " (score: "+str(game.scoreLeft)+"-"+str(game.scoreRight)+")"
            #self.games[i].setDescription(desc)
            game.setDescription(desc)
            i+=1
        
    
# '''  

ff = 0

def lengthSet(folder):
    global ff
    f = 0
    print(folder)
    for (p,dir, files) in os.walk(folder):
        for file in files:
            r = RoAReplay(path=os.path.join(p,file))
            print(r.summary())
            #print(r.displayLength())
            f += r.frames
        break
    print("Total (set): "+frames2readableTime(f))
    ff+=f
    print("Total (all): "+frames2readableTime(ff))
    print()

def tourneyResreamReplays(in_folder, out_folder):
    sets = []
    log = ""
    for (p, dirs, files) in os.walk(in_folder):
        for dir in dirs:
            sets.append(RoASet(path=os.path.join(p,dir)))
        break
    sets.sort(key = lambda set: set.sortKey)
    streamFolder = os.path.join(out_folder,"streamer")
    castFolder = os.path.join(out_folder,"caster")
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    if not os.path.exists(streamFolder):
        os.mkdir(streamFolder)
    if not os.path.exists(castFolder):
        os.mkdir(castFolder)
    framesT = 0
    for set in sets:
        framesS = 0
        log += set.name + "\n"
        log += removeExtraBlanks(set.player1) + " vs " + removeExtraBlanks(set.player2) + "\n"
        i = 1
        for game in set.games:
            framesS += game.frames
            log += "Game "+str(i)+": "+str(game.scoreLeft)+"-"+str(game.scoreRight)+"\t"+game.displayLength()+"\t"+roaStage[game.stageID]+"\t"+roaCharacter[game.players[0].charID]["name"]+" vs "+roaCharacter[game.players[1].charID]["name"]+"\n"
            game.date = game.date.replace(year = 1000 + set.sortKey)
            game.writePath(path=os.path.join(castFolder, set.name+"-"+str(i)+".roa"))
            game.hideTop()
            game.writePath(path=os.path.join(streamFolder, set.name+"-"+str(i)+".roa"))
            i+=1
        log += "Final score should be "+str(set.finalScore[0])+"-"+str(set.finalScore[1])+"\n"
        log += "Set duration: "+frames2readableTime(framesS)+"\n"
        framesT += framesS
        log += "Total duration after this set: "+frames2readableTime(framesT) + "\n\n"
    with open(os.path.join(out_folder,"log.txt"), "w") as logFile:
        logFile.write(log)

tourneyResreamReplays("SuperNova 10","replays_sn10")
