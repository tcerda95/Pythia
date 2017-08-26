# Pythia

Named after the Oracles of Delphi, Pythia is a testbed with the objetive of testing human recognition along with natural language processing. It detects someone's presence, intriguing about his/her troubles and providing an aphorism as a solution.

## Hardware

* [LilyPad MP3 Player](https://www.sparkfun.com/products/11013)
* [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

## Getting to know the LilyPad MP3 Player

We'll go through a number of sketches in order to familiarize ourselves with the concepts behind the LilyPad MP3 Player and the Arduino language, thinking through the most important parts and incrementally enhancing each sketch.

It is strongly recommended to go through the official [LilyPad MP3 Player Getting Started](https://learn.sparkfun.com/tutorials/getting-started-with-the-lilypad-mp3-player) first.

### Prerequisites

* [Arduino IDE installed](https://www.arduino.cc/en/Main/Software)
* [The provided libraries inside LilyPad/libraries directory installed](https://www.arduino.cc/en/Guide/Libraries)
* Understand C/C++/Arduino

### IDE Configuration

* **Board:** Arduino Pro or Pro Mini *(Tools > Board)*
* **Processor:** ATmega328 (3.3V, 8MHz) *(Tools > Processor)*
* **Port:** select the port that your FTDI board or cable is using. This is usually the highest number; you can be sure if you unplug the FTDI and the number disappears *(Tools > Port)*

### Basic Arduino Concepts

Let's review first some basic Arduino concepts which are recurrent to every sketch.

#### loop() and setup()

Every Arduino sketch is composed by the `setup()` and `loop()` functions. The `setup()` function is called only once when the sketch starts. As the name suggests, it is where the setup happens: initialization of variables, set pin modes, library classes, search and store files, etc.

On the other hand, the `loop()` function loops consecutively, allowing your program to read inputs, change it's state and respond. Here you can read pins (triggers in our case) status and respond accordingly, for instance, by playing or stopping a song.

#### Pins

The pins are the primary source of I/O communication for our board. In the case of the LilyPad MP3 Player we will be talking about **Triggers** which go from T1 to T5. Pins can have two possible values: `HIGH` and `LOW` and indicate the volts the pins are at. In the case of the LilyPad MP3 Player, `LOW` means 0V and `HIGH` means 3.3V.

These values may be read with `digitalRead()` function and set with the `digitalWrite()` function. We could, for example, set a trigger to an initial value of `HIGH` with `digitalWrite()` and check with `digitalRead()` if the value has changed to `LOW` and act accordingly.

### Trigger Sketch

This sketch comes preinstalled with the LilyPad MP3 Player. It will wait for one of the five trigger inputs to be grounded and will then play the corresponding audio file from the micro-SD card. The audio files should be placed under the root directory and renamed so the first character of each filename is the number "1" to "5", corresponding to the trigger that you want to play that file.
[Here](https://learn.sparkfun.com/tutorials/getting-started-with-the-lilypad-mp3-player/supported-audio-formats) are the supported audio formats.

The Sparkfun original source code is provided under the [TriggerDebug.ino](LilyPad/TriggerDebug/TriggerDebug.ino) file and a version without the debug directives, in order to improve code readability, is provided under the [Trigger.ino](LilyPad/Trigger/Trigger.ino) file. While the code is reasonably easy to understand on it's own, let's go through the essential parts which conform the basics of our LilyPad sketches. The [Trigger.ino](LilyPad/Trigger/Trigger.ino) sketch will be analyzed.

#### Code Explanation

#### setup()

Since we are planning to *receive* information from each of the triggers they are set to `INPUT` mode. Additionally, since the trigger inputs will be grounded, meaning they will enter a `LOW` mode, we manually set them to `HIGH` mode in order to be able to detect *when* they are grounded. In other words, we can detect a change from `HIGH` to `LOW` state.

```C++
for (x = 0; x <= 4; x++) {
    pinMode(trigger[x],INPUT);
    digitalWrite(trigger[x],HIGH);
}
```

Startup of the `SdFat` which allows us to traverse and read from the micro-SD. It's a utility class provided by the **SdFat** library. The `SD_CS` constant corresponds to the chip select for the SD card and `SPI_HALF_SPEED` to it's clock speed.

```C++
sd.begin(SD_CS, SPI_HALF_SPEED);
```

Startup of the `SFEMP3Shield` which allows us to play songs and any other kind of audio. It's a utility class provided by the `SFEMP3Shield` library.

```C++
MP3player.begin();
```

Change the micro-SD volume working directory to "/" as well as the current working directory. This is provided by the `true` value passed as parameter. This allows us to easily traverse the contents of any given directory.

```C++
sd.chdir("/",true);
```

Iterate through the files and subdirectories of the volume working directory, previously set to "/". Note `sd.vwd()` corresponds to a `SdFat` instance representing the directory contaning the file to be opened. `O_READ` corresponds to the usual flags associated with file operations. If the file name corresponds to the defined format it is saved in an array. The filename is read as a 13 length string. Note that if multiple filenames correspond to the same number, the last one read will be the one stored into the buffer. Finally, the file is closed. Attempting to open an already open file results in an error.

```C++
while (file.openNext(sd.vwd(),O_READ)) {
    file.getFilename(tempfilename);

    if (tempfilename[0] >= '1' && tempfilename[0] <= '5') {
        index = tempfilename[0] - '1';
        strcpy(filename[index],tempfilename);  
    }

    file.close();
}
```

#### loop()

Every trigger is read looking for a `LOW` status meaning it has been grounded (triggered). Here we can see why they were all set to `HIGH` in the first place.

A while loop representing a 50 msec delay to avoid a switch bounce. Note that it tics when the previously grounded trigger is in a `HIGH` state, therefore it will keep looping until we stop grounding the trigger.

Finally, if the interrupt or interrupt flags are set, the `MP3player` is stopped and played with the filename corresponding to the grounded trigger. We only need the name of the music file in order to play it.

```C++
for(t = 1; t <= 5; t++) {
    if (digitalRead(trigger[t-1]) == LOW) {
        x = 0;
        while(x < 50) {
            if (digitalRead(trigger[t-1]) == HIGH)
                x++;
            else
                x = 0;
            delay(1);
        } 

        if (filename[t-1][0] != 0) {
            if (interrupt && MP3player.isPlaying() && ((t != last_t) || interruptself)) {
                MP3player.stopTrack();
            }

            result = MP3player.playMP3(filename[t-1]);

            if (result == 0) 
                last_t = t;  // Save playing trigger
        }
    }
}
``` 

### Player Sketch

Let's build an MP3 player with the following features: PLAY, STOP, RESTART (restarts current song), NEXT and PREV. They will be assigned to the following triggers:

* T1: RESTART
* T2: NEXT
* T3: PLAY and STOP
* T4: PREV

We'll build simple versions, incrementally adding the necessary features until the final version.

### Version 1.0

Initially, let's play every audio file inside the root directory, one after the other and looping to the beginning once all audio files have been played. We'll have to:

* Determine when an audio file has finished playing
* Read the next audio file
* Loop all over again when all audio files in the directory have been read
* Validate that the file read is actually an audio file
* Play the audio file

The source code may be found under [Player1.0.ino](LilyPad/Player/Player1.0/Player1.0.ino). I encourage you to read it on your own before reading the explanation, it's very easy to follow.

#### Code Explanation

Since there should always be music playing, the simplest way to determine if an audio file has finished playing is merely checking if the `MP3Player` is playing. If it is not playing, we delay 50 msec and play the next track.

```C++
if (!MP3player.isPlaying()) {
    delay(50);
    playNextTrack();
}
```

In order to play the next track we first read the next filename in the root directory and store it into the `filename` `char` array. We must keep reading until we receive a valid audio file. Afterwards, we just play the file with the `MP3player.playMP3()` method.

```C++
void playNextTrack() {
  char filename[13];

  getNextFilename(filename);

  while (!isValidAudioFile(filename)) {
    getNextFilename(filename); 
  }

  MP3player.playMP3(filename);
}
```

Finally, in order to read the next filename, we make use of `file.openNext()`, which iterates over the files given by `sd.vwd()`. If no files are left to be read, `file.openNext()` returns 0, so we reset the file iterator by setting the SD VWD to root again .

```C++
void getNextFilename(char filename[]) {
  SdFile file;

  if (file.openNext(sd.vwd(), O_READ)) {
    file.getFilename(filename);
    file.close();
  }
  else {
    sd.chdir("/", true);  // Reset iterator
    getNextFilename(filename);
  }
}
```
### Version 2.0

Let's add now the PLAY and STOP funcitonality. Recall we will assign both to T3. We'll have to:

* Assign T3 as an `INPUT` pin (it will *receive* information) and set it to a `HIGH` state
* Determine when T3 enters a `LOW` state and take an action
* STOP the audio if it was *playing*; PLAY it otherwise

The source code may be found under [Player2.0.ino](LilyPad/Player/Player2.0/Player2.0.ino). As before, it is recommended to read it on your own before delving into the explanation.

#### Code Explanation

First, inside the `setup()` function, we prepare the T3 trigger. Since we will be *receiving* information from the pin it must be set to `INPUT`. Additionally, we set it to a `HIGH` state in order to check for a `LOW` state when it is grounded. Note that we previously defined `const int T3 = A5` as a global constant.

```C++
  pinMode(T3, INPUT);
  digitalWrite(T3, HIGH);
```

To be able to determine whether an audio file is playing or not, we make use of a `playing` flag. We cannot just check the value of `MP3player.isPlaying()` for this purpose because we are already relying on it for automatically playing the next song on the list. Therefore, we change the following line:

```C++
if (!MP3player.isPlaying()) {
    delay(50);
    playNextTrack();
}
```

to:

```C++
if (playing && !MP3player.isPlaying()) {
    delay(50);
    playNextTrack();
}
```

This way we prevent playing the next track if the player has been stopped, meaning `playing == false`.
Finally, we take an action if T3 is in a `LOW` state: STOP the track if it was `playing` or PLAY it otherwise.

```C++
if (digitalRead(T3) == LOW) {
  waitTriggerHigh(T3);
  
  if (playing)
    stopTrack();
  else
    resumeTrack();
}

void stopTrack() {
  playing = false;
  MP3player.pauseMusic();
}

void resumeTrack() {
  playing = true;
  MP3player.resumeMusic();
}
```

The last consideration is that the following line was added to `playNextTrack()`:

```C++
playing = true;
```

### Final Version

For the final version, we have to implement the RESTART, NEXT and PREV functionality. For this we will have to:

* Initialize the corresponding pins to `INPUT` and `HIGH` status
* Replay the current audio file when RESTART trigger is grounded
* Stop playing the current audio file when the PREV or NEXT trigger are grounded
* Determine the previous audio file played when PREV is grounded and play it
* Determine the next audio file when NEXT is grounded and play it

The source code may be found under [Player.ino](LilyPad/Player/Player/Player.ino). This code is a bit more complex than the others but still manageable.

#### Code Explanation

First of all, with the objective in mind of avoiding an `if` "trigger grounded then do this and that" chain for each trigger, we define a `Trigger` struct with the corresponding pin number and a function pointer to the action to be taken when such trigger is grounded. This allows us to define an array with each `Trigger` and simplify the `loop()` function by just iterating and checking if each pin has been grounded and execute an action if that's the case.

```C++
typedef struct {
    int trigger;
    void (*executor) (void);
} Trigger;

const Trigger triggers[] = {
                            {T1, &restartTrack}, 
                            {T2, &playNextTrack},
                            {T3, &toggleTrack}, 
                            {T4, &playPrevTrack}
                            };
```

and inside `loop()`:

```C++
int i;
for (i = 0; i < TRIGGERS_SIZE; i++) {
  if (digitalRead(triggers[i].trigger) == LOW) {
    waitTriggerHigh(triggers[i].trigger);
    triggers[i].executor();
  }
}  
```

The RESTART function makes use of `MP3player.skipTo()` which receives a msec skipping to that msec in the audio file. Beware that it automatically starts playing the audio file, so we check the value of the `playing` flag to determine if we should stop or not the music.

```C++
void restartTrack() {
  MP3player.skipTo(0);
  
  if (!playing)
    MP3player.pauseMusic();
}
```

The NEXT function makes use of `playNextTrack()` which is the as in version 1.0. The only precaution to be taken of is that the micro-SD files cannot be iterated while the MP3player is playing, so it is necessary to stop it before reading the next filename. Similarly, the MP3player must be stopped before playing a new audio file.

The PLAY and STOP functions were wrapped inside a `toggleTrack()` function which simply calls `stopTrack()` and `resumeTrack()` from version 2.0.

```C++
void toggleTrack() {
  if (playing)
    stopTrack();
  else
    resumeTrack();
}
```

Finally, the PREV function iterates the micro-SD backwards until a valid audio file is found. Iterating backwards it's not as simple as iterating forward. We must read files, storing the last one read until find the current file being played. This way, the stored filename represents the previous audio file to the current one. After that we iterate once more until the previous filename is read in order to reset the iterator: the next call to `getNextFilename()` should return the current track.

```C++
void playPrevTrack() {
  char prevFilename[MAX_FILENAME];
  
  getPrevFilename(prevFilename, currentTrack);
  strcpy(currentTrack, prevFilename);

  while (!isValidAudioFile(currentTrack)) {
    getPrevFilename(prevFilename, currentTrack);
    strcpy(currentTrack, prevFilename);
  }

  playTrack(currentTrack);
}

// Stores in prevFilename the previous file to currentFilename
void getPrevFilename(char prevFilename[], const char * currentFilename) {
  char loopFilename[MAX_FILENAME];

  strcpy(prevFilename, currentFilename);
  getNextFilename(loopFilename);

  while (strcasecmp(loopFilename, currentFilename) != 0) {
    strcpy(prevFilename, loopFilename);
    getNextFilename(loopFilename);
  }

  // Place iterator such that next call to getNextFilename returns currentFilename  
  while (strcasecmp(loopFilename, prevFilename) != 0)
    getNextFilename(loopFilename);
}
```

Notice that to be able to iterate backwards we need to know the name of the current track being played, so we define a `currentTrack` global and set it after every call to `playPrevTrack()` and `playNextTrack()`, as well as setting `playing = true`, stop the MP3player and wait until the MP3player is actually playing after a call to `MP3player.playMP3()`. To do this without repeating code between this two functions we define:

```C++
void playTrack(const char * trackName) {
  if (MP3player.isPlaying())
    MP3player.stopTrack();
  
  MP3player.playMP3(trackName);
  while (!MP3player.isPlaying()) // Wait until it starts playing
  ;
  playing = true;
  strcpy(currentTrack, trackName);
}
```

#### Final notes

* The filenames retrieved by the SD library are in the [8.3 format (short filename)](https://en.wikipedia.org/wiki/8.3_filename), which maximum length is of 12 plus the null character.
* Avoid using the T4 trigger when debugging. Since it is shared by the TX (transmitter) serial line, every write to the Serial will ground the T4 trigger. It is recommended to replace T4 for T5 in this case. While T5 is shared by the RX (receiver) serial line, information is never received from the Serial in this Sketch, so it shouldn't cause any trouble.

## Contact

Tomás Cerdá - <tcerda@itba.edu.ar>
