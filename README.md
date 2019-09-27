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
`brew install portaudio`

### 3. PyAudio
Remove pyaudio from `requirements.txt`, because it can't be installed with the default pip install command. Use instead the following:

`pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio`
Refer to https://gist.github.com/jiaaro/9767512210a1d80a8a0d#gistcomment-3023216 if this is not working

### 4. Install from requirements.txt

### 5. Start
While being in the venv
`python main.py`


### Naming
- **Intention** refers to intentions/functions within AgentSpeak(L)
- **Intent** refers to intents detected in user response returned by Wit.ai