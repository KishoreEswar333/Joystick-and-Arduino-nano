// Pin definitions
const int xAxisPin = A0; // Analog pin for X-axis
const int yAxisPin = A1; // Analog pin for Y-axis
const int buttonPin = 8; // Digital pin for joystick button

// Variables to store joystick readings
int xAxisValue = 0;
int yAxisValue = 0;
int previousButtonState = LOW; // Initial previous button state
int toggleState = LOW; // Toggle state for the button

void setup() {
  // Initialize Serial communication
  Serial.begin(9600);
  
  // Set button pin as input
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // Read analog values from X and Y axis
  xAxisValue = analogRead(xAxisPin);
  yAxisValue = analogRead(yAxisPin);

  // Read button state
  int buttonState = digitalRead(buttonPin);

  // Map analog values to a range of 0 to 1023 for both X and Y axes
  int mappedX = map(xAxisValue, 0, 1023, 0, 100);
  int mappedY = map(yAxisValue, 0, 1023, 0, 100);

  // Print mapped values to Serial Monitor
  Serial.print(mappedX);
  Serial.print(",");
  Serial.println(toggleState);

  // Check if button state has changed from LOW to HIGH (pressed)
  if (buttonState == HIGH && previousButtonState == LOW) {
    // Toggle the toggleState
    toggleState = !toggleState;
  }

  // Update previousButtonState
  previousButtonState = buttonState;

  // Add a short delay
  delay(100);
}
