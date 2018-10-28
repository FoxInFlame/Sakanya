# Changelog:
1.6.0
- Commands removed: >timeout
- Commands added: >timeout, >bots

1.5.0
- Moved to Heroku using Free Dynos (1000 hours/month) because IATGOF's server lost its DB.
- Commands added: >override_messagecount, >override_reactioncount

1.4.0
- Added April Fools channel shuffling

1.3.0
- 1.3.4
- - Fix half broken logic regarding suggestion control. One message could have 10 upvotes and 5 downvotes.

- 1.3.3
- - Quote function requires 3 characters prefix
- - Now counts reaction add/remove for emoji counter
- - Suggestioncontrol works with Force Completion by FoxInFlame

- 1.3.2
- - Return of the graph statistics
- - While also maintaining the text based statistics
- - New emoji statistics

- 1.3.1
- - Fixed stats problems Drutol and IATGOF kept negging about
- - Removed unused definitions in stats.py
  
- Reformatted >stats for simpler, more quicker layout that matches Andre's
  
1.2.0
- Commands added: >addreaction
- Added Admin help inside >help that only shows when Fox sends the message

1.1.2
- Add support for !manga url detection.
- Fix KeyError: 'emoji' in case Emoji didn't exist for some unknown Discord bug
- Now watches random YT videos as well.
  
1.1.1
- Disable Automatic Kicking System
- Commands added: >modules, >reset_messagecount
- Now changes presence to "Listening to" and "Watching" as well
- Change font for matplotlib to Osaka (installed by IATGOF)
- >readfile sends to Gist now
- Fix restart now working
- Rewrote logic for presence update randomness
  
1.1.0
- Now automatically kicks users if they're inactive!
  
1.0.19
- Add "hungry for new waifu" as the role to get notified by BobDono.
- Reset messagecounter and change JSON format.
  
1.0.18
- Automatically add roles to new users
- Now counts messages sent by authors.
- Commands added: >stats
- Now supports quoting using >
  
1.0.17
- Add botchain >hello
  
1.0.16
- Rewrote >saka using aiohttp instead of urllib so that it no longer crashes
  
1.0.15
- Added SakanyaCore boolean to disable colour restrictions
  
1.0.14
- Added >colour random, and >colour remove
- Update help message for >colour
- Added contrast checker for >colour
  
1.0.13
- Moved debug setting to Core.
- Removed all of Saka's useless Xaetral emote interactions
- Removed Saka's useless no-motsy interaction
- Commands added: >colour
  
1.0.12
- Comamnds added: ping
- Animation + average for ping
  
1.0.11
- - fix
  - Fixed mistyping of SakanyCore to SakanyaCore
  
- Fixed typing bug in mention.
- Fixed user selection when mentioning with question mark.
- Moved core code to SakanyaCore() class in __main__
- Use SakanyaCore() class in other files instead of hardcoded values.
- Moved PresenceUpdate function to individual file.
- Output startup errors for modules if there were any to Discord.
  
1.0.10
- Add 'n:cry' and 'n:motherofgod' to further mock Xae.
- Confirmed that mentions in embeds don't notify mentioned users.
- Changed response to mentioning André.
- Add 3 more love messages.
  
1.0.9
- Rename mockxaetral to uselessinteractions
- Added response to Andy's 'No Motsy' message
  
1.0.8
- Removed unnecessary new line in >update response
- Fixed status message after update was aborted
- Added a small command that you wouldn't notice :)
  
1.0.7
- Update command now aborts restart if it's already up-to-date.
  
1.0.6
- Properly handle help messages with nonexistent subcommands
- New turquoise background in profile picture
  
1.0.5
- Renamed suggestionremoval file and class to suggestioncontrol
- Added auto-reacting to suggestions
- Increased required x count to 5
- Rename ReadFile class to FileManagement
  
1.0.4
- Commands added: readfile, emptyfile
  
1.0.3
- Output git pull response to chat
- Commands added: iam, iamnot
  
1.0.2
- -fix2
  - Change switchversion to update
  
- -fix
  - Fix bugs in switchversion
  - Print debug statuses
  
- Added support for updating via Discord using the switchversion command
  
1.0.1
- Now on a stable server
- Commands added: robot
- Moved commands to individual files and used cogs (advise from IATGOF)
  
1.0.0
- Commands added: saka, restart, help, about, love, waifu
- Emoji Suggestion
- Suggestion Removal
- Interaction with mentions