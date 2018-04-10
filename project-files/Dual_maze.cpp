
#include <Arduino.h>
//#include <SPI.h>
//#include <SD.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
//#include <stdlib.h> //abs()

#include "Drawing.h"
#include "Map5088.h"
#include "initHand.h"

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

uint16_t PlayerX = 0;
uint16_t PlayerY = 0;
bool playerDead = false;
bool won1 = false;
bool won2 = false;

uint16_t colourRef[8] = {RED,ORANGE,_PINK,WHITE,YELLOW,GREEN,TEAL,BLUE};
bool colourState[8] = {false,false,false,false,false,false,false,false};
enum events {RED_CHANGE,ORANGE_CHANGE,PINK_CHANGE,WHITE_CHANGE,YELLOW_CHANGE,GREEN_CHANGE,TEAL_CHANGE,BLUE_CHANGE,DIED,OUT};


//104 -- 1 = negative(door only) -- 0 = color -- 4 = type(i.e. door)
//0grass -- 1wall -- 3switch -- 4door -- 5Pp -- 6end -- 7 Player start
extern uint8_t map1[2][16][12];

uint8_t MAP[16][12];

bool Grass = true;
// different than SD
//Sd2Card card;

//Definition only in this cpp


void setup() {
  init();
  Serial.begin(9600);
	Serial3.begin(9600);
  // including this seems to fix some SD card readblock errors
  // (at least on the old display)
  tft.begin();

  tft.fillScreen(BLACK);
  tft.setRotation(3);
  pinMode(JOY_SEL, INPUT_PULLUP);
  Serial.print("Git status ");
  /*
  Serial.print("Initializing SPI communication for raw reads..");
  if (!card.init(SPI_HALF_SPEED, SD_CS)) {
    Serial.println("Failed! Is the card inserted properly?");
    while (true) {}
  }
  else {
    Serial.println("OK");
  }

	Serial.print("Initializing SD card..");
	if (!SD.begin(SD_CS)) {
		Serial.println("Failed! Is it inserted properly?");
		while (true) {}
	}
  */
}


void refreshDoor(uint8_t index){
  uint8_t mapIndexLower = 0;
  uint8_t mapIndexUpper = 0;
  for (uint16_t i = 0; i < DISPLAY_WIDTH; i++) {
    for (uint16_t j = 0; j < DISPLAY_HEIGHT; j++) {
      mapIndexLower = MAP[i][j]%10;
      mapIndexUpper = (MAP[i][j]-mapIndexLower)/10;
      if ((mapIndexLower==4)&&(index%10==mapIndexUpper%10)) {
        drawDoor(i,j,mapIndexUpper);
        if ((PlayerX == i)&&(PlayerY == j)) {
          playerDead = true;
        }
      }
    }
  }
}
void refreshSwitch(uint8_t index){
  uint8_t mapIndexLower = 0;
  uint8_t mapIndexUpper = 0;
  for (uint16_t i = 0; i < DISPLAY_WIDTH; i++) {
    for (uint16_t j = 0; j < DISPLAY_HEIGHT; j++) {
      mapIndexLower = MAP[i][j]%10;
      mapIndexUpper = (MAP[i][j]-mapIndexLower)/10;
      if ((mapIndexLower==3)&&(index==mapIndexUpper)) {
        drawSwitch(i,j,mapIndexUpper);
        if ((PlayerX == i)&&(PlayerY == j)) {
          drawPlayer();
        }
      }
    }
  }
}
void refreshGrass(){
  Grass = !Grass;
  uint16_t mapIndex = 0;
  for (uint16_t i = 0; i < DISPLAY_WIDTH; i++) {
    for (uint16_t j = 0; j < DISPLAY_HEIGHT; j++) {
      mapIndex = MAP[i][j];
      if (mapIndex==0 && !(i == PlayerX && j == PlayerY)) {
        mow(i,j);
      }
    }
  }
}
void moveOff(uint16_t x, uint16_t y){
  uint8_t type = MAP[x][y];
  uint8_t index = (type - (type % 10))/10;
  //will serial3 write in here
  switch (type % 10) {
    case 0 :
    drawGround(x,y);
    break;
    case 3 :
    drawSwitch(x,y,index);
    break;
    case 4 :
    drawDoor(x,y,index);
    break;
    case 5 :
    //pressure plate case
    colourState[index] = !colourState[index];
    drawPpOff(x,y,colourRef[index]);
    refreshDoor(index);
    refreshSwitch(index);
    Serial3.print(index%10); //send an enum update associated w color
    break;
    case 6 :
    //exit case
    won1 = false;
    drawEnd(x,y);
    Serial3.print(OUT);
    break;
    case 7 :
    drawGround(x,y);
    break;
    default :break;
  }
}
bool moveOn(uint16_t x, uint16_t y) {
  uint8_t type = MAP[x][y];
  uint8_t index = (type - (type % 10))/10;
  //will serial3 write in switch
  switch (type % 10) {
    case 0 :
    return true;
    case 1 :
    return false;
    case 3 :
    //on a switch
    colourState[index] = !colourState[index];
    refreshSwitch(index);
    refreshDoor(index);
    playerDead = false;
    Serial3.print(index%10);//send an enum update associated w color
    return true;
    case 4 :
    //door case
    if (colourState[index%10]^(type>100)) {
      drawDoor(x,y,index);
      return true;
    }
    return false;
    case 5 :
    //on a pressure plate
    colourState[index] = !colourState[index];
    drawPpOn(x,y,colourRef[index]);
    refreshDoor(index);
    Serial3.print(index%10);//send an enum update associated w color
    refreshSwitch(index);
    playerDead = false;
    //Serial.print(index%10); //for testing
    /*
    if(index%10 == 0){
      Serial.print(RED_CHANGE);
    }
    */
    return true;
    case 6 :
    won1 = true;
    Serial3.print(OUT);
    return true;
    case 7 :
    return true;
    default:
    return false;
  }
}
bool processJoystick(bool canMove) {
  if (!canMove) {
    return false;
  }
  // reading the joystick
  uint16_t xVal = 1024 - analogRead(JOY_HORIZ);
  uint16_t yVal = analogRead(JOY_VERT);
  //checking if the joystick position would change the cursor position
  uint16_t newpositionY = constrain(checkJoy(yVal,PlayerY),0,DISPLAY_HEIGHT - 1);
  uint16_t newpositionX = constrain(checkJoy(xVal,PlayerX),0,DISPLAY_WIDTH - 1);
  if (canMove&&((newpositionX != PlayerX)^(newpositionY != PlayerY))&&moveOn(newpositionX,newpositionY)){
    uint16_t oldX = PlayerX;
    uint16_t oldY = PlayerY;
    PlayerX = newpositionX;
    PlayerY = newpositionY;
    moveOff(oldX,oldY);
    drawPlayer();
    return false;
  }
  else{
    return true;
  }
}

