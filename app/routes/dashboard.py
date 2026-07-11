from flask import Blueprint, render_template
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app import mongo

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    user_id = ObjectId(current_user.get_id())
    
    # Get task statistics
    total_tasks = mongo.db.tasks.count_documents({'user_id': user_id})
    completed_tasks = mongo.db.tasks.count_documents({'user_id': user_id, 'status': 'completed'})
    pending_tasks = total_tasks - completed_tasks
    
    # Get upcoming tasks
    upcoming_tasks = list(mongo.db.tasks.find({'user_id': user_id, 'status': 'pending'}).limit(5))
    
    # Get recent notes
    recent_notes = list(mongo.db.notes.find({'user_id': user_id}).sort('created_at', -1).limit(5))
    
    stats = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks
    }
    
    return render_template('dashboard.html', stats=stats, upcoming_tasks=upcoming_tasks, recent_notes=recent_notes)
