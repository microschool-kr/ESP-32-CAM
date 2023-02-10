#include <Servo.h>
#include <SoftwareSerial.h>
#define buzzer 2
#define servo_init 0
Servo myservo;
long time = millis();
SoftwareSerial mySerial(2,3);


void setup()
{   
    Serial.begin(9600);
    myservo.attach(3);
    pinMode(buzzer, OUTPUT);    
    myservo.write(servo_init);

}

void loop()
{   
    if (Serial.available() != 0) {
        char read = Serial.read();
        Serial.println(read);
        //Serial.println(time);
            if (read == '0'){
                myservo.write(servo_init); 
                noTone(buzzer);
                }
            else if (read == '1' or read == '2') {
                myservo.write(90);
                if (read == '1') {
                  noTone(buzzer);
                }
                  time = millis();
                    while(read == '2'){
                      if (Serial.available() != 0){
                         read = Serial.read(); 
                      }
                      Serial.println(read);
                      Serial.println("wake up!");
                      if (time + 1000 < millis()){
                          tone(buzzer, 261, 1000);
                      }
                      if (time + 2000 < millis()){
                          time = millis();
                          tone(buzzer, 392, 1000);
                      }
                    }
            }        
    }
    delay(100);
}