void Menu(){
  bool server = digitalRead(13);
  tft.fillScreen(BLACK);
  tft.setTextColor(ORANGE,BLACK);
  tft.setTextSize(4);
  tft.setCursor(50,70);
  tft.print("Duel Maze");
  bool readyPlayer1 = digitalRead(JOY_SEL);
  while(true){
    //update readyPlayer1
    readyPlayer1 = digitalRead(JOY_SEL);
    if (!readyPlayer1) {
      break;
    }

  }
  for (uint16_t i = 0; i < DISPLAY_WIDTH; i++) {
    for (uint16_t j = 0; j < DISPLAY_HEIGHT; j++) {
      MAP[i][j] = map1[server][i][j];
    }
  }
  tft.setTextSize(4);
  tft.setCursor(120,120);
  tft.print("Ready");

  while(true){
    //waiting on other player screen
    Serial3.print('A');//let the other player know you are ready
    if(Serial3.available() != 0){
      if(Serial3.read() == 'A'){
        break;
      }
    } //is other ready?

  }

    //wait until they are ready (sending im ready while you check)


}



int main() {
  setup();
    autoHandshake();
    while (true) {
        Menu();

        //initial conditions
        won1 = false;
        won2 = false;
        playerDead = false;
        for (int i = 0; i < 8; i++) {
          colourState[i] = false;
        }
        loadMap();


        uint16_t startG = millis();
        uint16_t TimeG = 0;
        uint16_t markG = 500;

        uint16_t TimeP = millis();
        uint16_t markP = 333;
        uint16_t startP = millis();
        bool canMove = true;
        bool startMove = false;

        while (true) { // in game loop
            if (TimeG > markG){
                //refreshGrass();
                startG = millis();
                TimeG = 0;
            }
            TimeG = millis() - startG;

            //seral3availalb stuff here
            if(Serial3.available() !=0 ){ //something recived over serial
              //Serial.print("recived: ");
              int recived = Serial3.read() - 48;
              //Serial.print(recived);
              switch(recived){
                case RED_CHANGE:
                case ORANGE_CHANGE:
                case PINK_CHANGE:
                case WHITE_CHANGE:
                case YELLOW_CHANGE:
                case GREEN_CHANGE:
                case TEAL_CHANGE:
                case BLUE_CHANGE:
                  colourState[recived] = !colourState[recived];
                  refreshDoor(recived);
                  refreshSwitch(recived);
                  break;
                case DIED:
                  playerDead = true;
                  break;
                case OUT:
                  won2 = !won2; //change the other players out status
                  break;
                default:
                break;
              }

            }
            canMove = processJoystick(canMove);
            if (startMove) {
              if (!canMove) {
                TimeP = millis();
                  if (TimeP > startP + markP) {
                      canMove = true;
                      TimeP = millis();
                      startP = millis();
                  }
              }
              else{
                startMove = false;
              }
            }
            else{
              if (!canMove) {
                startMove = true;
              }
              startP = millis();
            }


            if (won1 && won2) {
              //YOU BOTH GOT OUT YAAAY
              //record the time
              drawWin();
              break;
            }
            if (playerDead) {
              //someome got smushed activate the dead screen
              Serial3.print(DIED);
              drawDeath();
              break;
            }
        }
    }
  Serial3.end();
  Serial.end();
  return 0;
}
