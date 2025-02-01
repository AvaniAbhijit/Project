#Task for student
#Task 1: Slower Ball Speed – Reduce the ball speed to make it easier.
#Task 2: Increase Paddle Size – Make the paddle wider for better control.

import cv2
import numpy as np
import mediapipe as mp
import random

def main():
    # Initialize webcam and window
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
    # Initialize hand detection
    hands = mp.solutions.hands.Hands(max_num_hands=1)
    
    # Game variables
    score = 0
    lives = 3
    ball_x = random.randint(0, 800)
    ball_y = 0
    paddle_x = 350  # paddle start position
    game_over = False
    
    while True:
        # Get camera frame and resize it
        _, frame = cap.read()
        frame = cv2.resize(frame, (800, 600))
        frame = cv2.flip(frame, 1)
        
        # Create game frame (black background) 
        game = np.zeros((600, 800, 3), dtype=np.uint8)
        
        if not game_over:
            # Process hand landmarks if hand is detected
            hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if hand_results.multi_hand_landmarks:
                # Update paddle position based on index finger
                x = int(hand_results.multi_hand_landmarks[0].landmark[8].x * 800)
                paddle_x = np.clip(x - 50, 0, 700)  # 50 is half paddle width
                
                # Draw hand landmarks and connections on camera frame
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, 
                    hand_results.multi_hand_landmarks[0],
                    mp.solutions.hands.HAND_CONNECTIONS
                )
            
            # Update ball position
            ball_y += 5
            
            # Check collision
            if ball_y >= 550 and paddle_x <= ball_x <= paddle_x + 100:
                score += 1
                ball_y = 0
                ball_x = random.randint(0, 800)
            elif ball_y >= 600:
                lives -= 1
                ball_y = 0
                ball_x = random.randint(0, 800)
            
            # Check for game over
            if lives <= 0:
                game_over = True
        
        # Draw game elements
        cv2.rectangle(game, (paddle_x, 550), (paddle_x + 100, 570), (0, 255, 0), -1)  # paddle
        cv2.circle(game, (ball_x, ball_y), 10, (0, 0, 255), -1)  # ball
        cv2.putText(game, f'Score: {score} Lives: {lives}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        if game_over:
            cv2.putText(game, 'Game Over! Press R to restart', (200, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show both windows side by side
        combined = np.hstack((frame, game))
        cv2.imshow('Hand Controlled Game', combined)
        
        # Check for quit or restart
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        elif (key == ord('r') or key == ord('R')) and game_over:
            score = 0
            lives = 3
            ball_y = 0
            ball_x = random.randint(0, 800)
            game_over = False
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()
