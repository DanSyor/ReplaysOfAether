# ReplaysOfAether
Manager for replays from Rivals of Aether

You need Python 3 to run this.


# Usage
roareplay.py contains basic classes for replays, players within replays and "sets".  
A set is a folder containing replays of the same two players. For now, the folder must be named something like `x.SetName.EndScore`  where `x` is an integer, `SetName` is the name you want your set to have (just avoid the '.' character within it) and `EndScore` is the score at the end of the set. (ex: "42.Grand Finals - D4n vs George.3-2")  
The "set" class is currently kind of a mess, but you can use the `RoAReplay` and `RoAPlayer` classes to alter replays however you want.

# Restreams
The primary use of this script as is is for restreams of Rivals Of Aether tournaments where TOs gathered replays from players. 
* Get replays from players. Have each set in its own folder. Place all these folders inside one main directory.
* Rename each set-folder the way described in the previous paragraph (`x.SetName.EndScore`) where `x` is the order of your set for your restream (if `x` is smaller then it will be cast sooner)
* Run the script in Windows Command Line or Power Shell or anything else you installed with command lines, specifying the directory where your sets are and an output directory: `roareplay.py replays_in replays_out` or `python roareplay.py replays_in replays_out` or `py -3 roareplay.py replays_in replays_out` (note: you can drag and drop folders in the command line thing if the script and your replays are located far apart)
* It should mention if there's anything weird in those replays (like players changing) and output Steam name of players (as available from replays, so can be cut short) and the number of games (note: sets may be processed in a different order than they will be cast, it doesn't matter).
* If all went well, inside the `replays_out` folder, you will find two folders, `caster` and `streamer`, along with `log.txt`, in which you have information on all games of sets in the order you want them to be cast (scores at the beginning of a game, stage, characters). Files inside `caster` and `streamer` are the replays from the `replays_in` folder with their filenames changed to `SetName-y.roa`, meaning it's game `y` of the set, and the year in their date changed to `1000+x` (as seen from the game, not your OS). The difference between `caster` and `streamer` is that replays inside `streamer` have the top part of HUD (with Steam names and scores) turned off so that the streamer can display information on players however they want in their own overlay.
