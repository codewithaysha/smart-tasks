from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app import mongo
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/', methods=['GET'])
@login_required
def list_tasks():
    tasks = list(mongo.db.tasks.find({'user_id': ObjectId(current_user.get_id())}))
    return render_template('tasks/list.html', tasks=tasks)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task = {
            'user_id': ObjectId(current_user.get_id()),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'status': 'pending',
            'priority': request.form.get('priority', 'medium'),
            'due_date': request.form.get('due_date'),
            'created_at': datetime.now()
        }
        mongo.db.tasks.insert_one(task)
        flash('Task created successfully', 'success')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('tasks/create.html')

@bp.route('/<task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id), 'user_id': ObjectId(current_user.get_id())})
    
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('tasks.list_tasks'))
    
    if request.method == 'POST':
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {
            '$set': {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'priority': request.form.get('priority'),
                'due_date': request.form.get('due_date')
            }
        })
        flash('Task updated successfully', 'success')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('tasks/edit.html', task=task)

@bp.route('/<task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id), 'user_id': ObjectId(current_user.get_id())})
    flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks.list_tasks'))

@bp.route('/<task_id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id), 'user_id': ObjectId(current_user.get_id())})
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    new_status = 'completed' if task['status'] == 'pending' else 'pending'
    mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'status': new_status}})
    
    return jsonify({'status': new_status})
