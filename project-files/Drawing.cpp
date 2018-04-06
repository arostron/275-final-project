#include <Arduino.h>
//#include <SPI.h>
//#include <SD.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
//#include <stdlib.h> //abs()

#include "Drawing.h"

extern Adafruit_ILI9341 tft;

extern uint16_t PlayerX;
extern uint16_t PlayerY;
extern bool playerDead;

extern uint16_t colourRef[8];
extern bool colourState[8];
/*
0 = empty/walkway
1 = wall
2 = player
**3 = coloured switch
*4 = coloured door
*/
extern uint8_t MAP[16][12];

extern bool Grass;

void drawPlayer() {
  uint16_t x = PlayerX*BLOCK_SIZE;
  uint16_t y = PlayerY*BLOCK_SIZE;
  tft.drawLine(x+7,y+8,x+3,y+13,PLAYER);
  tft.drawLine(x+12,y+8,x+16,y+13,PLAYER);
  tft.fillRect(x+7,y+3,6,11,PLAYER2);
  tft.fillRect(x+7,y+13,6,1,PLAYER1);
  tft.fillRect(x+7,y+14,2,4,PLAYER1);
  tft.fillRect(x+11,y+14,2,4,PLAYER1);
  tft.fillRoundRect(x+5,y+1,10,7,3,BLACK);
  tft.fillRoundRect(x+7,y+1,8,7,3,PLAYER);
}
void drawGround1(uint16_t x, uint16_t y){
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRect(x,y,BLOCK_SIZE,BLOCK_SIZE,GROUND);
  tft.drawLine(x+5,y+19,x+7,y+16,GROUND1);
  tft.drawLine(x+17,y+14,x+16,y+12,GROUND1);
  tft.drawLine(x+1,y+11,x+2,y+9,GROUND1);
  tft.drawLine(x+5,y+5,x+3,y+2,GROUND1);
  tft.drawLine(x+10,y+11,x+12,y+8,GROUND1);
  tft.drawLine(x+14,y+17,x+14,y+15,GROUND1);
  tft.drawLine(x+18,y+4,x+17,y+3,GROUND1);
  tft.drawLine(x+7,y+7,x+7,y+5,GROUND1);
  tft.drawLine(x+13,y+6,x+12,y+4,GROUND1);
  tft.drawLine(x+4,y+16,x+2,y+15,GROUND1);
}
void drawGround2(uint16_t x, uint16_t y){
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRect(x,y,BLOCK_SIZE,BLOCK_SIZE,GROUND);
  tft.drawLine(x+5,y+19,x+6,y+16,GROUND1);
  tft.drawLine(x+17,y+14,x+15,y+12,GROUND1);
  tft.drawLine(x+1,y+11,x+1,y+9,GROUND1);
  tft.drawLine(x+5,y+5,x+2,y+2,GROUND1);
  tft.drawLine(x+10,y+11,x+11,y+8,GROUND1);
  tft.drawLine(x+14,y+17,x+13,y+15,GROUND1);
  tft.drawLine(x+18,y+4,x+16,y+3,GROUND1);
  tft.drawLine(x+7,y+7,x+6,y+5,GROUND1);
  tft.drawLine(x+13,y+6,x+11,y+4,GROUND1);
  tft.drawLine(x+4,y+16,x+1,y+15,GROUND1);
}
void drawGround(uint16_t x, uint16_t y){
  if (Grass) {
    drawGround1(x,y);
  }
  else{
    drawGround2(x,y);
  }
}
void mow(uint16_t x, uint16_t y) {
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  if (Grass) {
    tft.drawLine(x+5,y+19,x+6,y+16,GROUND);
    tft.drawLine(x+5,y+19,x+7,y+16,GROUND1);
    tft.drawLine(x+17,y+14,x+15,y+12,GROUND);
    tft.drawLine(x+17,y+14,x+16,y+12,GROUND1);
    tft.drawLine(x+1,y+11,x+1,y+9,GROUND);
    tft.drawLine(x+1,y+11,x+2,y+9,GROUND1);
    tft.drawLine(x+5,y+5,x+2,y+2,GROUND);
    tft.drawLine(x+5,y+5,x+3,y+2,GROUND1);
    tft.drawLine(x+10,y+11,x+11,y+8,GROUND);
    tft.drawLine(x+10,y+11,x+12,y+8,GROUND1);
    tft.drawLine(x+14,y+17,x+13,y+15,GROUND);
    tft.drawLine(x+14,y+17,x+14,y+15,GROUND1);
    tft.drawLine(x+18,y+4,x+16,y+3,GROUND);
    tft.drawLine(x+18,y+4,x+17,y+3,GROUND1);
    tft.drawLine(x+7,y+7,x+6,y+5,GROUND);
    tft.drawLine(x+7,y+7,x+7,y+5,GROUND1);
    tft.drawLine(x+13,y+6,x+11,y+4,GROUND);
    tft.drawLine(x+13,y+6,x+12,y+4,GROUND1);
    tft.drawLine(x+4,y+16,x+1,y+15,GROUND);
    tft.drawLine(x+4,y+16,x+2,y+15,GROUND1);
  }
  else{
    tft.drawLine(x+5,y+19,x+7,y+16,GROUND);
    tft.drawLine(x+5,y+19,x+6,y+16,GROUND1);
    tft.drawLine(x+17,y+14,x+16,y+12,GROUND);
    tft.drawLine(x+17,y+14,x+15,y+12,GROUND1);
    tft.drawLine(x+1,y+11,x+2,y+9,GROUND);
    tft.drawLine(x+1,y+11,x+1,y+9,GROUND1);
    tft.drawLine(x+5,y+5,x+3,y+2,GROUND);
    tft.drawLine(x+5,y+5,x+2,y+2,GROUND1);
    tft.drawLine(x+10,y+11,x+12,y+8,GROUND);
    tft.drawLine(x+10,y+11,x+11,y+8,GROUND1);
    tft.drawLine(x+14,y+17,x+14,y+15,GROUND);
    tft.drawLine(x+14,y+17,x+13,y+15,GROUND1);
    tft.drawLine(x+18,y+4,x+17,y+3,GROUND);
    tft.drawLine(x+18,y+4,x+16,y+3,GROUND1);
    tft.drawLine(x+7,y+7,x+7,y+5,GROUND);
    tft.drawLine(x+7,y+7,x+6,y+5,GROUND1);
    tft.drawLine(x+13,y+6,x+12,y+4,GROUND);
    tft.drawLine(x+13,y+6,x+11,y+4,GROUND1);
    tft.drawLine(x+4,y+16,x+2,y+15,GROUND);
    tft.drawLine(x+4,y+16,x+1,y+15,GROUND1);
  }
}
void drawWall(uint16_t x, uint16_t y){
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRect(x,y,BLOCK_SIZE,BLOCK_SIZE,WALL);
  tft.fillRect(x,y+1,9,8,WALL1);
  tft.fillRect(x+11,y+1,9,8,WALL1);
  tft.fillRect(x+1,y+11,18,8,WALL1);
}
void drawClosedDoor(uint16_t x, uint16_t y, uint16_t colour) {
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRect(x,y,BLOCK_SIZE,BLOCK_SIZE,WALL);
  tft.drawRect(x+1,y+1,BLOCK_SIZE-2,BLOCK_SIZE-2,colour);
  tft.fillTriangle(x+4,y+4,x+4,y+9,x+9,y+4,colour);
  tft.fillTriangle(x+15,y+4,x+15,y+9,x+10,y+4,colour);
  tft.fillTriangle(x+4,y+15,x+4,y+10,x+9,y+15,colour);
  tft.fillTriangle(x+15,y+15,x+15,y+10,x+10,y+15,colour);
}
void drawOpenDoor(uint16_t x, uint16_t y, uint16_t colour) {
  drawGround(x,y);
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillTriangle(x,y,x+5,y,x,y+5,colour);
  tft.fillTriangle(x+19,y,x+14,y,x+19,y+5,colour);
  tft.fillTriangle(x,y+19,x+5,y+19,x,y+14,colour);
  tft.fillTriangle(x+19,y+19,x+14,y+19,x+19,y+14,colour);
}
void drawEnd(uint16_t x, uint16_t y){
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRect(x,y,BLOCK_SIZE,BLOCK_SIZE,GROUND);
  tft.drawRect(x,y,BLOCK_SIZE ,BLOCK_SIZE ,WHITE);
  tft.drawRect(x+1,y+1,BLOCK_SIZE-2,BLOCK_SIZE-2,WHITE);
  tft.drawRect(x+5,y+5,BLOCK_SIZE-10,BLOCK_SIZE-10,WHITE);
  tft.drawFastVLine(x+6,y+6,8,_PINK);
  tft.drawFastVLine(x+7,y+6,8,RED);
  tft.drawFastVLine(x+8,y+6,8,YELLOW);
  tft.drawFastVLine(x+9,y+6,8,WHITE);
  tft.drawFastVLine(x+10,y+6,8,GREEN);
  tft.drawFastVLine(x+11,y+6,8,TEAL);
  tft.drawFastVLine(x+12,y+6,8,BLUE);
  tft.drawFastVLine(x+13,y+6,8,BLACK);
}
void drawOnSwitch(uint16_t x, uint16_t y, uint16_t colour){
  drawGround(x,y);
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillCircle(x+17,y+17,2,colour);
  tft.fillRoundRect(x+1,y+15,16,4,1,BLACK);
  tft.drawRoundRect(x+1,y+15,16,4,1,colour);
  for (int i = 0; i < 4; i++) {
    tft.drawLine(x+7+i,y+17,x+12+i,y+9,WHITE);
  }
  tft.fillCircle(x+13,y+9,4,BLACK);
  tft.fillCircle(x+14,y+9,3,colour);
}
void drawOffSwitch(uint16_t x, uint16_t y, uint16_t colour){
  drawGround(x,y);
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillCircle(x+17,y+17,2,colour);
  tft.fillRoundRect(x+1,y+15,16,4,1,BLACK);
  tft.drawRoundRect(x+1,y+15,16,4,1,colour);
  for (int i = 0; i < 4; i++) {
    tft.drawLine(x+7+i,y+17,x+5+i,y+9,WHITE);
  }
  tft.fillCircle(x+6,y+9,4,BLACK);
  tft.fillCircle(x+7,y+9,3,colour);
}
int checkJoy(uint16_t Val,uint16_t newpos){
		if (Val < JOY_CENTER - DEADZONE) {
			newpos -= 1;
		}
		else if (Val > JOY_CENTER + DEADZONE) {
			newpos += 1;
		}
	return newpos;
}
void drawSwitch(uint16_t x, uint16_t y, uint16_t index){
  if (colourState[index]) {
    drawOnSwitch(x,y,colourRef[index]);
  }
  else{
    drawOffSwitch(x,y,colourRef[index]);
  }
}
void drawDoor(uint16_t x, uint16_t y, uint16_t index){
  uint8_t i1 = index % 10;
  uint8_t i2 = (index-(i1))/10;
  if (colourState[i1]^i2) {
    drawOpenDoor(x,y,colourRef[i1]);
  }
  else{
    drawClosedDoor(x,y,colourRef[i1]);
  }
}
void drawPpOff(uint16_t x, uint16_t y, uint16_t colour){
  drawGround(x,y);
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRoundRect(x+6,y+15,8,5,2,BLACK);
  tft.fillRoundRect(x+6,y+13,8,5,2,colour);
}
void drawPpOn(uint16_t x, uint16_t y, uint16_t colour){
  drawGround(x,y);
  x = x*BLOCK_SIZE;
  y = y*BLOCK_SIZE;
  tft.fillRoundRect(x+6,y+15,8,5,2,colour);
}

