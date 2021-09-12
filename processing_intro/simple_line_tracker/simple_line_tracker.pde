

int screenHeight = 768;
int screenWidth = 8160;

int vertexLineLength = 15;

boolean topLeft = true;
int topLeftX = 0;
int topLeftY = 0;
int bottomRightX = 0;
int bottomRightY = 0;

boolean drawRect = false;
boolean waitUserInput = false;

int screenCount = 0;

// Objects to store screen coordinates
JSONArray screenArray = null;
JSONObject screenCoords = null;

void settings() {
  smooth();
}

void setup() {
  surface.setSize(screenWidth, screenHeight);
  surface.setLocation(1024, 0);
  
  // Create JSON array to hold coordinates for each screen
  screenArray = new JSONArray();
  println("Welcome to the Projector Alignment System!\nStarting from the far left screen and moving right, please click on the top left corner of the projector screen, followed by the bottom right corner.");
  println("At the end of alignment, the numbers should read in ascending order from left to right across the screens");
  println("When you are done plotting the projector coordinates, press [s] to save your work to the screen_coords.json file");
  println("\nPlease start by clicking the top left corner of Screen " + screenCount);
}


void draw() {
  background(255);
  strokeWeight(5.0);
  strokeJoin(MITER);
  if (!waitUserInput) {
  if (topLeft) {
      // Top left corner icon
      noFill();
      stroke(255, 0, 0);
      beginShape();
      vertex(mouseX, mouseY - vertexLineLength);
      vertex(mouseX, mouseY);
      vertex(mouseX + vertexLineLength, mouseY);
      endShape();
    } else {
      // Bottom right corner icon
      noFill();
      stroke(255, 0, 0);
      strokeWeight(10.0);
      beginShape();  
      vertex(mouseX - vertexLineLength, mouseY);
      vertex(mouseX, mouseY);
      vertex(mouseX, mouseY + vertexLineLength);
      endShape();
      fill(0, 0, 255);
      stroke(0,0,0);
      strokeWeight(0.0);
      rect(topLeftX, topLeftY, mouseX - topLeftX, mouseY - topLeftY);
    }
  }
  
  // Drawing the rectangles on the screen after they've been created
  for (int i = 0; i < screenArray.size(); i++){
    JSONObject currScreenCoords = screenArray.getJSONObject(i);
    int currTopLeftX = currScreenCoords.getInt("top_left_x");
    int currTopLeftY = currScreenCoords.getInt("top_left_y");
    int currBottomRightX = currScreenCoords.getInt("bottom_right_x");
    int currBottomRightY = currScreenCoords.getInt("bottom_right_y");
    
    // Drawing the final rectangle layout on the screens
    fill(0, 0, 255);
    strokeWeight(0.0);
    rect(currTopLeftX, currTopLeftY, currBottomRightX - currTopLeftX, currBottomRightY - currTopLeftY);
    
    // Number Label for the screens
    fill(0, 0, 0);
    textAlign(CENTER, CENTER);
    textSize(((currBottomRightX - currTopLeftX) / 2));
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
      
      println("Press the bottom right corner of Screen " + screenCount);
      topLeft = false;
    }
    else {
      // Store clicked position as bottom right coordinate
      bottomRightX = mouseX;
      bottomRightY = mouseY;
      
      screenCoords.setInt("bottom_right_x", bottomRightX);
      screenCoords.setInt("bottom_right_y", bottomRightY);
      // Append screen coordinates to array of all screens
      screenArray.append(screenCoords);
      // Reset coordinates for next screen
      screenCoords = null;
      
      screenCount++;
          
      topLeft = true;
      
      println("\nWould you like to proceed to tracing the next screen? [y/n]\nRemember, if you are done plotting, press [s] \n(If not, you will be prompted to redraw the most recent rectangle. You cannot make edits to this rectangle after this point).\n");
      waitUserInput = true;
  
    }
  } else {
    println("Press [y/n] to indicate if you would like to continue to the next screen or redraw the current screen mapping");
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
    println("\nPress the top left corner of Screen " + screenCount);

  } else if (key == 'y') {
    waitUserInput = false;
    println("\nPress the top left corner of Screen " + screenCount);
  } else if (key == 's') {
    saveJSONArray(screenArray, "screen_coords.json");
    exit();
  }
    
}


//void keyPressed() {
//  saveJSONArray(screenArray, "screen_coords.json");
//  exit();
//}
