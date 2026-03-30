#include <SoftwareSerial.h>

SoftwareSerial BT(2, 3);

// Motor pins
int I1 = 8;
int I2 = 9;
int I3 = 10;
int I4 = 11;

// Ultrasonic pins
int trigPin = 6;
int echoPin = 7;

char receiving = 'S';

long duration;
int distance;

void setup()
{
  Serial.begin(9600);
  BT.begin(9600);

  pinMode(I1, OUTPUT);
  pinMode(I2, OUTPUT);
  pinMode(I3, OUTPUT);
  pinMode(I4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.println("Robot Ready");
}


// ===== MOTOR FUNCTIONS =====

void forward()
{
  digitalWrite(I1, HIGH);
  digitalWrite(I2, LOW);
  digitalWrite(I3, HIGH);
  digitalWrite(I4, LOW);
}

void reverse()
{
  digitalWrite(I1, LOW);
  digitalWrite(I2, HIGH);
  digitalWrite(I3, LOW);
  digitalWrite(I4, HIGH);
}

void left()
{
  digitalWrite(I1, LOW);
  digitalWrite(I2, LOW);
  digitalWrite(I3, HIGH);
  digitalWrite(I4, LOW);
}

void right()
{
  digitalWrite(I1, HIGH);
  digitalWrite(I2, LOW);
  digitalWrite(I3, LOW);
  digitalWrite(I4, LOW);
}

void stopMotors()
{
  digitalWrite(I1, LOW);
  digitalWrite(I2, LOW);
  digitalWrite(I3, LOW);
  digitalWrite(I4, LOW);
}


// ===== DISTANCE FUNCTION =====

int getDistance()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distance = duration * 0.034 / 2;

  return distance;
}


// ===== MAIN LOOP =====

void loop()
{
  int d = getDistance();

  Serial.print("Distance: ");
  Serial.println(d);

  if (BT.available())
  {
    receiving = BT.read();

    Serial.print("Received: ");
    Serial.println(receiving);
  }

  //  CONTROL LOGIC

  if (receiving == 'F')
  {
    if (d > 2 && d < 15)
    {
      Serial.println("Obstacle → STOP");
      stopMotors();
    }
    else
    {
      forward();
    }
  }

  else if (receiving == 'B')
  {
    reverse();   // ALWAYS allowed
  }

  else if (receiving == 'L')
  {
    left();      // ALWAYS allowed
  }

  else if (receiving == 'R')
  {
    right();     // ALWAYS allowed
  }

  else
  {
    stopMotors();
  }
}