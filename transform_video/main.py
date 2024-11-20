from static.utils import (read_video, 
                   save_video,
                   measure_distance,
                   convert_pixels_distance_to_meters,
                   draw_player_stats
                   )
from static.trackers import PlayerTracker, BallTracker
from static.court_line_detector import CourtLineDetector
from static.mini_court import MiniCourt
import cv2


def process_video(input_path):
    # Read Video
    input_video_path = input_path
    video_frames = read_video(input_video_path)

    # Detect and Track Players and Detect Ball
    player_tracker = PlayerTracker(model_path='yolov8x')
    ball_tracker = BallTracker(model_path='static/models/yolo5_last.pt')

    player_detections = player_tracker.detect_frames(video_frames,
                                                     read_from_stub=False,
                                                     stub_path="static/tracker_stubs/player_detections.pkl"
                                                     )
    ball_detections = ball_tracker.detect_frames(video_frames,
                                                     read_from_stub=False,
                                                     stub_path="static/tracker_stubs/ball_detections.pkl"
                                                     )
    ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)
    
    
    # Court Line Detector Model
    court_model_path = "static/models/keypoints_model-2.pth"
    court_line_detector = CourtLineDetector(court_model_path)
    court_keypoints = court_line_detector.predict(video_frames[0])

    # Choose and Filter Players
    player_detections = player_tracker.choose_and_filter_players(court_keypoints, player_detections)

    # Initialize MiniCourt
    mini_court = MiniCourt(video_frames[0])

    # Detect Ball Shots
    ball_shot_frames = ball_tracker.get_ball_shot_frames(ball_detections)




    # Draw output
    ## Draw Player and Ball Bounding Boxes
    output_video_frames = player_tracker.draw_bboxes(video_frames, player_detections)
    output_video_frames = ball_tracker.draw_bboxes(output_video_frames, ball_detections)

    ## Draw court keypoints
    output_video_frames = court_line_detector.draw_keypoints_on_video(output_video_frames, court_keypoints)

    ## Draw MiniCourt
    output_video_frames = mini_court.draw_mini_court(output_video_frames)

    ## Draw frame number on top left corner
    for i, frame in enumerate(output_video_frames):
        cv2.putText(frame, f"Frame: {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    print()
    save_video(output_video_frames, "static/outputs/output_video1.avi")