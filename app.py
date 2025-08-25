from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Data file to store tasks
DATA_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/')
def index():
    """Display all tasks"""
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    task_text = request.form.get('task', '').strip()
    
    if task_text:
        tasks = load_tasks()
        
        # Generate new ID
        new_id = max([task.get('id', 0) for task in tasks], default=0) + 1
        
        new_task = {
            'id': new_id,
            'text': task_text,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        tasks.append(new_task)
        save_tasks(tasks)
    
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Toggle task completion status"""
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """Edit a task"""
    new_text = request.form.get('task', '').strip()
    
    if new_text:
        tasks = load_tasks()
        
        for task in tasks:
            if task['id'] == task_id:
                task['text'] = new_text
                break
        
        save_tasks(tasks)
    
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    """API endpoint to get all tasks"""
    return jsonify(load_tasks())

if __name__ == '__main__':
    app.run(debug=True)