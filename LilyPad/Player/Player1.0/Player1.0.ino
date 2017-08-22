
#include <SPI.h>            // To talk to the SD card and MP3 chip
#include <SdFat.h>          // SD card file system
#include <SFEMP3Shield.h>   // MP3 decoder chip

const int EN_GPIO1 = A2; // Amp enable + MIDI/MP3 mode select
const int SD_CS = 9;     // Chip Select for SD card

char * validExtensions[] = {"MP3", "WAV", "MID", "MP4", "WMA", "FLA", "OGG", "AAC"};

SFEMP3Shield MP3player;
SdFat sd;

void setup() {
  Serial.begin(9600);
  byte result;

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

  Serial.println(F("Setup done!"));
}


void loop() {
  if (!MP3player.isPlaying()) {
    delay(50);
    playNextTrack();
  }
}

void playNextTrack() {
  char filename[13];

  getNextFilename(filename);

  while (!isValidAudioFile(filename)) {
    Serial.println(F("Invalid audio file"));
    getNextFilename(filename); 
  }

  MP3player.playMP3(filename);
  Serial.print(F("Playing: "));
  Serial.println(filename);
}

void getNextFilename(char filename[]) {
  SdFile file;

  if (file.openNext(sd.vwd(), O_READ)) {
    file.getFilename(filename);
    file.close();

    Serial.print(F("Read filename: %s\n"));
    Serial.println(filename);
  }
  else {
    Serial.println(F("Looping through all files again"));
    sd.chdir("/", true);  // Reset iterator
    getNextFilename(filename);
  }
}

boolean isValidAudioFile(const char * filename) {
  int i;
  int extensionsLength = (sizeof(validExtensions) / sizeof(validExtensions[0]));
  char *extension;
  
  extension = strrchr(filename, '.');
  extension++;

  for (i = 0; i < extensionsLength; i++) {
    if (strcasecmp(extension, validExtensions[i]) == 0) {
      return true;
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


