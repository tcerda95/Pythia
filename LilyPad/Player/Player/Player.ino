
#include <SPI.h>            // To talk to the SD card and MP3 chip
#include <SdFat.h>          // SD card file system
#include <SFEMP3Shield.h>   // MP3 decoder chip

typedef struct {
    int trigger;
    void (*executor) (void);
} Trigger;

const int T1 = A0;  // RESTART
const int T2 = A4;  // NEXT
const int T3 = A5;  // PLAY AND STOP
const int T4 = 1;   // PREV
const int T5 = 0;

const boolean debugging = false;

void restartTrack(void);
void playNextTrack(void);
void toggleTrack(void);
void playPrevTrack(void);

const Trigger triggers[] = {
                            {T1, &restartTrack}, 
                            {T2, &playNextTrack},
                            {T3, &toggleTrack}, 
                            {debugging ? T5 : T4, &playPrevTrack}
                            };

const int TRIGGERS_SIZE = sizeof(triggers)/sizeof(triggers[0]);

const int EN_GPIO1 = A2; // Amp enable + MIDI/MP3 mode select
const int SD_CS = 9;     // Chip Select for SD card

const int WAIT_HIGH_MSECS = 50;
const int MAX_FILENAME = 13;

const char * validExtensions[] = {"MP3", "WAV", "MID", "MP4", "WMA", "FLA", "OGG", "AAC", "M4A"};

SFEMP3Shield MP3player;
SdFat sd;
SdFile file;
char currentTrack[MAX_FILENAME]; // Short file name format (8.3) Max length 13
boolean playing;

void setup() {
  byte result;
  int i;

  if (debugging)
    Serial.begin(9600);

  for (i = 0; i < TRIGGERS_SIZE; i++) {
    pinMode(triggers[i].trigger, INPUT);
    digitalWrite(triggers[i].trigger, HIGH);    
  }

  // The board uses a single I/O pin to select the
  // mode the MP3 chip will start up in (MP3 or MIDI),
  // and to enable/disable the amplifier chip:
  
  pinMode(EN_GPIO1,OUTPUT);
  digitalWrite(EN_GPIO1,LOW);  // MP3 mode / amp off

  // Initialize the SD card; SS = pin 9, half speed at first

  result = sd.begin(SD_CS, SPI_HALF_SPEED);

  if (result != 1)
    error(F("Failed to initialize SD card"));
  
  result = MP3player.begin();

  if ((result != 0) && (result != 6))
    error(F("Failed to initialize MP3 PLayer"));

  sd.chdir("/",true);

  // Set the VS1053 volume corresponding to left and right speaker. 
  // 0 is loudest, 255 is lowest (off):

  MP3player.setVolume(10,10);
    
  digitalWrite(EN_GPIO1,HIGH);
  delay(2);

  playNextTrack();  // Play first track
  delay(50);  // Wait a bit for track to start
  Serial.println(F("Setup done!"));
}


void loop() {
  int i;
  
  if (playing && !MP3player.isPlaying())
    playNextTrack();

  for (i = 0; i < TRIGGERS_SIZE; i++) {
    if (digitalRead(triggers[i].trigger) == LOW) {
      waitTriggerHigh(triggers[i].trigger);
      triggers[i].executor();
    }
  }  
}

void waitTriggerHigh(int trigger) {
  int elapsedMsecs = 0;

  for (elapsedMsecs = 0; elapsedMsecs < WAIT_HIGH_MSECS; elapsedMsecs++) {
    if (digitalRead(trigger) != HIGH)
      elapsedMsecs = 0;
    delay(1);
  }
}

void toggleTrack() {
  if (playing)
    stopTrack();
  else
    resumeTrack();
}

void stopTrack() {
  playing = false;
  MP3player.pauseMusic();
  Serial.print(F("Stopping track: "));
  Serial.println(currentTrack);
}

void resumeTrack() {
  playing = true;
  MP3player.resumeMusic();
  Serial.print(F("Resuming track: "));
  Serial.println(currentTrack);
}

void restartTrack() {
  MP3player.skipTo(0);  // Restarts AND plays track
  
  if (!playing)
    MP3player.pauseMusic();
    
  Serial.print(F("Restarting track: "));
  Serial.println(currentTrack);
}

void playNextTrack() {
  char filename[13];

  getNextFilename(filename);

  while (!isValidAudioFile(filename)) {
    Serial.println(F("Invalid audio file"));
    getNextFilename(filename); 
  }

  playTrack(filename);
}

void getNextFilename(char filename[]) {  
  if (MP3player.isPlaying()) // Cannot read SD while music is playing
    MP3player.stopTrack();

  if (file.openNext(sd.vwd(), O_READ)) {
    file.getFilename(filename);
    file.close();

    Serial.print(F("Read filename: "));
    Serial.println(filename);
  }
  else {
    Serial.println(F("Looping through all files again"));
    sd.chdir("/", true);  // Reset iterator
    getNextFilename(filename);
  }
}

void playTrack(const char * trackName) {
  if (MP3player.isPlaying())
    MP3player.stopTrack();
  
  MP3player.playMP3(trackName);
  while (!MP3player.isPlaying()) // Wait until it starts playing
  ;
  playing = true;
  strcpy(currentTrack, trackName);

  Serial.print(F("Playing: "));
  Serial.println(currentTrack);
}

void playPrevTrack() {
  char prevFilename[MAX_FILENAME];
  
  getPrevFilename(prevFilename, currentTrack);
  strcpy(currentTrack, prevFilename);
  Serial.print(F("Prev audio file: "));
  Serial.println(prevFilename);

  while (!isValidAudioFile(currentTrack)) {
    Serial.println(F("Invalid prev audio file"));
    getPrevFilename(prevFilename, currentTrack);
    strcpy(currentTrack, prevFilename);
    Serial.print(F("Prev audio file: "));
    Serial.println(prevFilename);
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

boolean isValidAudioFile(const char * filename) {
  int i;
  int extensionsLength = (sizeof(validExtensions) / sizeof(validExtensions[0]));
  char *extension;
  
  extension = strrchr(filename, '.');
  extension++;

  for (i = 0; i < extensionsLength; i++) {
    if (strcasecmp(extension, validExtensions[i]) == 0) {
      return filename[0] != '_';
    }
  }
  
  return false;
}

void error(const __FlashStringHelper * cause) {
  while(true) {
    Serial.println(cause);
    delay(2000);
  }
}

