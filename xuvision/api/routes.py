from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from xuvision.models.video import db, Video, Transcription, TranscriptionSegment, User
from xuvision.utils.transcription import transcribe_video, process_transcription
import logging

logger = logging.getLogger(__name__)
xuvision_bp = Blueprint('xuvision', __name__, url_prefix='/api/xuvision')

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@xuvision_bp.route('/videos', methods=['GET'])
def get_videos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    videos = Video.query.filter_by(is_public=True).order_by(Video.created_at.desc()).paginate(page=page, per_page=per_page)
    
    result = {
        'videos': [{
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'thumbnail_path': video.thumbnail_path,
            'duration': video.duration,
            'owner': video.owner.username,
            'created_at': video.created_at.isoformat()
        } for video in videos.items],
        'total': videos.total,
        'pages': videos.pages,
        'current_page': page
    }
    
    return jsonify(result)

@xuvision_bp.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    
    if not video.is_public:
        return jsonify({'error': 'This video is private'}), 403
    
    result = {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'file_path': video.file_path,
        'thumbnail_path': video.thumbnail_path,
        'duration': video.duration,
        'owner': video.owner.username,
        'created_at': video.created_at.isoformat(),
        'has_transcription': video.transcription is not None and video.transcription.is_processed
    }
    
    return jsonify(result)

@xuvision_bp.route('/videos/<int:video_id>/transcription', methods=['GET'])
def get_transcription(video_id):
    video = Video.query.get_or_404(video_id)
    
    if not video.is_public:
        return jsonify({'error': 'This video is private'}), 403
    
    if not video.transcription or not video.transcription.is_processed:
        return jsonify({'error': 'Transcription not available'}), 404
    
    segments = [
        {
            'start_time': segment.start_time,
            'end_time': segment.end_time,
            'text': segment.text,
            'speaker': segment.speaker,
            'confidence': segment.confidence
        }
        for segment in video.transcription.segments
    ]
    
    result = {
        'video_id': video.id,
        'language': video.transcription.language,
        'content': video.transcription.content,
        'segments': segments,
        'created_at': video.transcription.created_at.isoformat(),
        'updated_at': video.transcription.updated_at.isoformat()
    }
    
    return jsonify(result)

@xuvision_bp.route('/upload', methods=['POST'])
def upload_video():
    # This endpoint would require authentication in a real app
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # In a real app, we would check the user's quota, file size, etc.
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Create a video record in the database
    # For this example, we'll use a dummy user (in a real app, we'd use the authenticated user)
    user = User.query.first()  # Dummy user
    
    video = Video(
        title=request.form.get('title', 'Untitled'),
        description=request.form.get('description', ''),
        file_path=file_path,
        user_id=user.id if user else 1  # Dummy user ID
    )
    
    db.session.add(video)
    db.session.commit()
    
    # Start transcription process in background (would use Celery or similar in a real app)
    # This is just a placeholder for the real implementation
    try:
        transcribe_video(video.id)
    except Exception as e:
        logger.error(f"Error starting transcription: {str(e)}")
    
    return jsonify({
        'id': video.id,
        'title': video.title,
        'file_path': video.file_path,
        'message': 'Video uploaded successfully. Transcription is being processed.'
    }), 201
