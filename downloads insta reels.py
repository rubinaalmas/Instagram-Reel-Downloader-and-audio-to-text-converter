import instaloader
import pytesseract
import cv2
import pandas as pd
import os

# function to authenticate and fetch reel details
def fetch_reel_details(reel_url, username, session_file):
    """
    Fetch caption and comments from an Instagram reel.
    """
    L = instaloader.Instaloader()
    L.load_session_from_file(username, session_file)
    shortcode = reel_url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    # fetch caption
    caption = post.caption if post.caption else "No caption available."

    #  comments and usernames
    comments_and_usernames = []
    for comment in post.get_comments():
        # debugging: Print attributes to ensure correct access
        if hasattr(comment.owner, "username"):
            comments_and_usernames.append((comment.owner.username, comment.text))
        else:
            comments_and_usernames.append(("Anonymous", comment.text))

    return caption, comments_and_usernames

# download the reel video
def download_reel_video(reel_url, username, session_file, download_dir="reel_videos"):
    """
    Download the reel video from Instagram.
    """
    L = instaloader.Instaloader()
    L.load_session_from_file(username, session_file)
    shortcode = reel_url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    os.makedirs(download_dir, exist_ok=True)
    video_path = os.path.join(download_dir, f"{shortcode}.mp4")
    L.download_post(post, download_dir)
    return video_path

#extract OCR text from video
def extract_ocr_text_from_video(video_path, frame_interval=30):
    """
    Extract OCR text from video frames.
    """
    cap = cv2.VideoCapture(video_path)
    extracted_text = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray_frame, config="--oem 3 --psm 6")
            extracted_text.append(text.strip())

        frame_count += 1

    cap.release()
    return " ".join(extracted_text)

# function to combine data and save to CSV
def generate_csv_from_reel(reel_url, username, session_file, output_csv="reel_data.csv"):
    """
    Generate a CSV file containing caption, comments, usernames, and OCR text.
    """
    print("Fetching reel details...")
    caption, comments_and_usernames = fetch_reel_details(reel_url, username, session_file)

    print("Downloading reel video...")
    video_path = download_reel_video(reel_url, username, session_file)

    print("Extracting OCR text from the video...")
    ocr_text = extract_ocr_text_from_video(video_path)

    # combine data
    data = []
    for user, comment in comments_and_usernames:
        data.append({
            "username": user,
            "comment": comment,
            "caption": caption,
            "ocr_text": ocr_text
        })

    # save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    reel_url = "reel_url"
    username = "username_"
    session_file = "/Users/rubinaalmas/.config/instaloader/session-dmprojectgroup24"  # correct session file path
    output_csv = "reel_data.csv"

    generate_csv_from_reel(reel_url, username, session_file, output_csv)
