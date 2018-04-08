#ifndef _initHand_h
#define _initHand_h

uint32_t uint32_from_serial3();
bool wait_on_serial3( uint8_t nbytes, long timeout );
void uint32_to_serial3(uint32_t num);
void serverHand();
void clientHand();
void autoHandshake();
void setup();

#endif