void loadMap(){
  uint8_t type = 0;
  for (uint16_t i = 0; i < DISPLAY_WIDTH; i++) {
    for (uint16_t j = 0; j < DISPLAY_HEIGHT; j++) {
      type = MAP[i][j];
      if ((type % 10) == 7) {
        drawGround(i,j);
        PlayerX = i;
        PlayerY = j;
        drawPlayer();
      }
      else{
      uint8_t index = (type - (type % 10))/10;
      switch (type % 10) {
        case 0 : drawGround(i,j);
        break;
        case 1 : drawWall(i,j);
        break;
        case 3 : drawSwitch(i,j,index);
        break;
        case 4 : drawDoor(i,j,index);
        break;
        case 5 : drawPpOff(i,j,colourRef[index]);
        break;
        case 6 : drawEnd(i,j);
        default:break;
      }
    }
  }
  }
}
void ice(uint16_t index){
  if ((index < floor(DISPLAY_P_WIDTH/5))&&(index % 3 ==0)) {
    tft.drawLine(0,0,index,DISPLAY_P_HEIGHT,0x000D);
    tft.drawLine(index,0,0,DISPLAY_P_HEIGHT,0x000A);
    tft.drawLine(DISPLAY_P_WIDTH,0,DISPLAY_P_WIDTH - index,DISPLAY_P_HEIGHT,0x000C);
    tft.drawLine(DISPLAY_P_WIDTH - index,0,DISPLAY_P_WIDTH,DISPLAY_P_HEIGHT,0x000B);
  }
}
void sun(uint16_t index){
  if ((index < DISPLAY_P_HEIGHT)&&(index % 3 ==0)) {
    for (int i = 0; i < 30; i++) {
      tft.drawLine(DISPLAY_P_WIDTH,0,
        DISPLAY_P_WIDTH - index + floor(index*cos(i)),
        floor(index*sin(i)),
        PLAYER);
    }

  }
}
void drawDeath(){
  uint16_t back = BLACK;
  uint16_t front = RED;
  tft.fillScreen(back);
  //tft.drawTriangle(0,0,0,30,30,0,_PINK);
  tft.setTextColor(front,back);
  tft.setTextSize(2);
  tft.setCursor(95,35);
  tft.print("SOMEONE GOT");
  tft.setTextSize(6);
  tft.setCursor(25,75);
  tft.print("SMUSHED!");
  tft.setTextSize(3);
  uint16_t temp = 0;
  uint8_t index = 0;
  uint16_t icy = 0;
  bool select = false;
  //bool dig = false;
  while (true) {
    tft.setCursor(75,180);
    tft.setTextColor(front,back);
    tft.print("Try Again?");
    bool dig = digitalRead(JOY_SEL);
    if (!dig) {
      select = true;
    }
    if (select) {
      delay(25);
      index++;
    }
    else{
      delay(100);
      icy++;
      ice(icy);
    }
    if (index == 20) {
      break;
    }
    temp = front;
    front = back;
    back = temp;
  }
  tft.fillScreen(BLACK);

}

void drawWin(){
  uint16_t back = WHITE;
  uint16_t front = ORANGE;
  tft.fillScreen(back);
  tft.fillCircle(300,290,90,GROUND);
  tft.fillCircle(305,295,89,GREEN);
  tft.setTextColor(front,back);
  tft.setTextSize(3);
  tft.setCursor(135,35);
  tft.print("YOU");
  tft.setTextSize(6);
  tft.setCursor(110,75);
  tft.print("WON");
  tft.setTextSize(3);
  uint16_t temp = 0;
  uint8_t index = 0;
  bool select = false;
  bool dig = false;
  uint16_t sunny = 0;
  while (true) {
    tft.setCursor(65,180);
    tft.setTextColor(front,back);
    tft.print("Play Again?");
    dig = digitalRead(JOY_SEL);
    if (!dig) {
      select = true;
    }
    if (select) {
      delay(25);
      index++;
    }
    else{
      delay(100);
      sunny++;
      sun(sunny);
    }
    if (index == 20) {
      break;
    }
    temp = front;
    front = back;
    back = temp;
  }
  tft.fillScreen(BLACK);
}
void drawMenu(){

}
