from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app import mongo
from datetime import datetime

bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('/', methods=['GET'])
@login_required
def list_notes():
    notes = list(mongo.db.notes.find({'user_id': ObjectId(current_user.get_id())}))
    return render_template('notes/list.html', notes=notes)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        note = {
            'user_id': ObjectId(current_user.get_id()),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'tags': request.form.get('tags', '').split(','),
            'category': request.form.get('category'),
            'created_at': datetime.now()
        }
        mongo.db.notes.insert_one(note)
        flash('Note created successfully', 'success')
        return redirect(url_for('notes.list_notes'))
    
    return render_template('notes/create.html')

@bp.route('/<note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id), 'user_id': ObjectId(current_user.get_id())})
    
    if not note:
        flash('Note not found', 'error')
        return redirect(url_for('notes.list_notes'))
    
    if request.method == 'POST':
        mongo.db.notes.update_one({'_id': ObjectId(note_id)}, {
            '$set': {
                'title': request.form.get('title'),
                'content': request.form.get('content'),
                'tags': request.form.get('tags', '').split(','),
                'category': request.form.get('category')
            }
        })
        flash('Note updated successfully', 'success')
        return redirect(url_for('notes.list_notes'))
    
    return render_template('notes/edit.html', note=note)

@bp.route('/<note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    mongo.db.notes.delete_one({'_id': ObjectId(note_id), 'user_id': ObjectId(current_user.get_id())})
    flash('Note deleted successfully', 'success')
    return redirect(url_for('notes.list_notes'))
