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

This sketch comes preinstalled with the LilyPad MP3 Player. This sketch will wait for one of the five trigger inputs to be grounded and will then play the corresponding audio file from the micro-SD card. The audio files should be placed under the root directory and renamed so the first character of each filename is the number "1" to "5", corresponding to the trigger that you want to play that file.
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

#### Coming Soon!

## Contact

Tomás Cerdá - <tcerda@itba.edu.ar>
