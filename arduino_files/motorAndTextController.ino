#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display


String FL = ""; // for incoming serial data
String FR = "";
String BL = "";
String BR = "";
String LCDText = "";

    void setup() {
      Serial.begin(9600); 
        lcd.init();                      // initialize the lcd 
        // Print a message to the LCD.
        lcd.backlight();
        lcd.setCursor(0,0);
        //scrollText("Sticking out your gyatt for the rizzler, you're so skibidi, you're so fanum tax, I just wanna be your sigma, freaking come here, give me your ohio");
    }

    void loop() {
      // send data only when you receive data:
      if (Serial.available() > 0) {
        // read the incoming byte:
        FL = Serial.readStringUntil(',');
        FR = Serial.readStringUntil(',');
        LCDText = Serial.readStringUntil('\n');

        if(LCDText != NULL){
          lcd.setCursor(0, 0);
          LCDText.trim();
          Serial.println(LCDText);
          Serial.println(LCDText.length());
          scrollText(LCDText);
          
        }

        controlMotor(10,9,8,FL.toInt());
        controlMotor(11,13,12,FR.toInt());
        controlMotor(3,2,1,BL.toInt());
        controlMotor(5,6,7,BR.toInt());

        Serial.println("FL: "+ FL +"   FR: " + FR + "   BL: "+BL+"   BR: "+BR);
      }
    }

    void controlMotor(int PWMPin, int MotorPin1, int MotorPin2, int Speed) {
    Speed = constrain(Speed, -255, 255);

    if (Speed > 0) {
        digitalWrite(MotorPin1, HIGH);
        digitalWrite(MotorPin2, LOW);
        analogWrite(PWMPin, Speed);
    } else if (Speed < 0) {
        // Reverse direction
        digitalWrite(MotorPin1, LOW);
        digitalWrite(MotorPin2, HIGH);
        analogWrite(PWMPin, -Speed);
    } else {
        // Stop the motor
        digitalWrite(MotorPin1, LOW);
        digitalWrite(MotorPin2, LOW);
        analogWrite(PWMPin, 0);
    }
}

void scrollText(String text) {
    String displayBuffer[4] = {"", "", "", ""};
    int row = 0, col = 0;
    lcd.clear();
    
    String word = "";
    for (int i = 0; i <= text.length(); i++) {
        char c = (i < text.length()) ? text[i] : ' '; 
        
        if (c == ' ' || i == text.length()) { 
            if (col + word.length() > 20) { 
                col = 0;
                row++;
            }
            if (row >= 4) { 
                for (int j = 0; j < 3; j++) {
                    displayBuffer[j] = displayBuffer[j + 1];
                }
                displayBuffer[3] = "";
                delay(250);
                lcd.clear();
                for (int j = 0; j < 4; j++) {
                    lcd.setCursor(0, j);
                    lcd.print(displayBuffer[j]);
                }
                row = 3;
                delay(250);
            }
            
            lcd.setCursor(col, row);
            lcd.print(word);
            displayBuffer[row] += word + " ";
            col += word.length() + 1;
            word = "";
            delay(80); 
        } else {
            word += c;
        }
    }
}
