#include <Arduino.h>
#include "initHand.h"

uint32_t uint32_from_serial3() {
/* Reads an uint32_t from Serial3, starting from the least-significant
 * and finishing with the most significant byte.
 */
  uint32_t num = 0;
  num = num | ((uint32_t) Serial3.read()) << 0;
  num = num | ((uint32_t) Serial3.read()) << 8;
  num = num | ((uint32_t) Serial3.read()) << 16;
  num = num | ((uint32_t) Serial3.read()) << 24;
  return num;
}

bool wait_on_serial3( uint8_t nbytes, long timeout ) {
  unsigned long deadline = millis() + timeout;//wraparound not a problem
  while (Serial3.available()<nbytes && (timeout<0 || millis()<deadline))
  {
    delay(1); // be nice, no busy loop
  }
  return Serial3.available()>=nbytes;
}


void uint32_to_serial3(uint32_t num) {
  /** Writes an uint32_t to Serial3, starting from the least-significant
   * and finishing with the most significant byte.
   */
  Serial3.write((char) (num >> 0));
  Serial3.write((char) (num >> 8));
  Serial3.write((char) (num >> 16));
  Serial3.write((char) (num >> 24));
}


void serverHand(){
  //The finite state machine for the server
  //This also returns the key of the client to the main handshake function
	char CR = 'C';
	char AR = 'A';
	enum State {LI,WFK1,WFA1,WFK2,WFA2,DX};
	State currentstate = LI;
	while (currentstate != DX) {

		if (currentstate==LI && Serial3.read()==CR) {
			currentstate = WFK1;
		}

		else if (currentstate == WFK1) {
			if (wait_on_serial3(1,1000)) {
				Serial3.print(AR);
				currentstate = WFA1;
			}
			else{
				currentstate = LI;
			}
		}

		else if (currentstate == WFA1) {
			if (wait_on_serial3(1,1000)) {
				char Recieved = Serial3.read();
				if(Recieved==CR) {
					currentstate = WFK2;
				}
				else if(Recieved==AR){
					currentstate = DX;
				}
				else{
					currentstate = LI;
				}
			}
			else{
				currentstate = LI;
			}
		}

		else if (currentstate == WFK2) {
			if (wait_on_serial3(1,1000)) {
				//true means the key is in the buffer
				currentstate = WFA2;
			}
			else{
				currentstate = LI;
			}
		}

		else if (currentstate == WFA2) {
			if (wait_on_serial3(1,1000)) {
				char Recieved = Serial3.read();
				if(Recieved==CR) {
					currentstate = WFK2;
				}
				else if(Recieved==AR){
					currentstate = DX;
				}
				else{
					currentstate = LI;
				}
			}
			else{
				currentstate = LI;
			}
		}

	}
}

void clientHand(){
  //The finite state machine for the client
  //This also returns the key of the server to the main handshake function
	char CR = 'C';
	char AR = 'A';
	while (true) {
		Serial3.print(CR);
		if (wait_on_serial3(1,1000)&&Serial3.read()==AR) {
			Serial3.print(AR);
			break;
		}
	}
}


void autoHandshake() {
  //calls the appropriate handshake,

	if (digitalRead(13)==1) {
		Serial.println("THIS IS THE SERVER");
		serverHand();

	}
	else{
		Serial.println("THIS IS THE CLIENT");
		clientHand();

	}

  //Printing notices to user
  Serial.println(' ');
  Serial.println("Successful Handshake");
  Serial.println("ready player 1");
  Serial.println(' ');

}
