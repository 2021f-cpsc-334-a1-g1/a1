
int screenHeight = 768;
int screenWidth = 8160;

color red = color(255, 0, 0);
color orange = color(255, 127, 0);
color yellow = color(255, 255, 0);
color green = color(0, 255, 0);
color blue = color(0, 0, 255);
color indigo = color(46, 43, 95);
color violet = color(139, 0, 255);

color [] rainbow = {red, orange, yellow, green, blue, indigo, violet};
int colorCount = 7;

int vertexLineLength = 100;

boolean topLeft = true;
int topLeftX = 0;
int topLeftY = 0;
int bottomRightX = 0;
int bottomRightY = 0;

boolean drawRect = false;
boolean waitUserInput = false;

int screenCount = 0;

// Objects to store display coordinates
JSONArray screenArray = null;
JSONObject screenCoords = null;

void setup() {
  fullScreen(0);
  println(height);
  
  // Create JSON array to hold coordinates for each display
  screenArray = new JSONArray();
  println("Welcome to the Display Alignment System!\nStarting from the far left display and moving right, please click on the top left corner of the display, followed by the bottom right corner.");
  println("At the end of alignment, the numbers should read in ascending order from left to right across the screens");
  println("When you are done plotting the display coordinates, press [s] to save your work to the display_config.json file");
  println("\nPlease start by clicking the top left corner of Display " + screenCount);
}


void draw() { //<>//
  background(255);
  strokeWeight(20.0);
  strokeJoin(MITER);
  if (!waitUserInput) {
    if (topLeft) {
      // Top left corner icon
      noFill();
      stroke(0, 0, 0);
      beginShape();
      vertex(mouseX, mouseY - vertexLineLength);
      vertex(mouseX, mouseY);
      vertex(mouseX + vertexLineLength, mouseY);
      endShape();
    } else {
      // Bottom right corner icon
      noFill();
      stroke(0, 0, 0);
      strokeWeight(40.0);
      beginShape();  
      vertex(mouseX - vertexLineLength, mouseY);
      vertex(mouseX, mouseY);
      vertex(mouseX, mouseY + vertexLineLength);
      endShape();
      fill(rainbow[screenCount % colorCount]);
      stroke(0,0,0);
      strokeWeight(0.0);
      rect(topLeftX, topLeftY, mouseX - topLeftX, mouseY - topLeftY);
    }
  }
  
  // Drawing the rectangles on the display after they've been created
  for (int i = 0; i < screenArray.size(); i++){
    JSONObject currScreenCoords = screenArray.getJSONObject(i);
    int currTopLeftX = currScreenCoords.getInt("top_left_x");
    int currTopLeftY = currScreenCoords.getInt("top_left_y");
    int currBottomRightX = currScreenCoords.getInt("bottom_right_x");
    int currBottomRightY = currScreenCoords.getInt("bottom_right_y");
    
    // Drawing the final rectangle layout on the displays
    fill(rainbow[i % colorCount]);
    strokeWeight(0.0);
    rect(currTopLeftX, currTopLeftY, currBottomRightX - currTopLeftX, currBottomRightY - currTopLeftY);
    
    // Number Label for the displays
    fill(0, 0, 0);
    textAlign(CENTER, CENTER);
    textSize(abs((currBottomRightX - currTopLeftX) / 2));
    pushMatrix();
    translate(currTopLeftX + ((currBottomRightX - currTopLeftX) / 2.5), currTopLeftY + ((currBottomRightY - currTopLeftY)) / 2);
    rotate(radians(-90));
    text(i, 0, 0);
    popMatrix();
  }
  

}

void mousePressed() {
  if (!waitUserInput) {
    if (screenCoords == null) {
      // Create a new JSON object to store coordinates
      screenCoords = new JSONObject();
      // Store clicked position as top left coordinate
      topLeftX = mouseX;
      topLeftY = mouseY;
      
      screenCoords.setInt("top_left_x", topLeftX);
      screenCoords.setInt("top_left_y", topLeftY);
      
      println("Press the bottom right corner of Display " + screenCount);
      topLeft = false;
    }
    else {
      // Store clicked position as bottom right coordinate
      bottomRightX = mouseX;
      bottomRightY = mouseY;
      
      screenCoords.setInt("bottom_right_x", bottomRightX);
      screenCoords.setInt("bottom_right_y", bottomRightY);
      // Append displays coordinates to array of all displays
      screenArray.append(screenCoords);
      // Reset coordinates for next display
      screenCoords = null;
      
      screenCount++;
          
      topLeft = true;
      
      println("\nWould you like to proceed to tracing the next displays? [y/n]\nRemember, if you are done plotting, press [s] \n(If not, you will be prompted to redraw the most recent rectangle. You cannot make edits to this rectangle after this point).\n");
      waitUserInput = true;
  
    }
  } else {
    println("Press [y/n] to indicate if you would like to continue to the next display or redraw the current display mapping");
  }
}

void mouseReleased() {
    if (topLeft) {
      drawRect = true;
    }
}

void keyTyped() {
  if (key == 'n') {
    screenCount--;
    screenArray.remove(screenCount);
    waitUserInput = false;
    println("\nPress the top left corner of Display " + screenCount);

  } else if (key == 'y') {
    waitUserInput = false;
    println("\nPress the top left corner of Display " + screenCount);
  } else if (key == 's') {
    saveJSONArray(screenArray, "./reports/display_config.json");
    exit();
  }
    
}
