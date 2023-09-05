
/*
  simpleMovements.ino

 This  sketch simpleMovements shows how they move each servo motor of Braccio

 Created on 18 Nov 2015
 by Andrea Martino

 This example is in the public domain.
 */

#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int base_int = 90;
int shoulder_int = 45;
int elbow_int = 180;
int w_vert_int = 180;
int w_rot_int = 90;
int gripper_int = 45;


void setup() {
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  Braccio.begin();
}

//Accepts an integer between 0 to 100 indicating how "strong" the grip strength should be
void grip_strength(int strength) {
  gripper_int = 63 / 100 * strength + 10;
}

void loop() {
  char c;
  // w_vert_int =90;
  // elbow_int=90;
  // shoulder_int=90;
   Braccio.ServoMovement(20, base_int, shoulder_int, elbow_int, w_vert_int, w_rot_int, gripper_int);
     delay(5);
  // if (Serial.available() > 0) {

  //   c = Serial.read();


  //   w_rot_int=c;


  // } else {
    
  // }

  // // gripper_int = gripper_int + 1;
 
  // // }
  //  /*
  //  Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
  //  M1=base degrees. Allowed values from 0 to 180 degrees
  //  M2=shoulder degrees. Allowed values from 15 to 165 degrees
  //  M3=elbow degrees. Allowed values from 0 to 180 degrees
  //  M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
  //  M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
  //  M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  // */

  //                      //(step delay, M1, M2, M3, M4, M5, M6);
  // Braccio.ServoMovement(20, base_int, shoulder_int, elbow_int, w_vert_int, w_rot_int, gripper_int);  

  // //Braccio.ServoMovement(20,           180,  165, 0, 0, 180,  10);  

  // //Wait 1 second
  // delay(0);

  //     //w_rot_int++;

  //     if(w_rot_int > 180) {
  //     w_rot_int = 0;
  //     }
       Braccio.ServoMovement(20, base_int, shoulder_int, elbow_int, w_vert_int, w_rot_int, gripper_int);  
       delay(0);
}
