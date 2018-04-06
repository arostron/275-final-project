#ifndef _Drawing_h
#define _Drawing_h


#define TFT_DC 9
#define TFT_CS 10
#define SD_CS 6

#define DISPLAY_P_WIDTH  320
#define DISPLAY_P_HEIGHT 240
#define DISPLAY_WIDTH  16
#define DISPLAY_HEIGHT 12
#define BLOCK_SIZE 20
//16 * 12 20p

#define JOY_VERT  A1 // should connect A1 to pin VRx
#define JOY_HORIZ A0 // should connect A0 to pin VRy
#define JOY_SEL  2
#define JOY_CENTER  512
#define DEADZONE 100

#define GROUND 0x0341
#define GROUND1 0x0E00
#define WALL 0xAAA0
#define WALL1 0x5A20
#define PLAYER 0xE7C8
#define PLAYER1 0x439F
#define PLAYER2 0xD820
#define PLAYER3 0xFEC1
#define BLACK 0x0000
#define _PINK 0xE00F
#define WHITE 0xFFFF
#define BLUE 0x43FF
#define GREEN 0x0F86
#define YELLOW 0xF6C9
#define TEAL 0x00F0
#define RED 0xF000
#define ORANGE 0xFC40


void drawPlayer();
void drawGround1(uint16_t x, uint16_t y);
void drawGround2(uint16_t x, uint16_t y);
void drawGround(uint16_t x, uint16_t y);
void mow(uint16_t x, uint16_t y);
void drawWall(uint16_t x, uint16_t y);
void drawClosedDoor(uint16_t x, uint16_t y, uint16_t colour);
void drawOpenDoor(uint16_t x, uint16_t y, uint16_t colour);
void drawEnd(uint16_t x, uint16_t y);
void drawOnSwitch(uint16_t x, uint16_t y, uint16_t colour);
void drawOffSwitch(uint16_t x, uint16_t y, uint16_t colour);
void loadMap();
int checkJoy(uint16_t Val,uint16_t newpos);
void drawSwitch(uint16_t x, uint16_t y, uint16_t index);
void drawDoor(uint16_t x, uint16_t y, uint16_t index);
void drawPpOff(uint16_t x, uint16_t y, uint16_t colour);
void drawPpOn(uint16_t x, uint16_t y, uint16_t colour);
void drawDeath();
void drawWin();
void drawMenu();


#endif
