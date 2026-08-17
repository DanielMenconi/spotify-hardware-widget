#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

String inputLine = "";

void setup() {
  Serial.begin(9600);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true) {}
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  display.setCursor(0, 0);
  display.println("Spotify Widget");
  display.display();
}

void loop() {

  while (Serial.available() > 0) {

    char c = Serial.read();

    if (c == '\n') {
      processLine(inputLine);
      inputLine = "";
    }
    else {
      inputLine += c;
    }
  }
}

void processLine(String line) {

  int first = line.indexOf('|');
  int second = line.indexOf('|', first + 1);

  if (first == -1 || second == -1) {
    return;
  }

  String canzone = line.substring(0, first);
  String artista = line.substring(first + 1, second);
  String conteggio = line.substring(second + 1);

  showTrack(canzone, artista, conteggio);
}

void showTrack(String canzone, String artista, String conteggio) {

  display.clearDisplay();

  display.setCursor(0, 0);
  display.println("Now Playing");

  display.setCursor(0, 16);
  display.println(canzone);

  display.setCursor(0, 32);
  display.println(artista);

  display.setCursor(0, 48);
  display.print("N:");
  display.println(conteggio);

  display.display();
}