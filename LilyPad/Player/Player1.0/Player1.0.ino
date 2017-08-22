
#include <SPI.h>            // To talk to the SD card and MP3 chip
#include <SdFat.h>          // SD card file system
#include <SFEMP3Shield.h>   // MP3 decoder chip

const int EN_GPIO1 = A2; // Amp enable + MIDI/MP3 mode select
const int SD_CS = 9;     // Chip Select for SD card

char * validExtensions[] = {"MP3", "WAV", "MID", "MP4", "WMA", "FLA", "OGG", "AAC"};

SFEMP3Shield MP3player;
SdFile file;
SdFat sd;

void setup()
{
  int index;
  byte result;

  // The board uses a single I/O pin to select the
  // mode the MP3 chip will start up in (MP3 or MIDI),
  // and to enable/disable the amplifier chip:
  
  pinMode(EN_GPIO1,OUTPUT);
  digitalWrite(EN_GPIO1,LOW);  // MP3 mode / amp off

  // Initialize the SD card; SS = pin 9, half speed at first

  result = sd.begin(SD_CS, SPI_HALF_SPEED); // 1 for success
  
  if (result != 1) // Problem initializing the SD card
  {
    error(); // Halt forever
  }
  
  // Start up the MP3 library

  result = MP3player.begin(); // 0 or 6 for success

  // Check the result, see the library readme for error codes.

  if ((result != 0) && (result != 6)) // Problem starting up
  {
    error(); // Halt forever
  }

  sd.chdir("/",true);

  // Set the VS1053 volume corresponding to left and right speaker. 
  // 0 is loudest, 255 is lowest (off):

  MP3player.setVolume(10,10);
    
  digitalWrite(EN_GPIO1,HIGH);
  delay(2);

  playNextTrack();
}


void loop()
{
  if (!MP3player.isPlaying()) {
    playNextTrack();
  }
}

void playNextTrack() {
  char fileName[13];
  
  if (file.openNext(sd.vwd(), O_READ)) {
    file.getFilename(fileName);
    file.close();
    
    if (isValidAudioFile(fileName))
      MP3player.playMP3(fileName);
    else
      playNextTrack();
  }
  else {
    sd.chdir("/",true);
    playNextTrack();
  }  
}

boolean isValidAudioFile(const char * fileName) {
  int i;
  char *extension;
  
  extension = strrchr(fileName, '.');
  extension++;

  for (i = 0; i < (sizeof(validExtensions) / sizeof(validExtensions[0])); i++) {
    if (strcasecmp(extension, validExtensions[i]) == 0) {
      return true;
    }
  }
  
  return false;
}

void error()
{
  while(true) // Loop forever
  ;
}
