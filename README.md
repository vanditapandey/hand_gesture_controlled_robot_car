# Gesture Controlled Robot 

## Overview

This project is a simple robot controlled using hand gestures through a webcam.
The gestures are detected using Python (OpenCV + MediaPipe) and sent wirelessly via an HC-05 Bluetooth module to an Arduino, which controls the motors.

---

## How It Works

* Webcam captures your hand
* Program detects gesture
* Gesture is converted into a command (F, L, R, S)
* Command is sent via Bluetooth
* Arduino receives it and moves the robot

---

## Files

* `gesture_control_1.py` → Gesture detection and Bluetooth communication
* `gesture_control.ino` → Arduino motor control code
* Screenshot → arduino connections using TinkerCad
* Video → Demo of working system

---

## Requirements

### Software

* Python
* OpenCV
* MediaPipe
* PySerial

### Hardware

* Arduino
* HC-05 Bluetooth module
* Motor driver
* DC motors
* Robot chassis
* Laptop with webcam

---

## Setup

1. Install required Python libraries
2. Pair HC-05 with your laptop
3. Upload Arduino code
4. Set correct COM port in Python file
5. Run the Python script

---

## Notes

* Works best in good lighting
* Make sure baud rate matches (usually 9600)
* Check correct COM port before running

---

