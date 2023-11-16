#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int base_int = 90; // Case D
int shoulder_int = 45; //Case A
int elbow_int = 180; //Case B
int w_vert_int = 180; //Case C
int w_rot_int = 90; //Case E
int gripper_int = 45; //Case F


void setup() {
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  delay(2000);


  Braccio.begin();
}

void loop() {
Serial.println("Program start");
int count=1;
char c='0';
int t='0';
while(1)
{
  if (Serial.available() > 1) 
  {
    c=Serial.read();
    Serial.print("C: ");
    Serial.println(c); 
    t=Serial.read();
    Serial.print("T: ");
    Serial.println(t);
    // C represents the part of the arm that will be moving, the arm will idle in it's default position until 
    // it receives a command via the serial port
  
  }
  else
  {

  }
  if(gripper_int > 73) { // More random debug code that can be removed later
    gripper_int = 10;
  }


  // if(c != '0'){
  //   Serial.print("Loop#:");
  //   Serial.println((int)count);  
  //   Serial.print("Value of c");
  //   Serial.println((char)c);
  // }
  //Outputs to verify that the code is progressing through the loops and is checking the serial port,
  //also verifies the code is progressing but taking no action when no command is received
  switch(c)
  {
    case 'A': // Case for shoulder joint
      shoulder_int = t;
      shoulder.write(t);
      // Serial.print("Shoulder_int: ");
      // Serial.println(t, DEC);
    break;

    case 'B': // case for elbow joint
      elbow_int = t;
      elbow.write(t);
      // Serial.print("Elbow_int: ");
      // Serial.println(t, DEC);
    break;

    case 'C': // case for wrist joint ( non-rotational )
      w_vert_int = t;
      wrist_ver.write(t);
      // Serial.print("W_vert_int: ");
      // Serial.println(t, DEC);
    break;

    case 'D': // Case for shoulder joint
      base_int = t;
      base.write(t);
      // Serial.print("Base_int: ");
      // Serial.println(t, DEC);
    break;

     case 'E': // Case for shoulder joint
      wrist_rot.write(t);
      // Serial.print("W_rot_int: ");
      // Serial.println(t, DEC);
    break;

    case 'F': // Case for shoulder joint
      gripper.write(t);
      // Serial.print("gripper_int: ");
      // Serial.println(t, DEC);
    break;
    default:
      //Serial.print("Error");
    break;
  }
  t=0;
  c='0';

   /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */

  //(step delay, M1, M2, M3, M4, M5, M6);  
  
  count++;
}
}

