//Include the library files
#include <LiquidCrystal.h>
#include <Wire.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

#define sensor 34
#define relay 22

//Initialize the LCD display
LiquidCrystal lcd(2, 4, 5, 18, 19, 21);

BlynkTimer timer;

// Enter your Auth token
char auth[] = "************************";

//Enter your WIFI SSID and password
char ssid[] = "***************";
char pass[] = "************";

void setup() {
  // Debug console
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
  lcd.begin(16, 2);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);

  lcd.setCursor(1, 0);
  lcd.print("System Loading");
  for (int a = 0; a <= 15; a++) {
    lcd.setCursor(a, 1);
    lcd.print(".");
    delay(200);
  }
  lcd.clear();
}

//Get the ultrasonic sensor values
void soilMoisture() {
  int value = analogRead(sensor);
  value = map(value, 0, 4095, 0, 100);
  value = (value - 100) * -1;
  Blynk.virtualWrite(V0, value);
  Serial.println(value);
  lcd.setCursor(0, 0);
  lcd.print("Moisture :");
  lcd.print(value);
  lcd.print(" ");
}

//Get the button value
BLYNK_WRITE(V1) {
  bool Relay = param.asInt();
  if (Relay == 1) {
    digitalWrite(relay, LOW);
    lcd.setCursor(0, 1);
    lcd.print("Motor is ON ");
  } else {
    digitalWrite(relay, HIGH);
    lcd.setCursor(0, 1);
    lcd.print("Motor is OFF");
  }
}

void loop() {
  soilMoisture();
  Blynk.();//Run the Blynk library
  //delay(200);

}