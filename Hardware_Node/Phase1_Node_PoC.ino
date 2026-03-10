// AeroGrid Node - Phase 1 PoC
// Hardware: Uno + GP2Y10 dust sensor + MQ135 + MQ7 + BME280
// Grabbing raw sensor data for the Python ML script via serial

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// sensor pins matching the breadboard
#define mq7_pin A0
#define mq135_pin A1
#define measurePin A2      // dust sensor analog
#define ledPower 2         // dust sensor IR LED

Adafruit_BME280 bme; 

// GP2Y1010AU0F timing variables from datasheet
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPower, OUTPUT);
  
  Serial.println("Starting AeroGrid PoC...");
  
  // I2C address is usually 0x76 for these cheap BME modules
  if (!bme.begin(0x76)) { 
    Serial.println("bme280 error! check wiring");
    // while(1); // don't freeze here, just in case
  }
  
  delay(2000); // let the gas sensors warm up a bit
}

void loop() {
  // read temp & humidity
  float t = bme.readTemperature();
  float h = bme.readHumidity();

  // read gas levels
  int val_mq7 = analogRead(mq7_pin);
  int val_mq135 = analogRead(mq135_pin);

  // sharp dust sensor reading process
  digitalWrite(ledPower, LOW); // power on LED
  delayMicroseconds(samplingTime);
  
  voMeasured = analogRead(measurePin); // read dust
  
  delayMicroseconds(deltaTime);
  digitalWrite(ledPower, HIGH); // turn off
  delayMicroseconds(sleepTime);

  // calculate density math
  calcVoltage = voMeasured * (5.0 / 1024.0);
  dustDensity = 170 * calcVoltage - 0.1;
  
  if (dustDensity < 0) {
    dustDensity = 0; // prevent negative values from messing up the ML script
  }

  // dump everything to serial for the python pipeline
  // Serial.println(dustDensity); // debug line
  
  Serial.print("TEMP:"); Serial.print(t);
  Serial.print("|HUM:"); Serial.print(h);
  Serial.print("|MQ7:"); Serial.print(val_mq7);
  Serial.print("|MQ135:"); Serial.print(val_mq135);
  Serial.print("|PM:"); Serial.println(dustDensity);

  delay(2000); // send every 2 secs
}
