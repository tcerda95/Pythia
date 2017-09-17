/* 
 * TalkingSensor.h - Library for checking is someone is talking.
 * Created by Tomas Cerda
 * Released into the public domain
 */

#ifndef _talkingSensor_h_
#define _talkingSensor_h_

#include "Arduino.h"
#include <elapsedMillis.h>

#define DEFAULT_THRESHOLD 2000

class TalkingSensor {
  public:
    TalkingSensor(int digitalPin, int talkingThreshold = DEFAULT_THRESHOLD);
    bool isTalking();
  private:
    int _pin;
    int _talkingThreshold;
    elapsedMillis _timeSinceLastSound;
};

#endif
