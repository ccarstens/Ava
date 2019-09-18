# Ava
Ava is an autonomous virtual assistant

## Installation
### 1. Prosody
**Install Prosody via homebrew**
```
brew tap prosody/prosody 
brew install prosody
```
Refer to https://prosody.im/download/start for details

**If needed edit the config file for SSL or domain settings**
`/usr/local/etc/prosody/prosody.cfg.lua`

**Add a user for each agent** 
`prosodyctl adduser`

**Start prosody**
`prosodyctl start`

### 2. Portaudio
**`brew install portaudio`**

