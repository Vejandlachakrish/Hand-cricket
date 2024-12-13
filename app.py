import cv2
import numpy as np
import random


# Function to detect the number of fingers raised
def count_fingers(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return 0

    cnt = max(contours, key=lambda x: cv2.contourArea(x))
    hull_indices = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull_indices)

    if defects is None:
        return 0

    finger_count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = np.linalg.norm(np.array(start) - np.array(end))
        b = np.linalg.norm(np.array(start) - np.array(far))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c)) * 57
        if angle <= 90:
            finger_count += 1

    return min(finger_count + 1, 6)


def hand_cricket():
    cap = cv2.VideoCapture(0)
    user_score = 0
    computer_score = 0
    is_user_out = False

    print("You will bowl first!")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 100:400]
        cv2.putText(frame, 'Press "c" to bowl!', (
            10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            user_choice = count_fingers(roi)
            computer_choice = random.randint(1, 6)
            cv2.putText(frame, f'Your Bowl: {user_choice}', (10, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Computer Batted: {computer_choice}', 
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if user_choice == computer_choice:
                is_user_out = True
                break
            if computer_choice != 0:
                computer_score += computer_choice

        cv2.putText(frame, f'Computer Score: {computer_score}', (10, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow('Hand Cricket', frame)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Game Over! Computer Score: {computer_score}")
    if is_user_out:
        print("The computer is out!")
    else:
        print("You ended the game voluntarily.")

    print("\nNow it's your turn to bat!")
    cap = cv2.VideoCapture(0)
    is_computer_out = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 100:400]
        cv2.putText(frame, 'Press "c" to bat!', (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            player_choice = count_fingers(roi)
            computer_choice = random.randint(1, 6)
            cv2.putText(frame, f'Your Bat: {player_choice}', (10, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Computer Bowled: {computer_choice}', 
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if player_choice == computer_choice:
                is_computer_out = True
                break
            if player_choice != 0:
                user_score += player_choice

        cv2.putText(frame, f'Your Score: {user_score}', (10, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow('Hand Cricket', frame)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Game Over! Your Score: {user_score}")
    if is_computer_out:
        print("You are out!")
    else:
        print("You ended cthe game voluntarily.")

    print("\nFinal Scores:")
    print(f"User Score: {user_score}")
    print(f"Computer Score: {computer_score}")
    
    if user_score > computer_score:
        print("Congratulations! You win!")
    elif user_score < computer_score:
        print("The computer wins! Better luck next time.")
    else:
        print("It's a tie!")


if __name__ == '__main__':
    hand_cricket()
