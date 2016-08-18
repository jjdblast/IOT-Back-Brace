
#include <SoftwareSerial.h>

//////////////////////
// Credits
//
// I2C device class (I2Cdev) demonstration Arduino sketch for MPU6050 class using DMP (MotionApps v2.0)
// 6/21/2012 by Jeff Rowberg <jeff@rowberg.net>
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib


///////////////////////////////////////////////////////////////////////////////
// MPU6050 Variables
// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"
//#include "MPU6050.h" // not necessary if using MotionApps include file

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for SparkFun breakout and InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 mpu;
//MPU6050 mpu(0x69); // <-- use for AD0 high

// uncomment "OUTPUT_READABLE_YAWPITCHROLL" if you want to see the yaw/
// pitch/roll angles (in degrees) calculated from the quaternions coming
// from the FIFO. Note this also requires gravity vector calculations.
// Also note that yaw/pitch/roll angles suffer from gimbal lock (for
// more info, see: http://en.wikipedia.org/wiki/Gimbal_lock)
#define OUTPUT_READABLE_YAWPITCHROLL

#define INTERRUPT_PIN 2  // use pin 2 on Arduino Uno & most boards
#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

float pitchAngle;


// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
//////////////////////////////////////////
// ESP8266 Variables
/////////////////////////////////////////


SoftwareSerial esp(6, 7);// RX, TX

// Variables used in POST packet
//char deviceID[] = "ac423eb65d4a32";
//char metricTypeID[] = "6";
//char uomID[] = "4";

int connectionStatus;
int tcpConnectionStatus;void dmpDataReady() {
    mpuInterrupt = true;
}



///////////////////////////////////////////////
// Other Variables
//////////////////////////////////////////////

float yawSetRunningTotal;
float yawSetPoint;
float pitchSetRunningTotal;
float pitchSetPoint;
float rollSetRunningTotal;
float rollSetPoint;
float yawDiffRunningTotal;
float pitchDiffRunningTotal;
float rollDiffRunningTotal;
int numberSetReadings = 100; // Numbere of readings to create setPoints
int readingsToReport = 10; // Report every 10 readings that are above threshold
bool gettingSetPoints = true;

float prevYawReading;
float prevPitchReading;
float prevRollReading;
float changeThreshold = 0.25;


