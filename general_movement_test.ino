#include <DFRobot_BMX160.h>
DFRobot_BMX160 bmx160;

// Movement threshold (adjust as needed)
#define MOVEMENT_THRESHOLD 5

float prevX = 0, prevY = 0, prevZ = 0;

void setup(){
  Serial.begin(115200);
  delay(100);
  
  //init the hardware bmx160  
  while (bmx160.begin() != true){
    Serial.println("Initialization failed! Check your wiring.");
    delay(1000);
  }
  delay(100);
}

void loop(){  
  // Serial.println("hi");
  sBmx160SensorData_t Omagn, Ogyro, Oaccel;
  bmx160.getAllData(&Omagn, &Ogyro, &Oaccel);
    int delayCounter = 0;
    // Convert raw acceleration data to g-force
    float ax = Oaccel.x;
    float ay = Oaccel.y;
    float az = Oaccel.z;
    //delay (500);
    // Compute change in acceleration
    float deltaX = abs(ax - prevX);
    float deltaY = abs(ay - prevY);
    float deltaZ = abs(az - prevZ);
    
    // If movement exceeds threshold, print a message
    if (deltaX > MOVEMENT_THRESHOLD || deltaY > MOVEMENT_THRESHOLD || deltaZ > MOVEMENT_THRESHOLD) {
        Serial.println("Significant movement!");
        delay(3000);
      float ax = Oaccel.x;
      float ay = Oaccel.y;
      float az = Oaccel.z;
          // Test by moving it to the if statement so that delta will keep increasing until it reaches the tolerance
    // Then it'll get hit with the 3s delay before resetting everything again and start scanning for movement
    prevX = ax;
    prevY = ay;
    prevZ = az;
    }


    // Update previous values

    delay(100); // Adjust delay as needed
}