void setup() 
  {
    
    ///////////////////////////////////
    // ESP8266 Setup
    esp.begin(9600);
    resetEsp();
    randomSeed(analogRead(0));
    
    //////////////////////////////////////////////////////
    //IMU Setup
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (115200 chosen because it is required for Teapot Demo output, but it's
    // really up to you depending on your project)
    Serial.begin(115200);
    while (!Serial); // wait for Leonardo enumeration, others continue immediately

    // NOTE: 8MHz or slower host processors, like the Teensy @ 3.3v or Ardunio
    // Pro Mini running at 3.3v, cannot handle this baud rate reliably due to
    // the baud timing being too misaligned with processor ticks. You must use
    // 38400 or slower in these cases, or use some kind of external separate
    // crystal solution for the UART timer.

    // initialize device
    Serial.println(F("Initializing I2C devices..."));
    mpu.initialize();
    pinMode(INTERRUPT_PIN, INPUT);

    // verify connection
    Serial.println(F("Testing device connections..."));
    Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

    // wait for ready
    Serial.println(F("\nSend any character to begin DMP programming and demo: "));
    while (Serial.available() && Serial.read()); // empty buffer
    while (!Serial.available());                 // wait for data
    while (Serial.available() && Serial.read()); // empty buffer again

    // load and configure the DMP
    Serial.println(F("Initializing DMP..."));
    devStatus = mpu.dmpInitialize();

    // supply your own gyro offsets here, scaled for min sensitivity
    mpu.setXGyroOffset(117);
    mpu.setYGyroOffset(-16);
    mpu.setZGyroOffset(40);
    mpu.setZAccelOffset(1162); // 1688 factory default for my test chip
    //mpu.setXGyroOffset(220);
    //mpu.setYGyroOffset(76);
    //mpu.setZGyroOffset(-85);
    //mpu.setZAccelOffset(1788); // 1688 factory default for my test chip

    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // turn on the DMP, now that it's ready
        Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        // enable Arduino interrupt detection
        Serial.println(F("Enabling interrupt detection (Arduino external interrupt 0)..."));
        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        Serial.print(F("DMP Initialization failed (code "));
        Serial.print(devStatus);
        Serial.println(F(")"));
    }

    // configure LED for output
    pinMode(LED_PIN, OUTPUT);

    
  }// End Setup
  
  void loop()
  {
      
      // if programming failed, don't try to do anything
    if (!dmpReady) return;

    // wait for MPU interrupt or extra packet(s) available
    while (!mpuInterrupt && fifoCount < packetSize) {
        // other program behavior stuff here
        // .
        // .
        // .
        // if you are really paranoid you can frequently test in between other
        // stuff to see if mpuInterrupt is true, and if so, "break;" from the
        // while() loop to immediately process the MPU data
        // .
        // .
        // .
    }

    // reset interrupt flag and get INT_STATUS byte
    mpuInterrupt = false;
    mpuIntStatus = mpu.getIntStatus();

    // get current FIFO count
    fifoCount = mpu.getFIFOCount();

    // check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
        // reset so we can continue cleanly
        mpu.resetFIFO();
        Serial.println(F("FIFO overflow!"));

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus & 0x02) {
        // wait for correct available data length, should be a VERY short wait
        while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

        // read a packet from FIFO
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize;


        #ifdef OUTPUT_READABLE_YAWPITCHROLL
            // display Euler angles in degrees
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

            float yawReading = ypr[0] * 180/M_PI;
            float pitchReading = ypr[1] * 180/M_PI;
            float rollReading = ypr[2] * 180/M_PI;

            if(!gettingSetPoints) 
            {
              processReading(yawReading, pitchReading, rollReading);
            }
            else {
              yawSetRunningTotal += yawReading;
              pitchSetRunningTotal += pitchReading;
              rollSetRunningTotal += rollReading;
              numberSetReadings--;
              if(numberSetReadings == 0) {
                yawSetPoint = yawSetRunningTotal / 100;
                pitchSetPoint = pitchSetRunningTotal / 100;
                rollSetPoint = rollSetRunningTotal / 100;
                gettingSetPoints = false;
                Serial.println("Done setting setPoints");
                Serial.print("ypr\t");
                Serial.print(yawSetPoint);
                Serial.print("\t");
                Serial.print(pitchSetPoint);
                Serial.print("\t");
                Serial.println(rollSetPoint);
                
              }
            }
            
        #endif
    
        // blink LED to indicate activity
        blinkState = !blinkState;
        digitalWrite(LED_PIN, blinkState);
    } 
}


void processReading(float yawReading, float pitchReading, float rollReading)
{
  
  // Check if reading is above threshold.  If so, report it.
  float yawDiff = yawSetPoint - yawReading;
  float pitchDiff = pitchSetPoint - pitchReading;
  float rollDiff = rollSetPoint - rollReading;
  
  float absYawReading = abs(yawReading);
  float absPitchReading = abs(pitchReading);
  float absRollReading = abs(rollReading);
  float absPrevYawReading = abs(prevYawReading);
  float absPrevPitchReading = abs(prevPitchReading);
  float absPrevRollReading = abs(prevRollReading);
  
   if(absPitchReading > (absPrevPitchReading + changeThreshold))
   {
            Serial.print("ypr\t");
            Serial.print(yawDiff);
            Serial.print("\t");
            Serial.print(pitchDiff);
            Serial.print("\t");
            Serial.println(rollDiff);

            if(readingsToReport <= 0) {

            float reportedYaw = yawDiffRunningTotal / 10;
            float reportedPitch = pitchDiffRunningTotal / 10;
            float reportedRoll = rollDiffRunningTotal / 10;
              
            Serial.print("Reporting");

            mpu.resetFIFO();
            dmpReady = false; // Multitasking leading to inconsistent results; 
            
            reportReadings(reportedYaw, reportedPitch, reportedRoll);
            
            dmpReady = true; // Start it back up again; 
            
            // Reset variables
            readingsToReport = 10;
            yawDiffRunningTotal = 0;
            pitchDiffRunningTotal = 0;
            rollDiffRunningTotal = 0;
           }
           else {
            readingsToReport--;
            yawDiffRunningTotal += yawDiff;
            pitchDiffRunningTotal += pitchDiff;
            rollDiffRunningTotal += rollDiff;
            
           }
   }

   


  // Assign new previous values
  prevYawReading = yawReading;
  prevPitchReading = pitchReading;
  prevRollReading = rollReading;
   
}

