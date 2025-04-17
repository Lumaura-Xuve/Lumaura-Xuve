from flask import Blueprint, request, jsonify, current_app
import logging
import json
import os
from xuvecode.models.project import db, Project, CodeFile, AICodeGeneration, CodeReview
from xuvecode.utils.ai_generation import generate_code

logger = logging.getLogger(__name__)
xuvecode_bp = Blueprint('xuvecode', __name__, url_prefix='/api/xuvecode')

@xuvecode_bp.route('/projects', methods=['GET'])
def get_projects():
    # In a real app, we would filter by the authenticated user
    # For demo purposes, we'll get all projects
    projects = Project.query.all()
    
    result = [{
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'programming_language': project.programming_language,
        'file_count': len(project.files),
        'created_at': project.created_at.isoformat(),
        'updated_at': project.updated_at.isoformat()
    } for project in projects]
    
    return jsonify(result)

@xuvecode_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    
    # Validate the data
    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400
    
    # In a real app, we would use the authenticated user
    # For demo purposes, we'll use a fixed user ID
    user_id = 1  # Demo user ID
    
    project = Project(
        name=data['name'],
        description=data.get('description', ''),
        user_id=user_id,
        programming_language=data.get('programming_language', 'python')
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'programming_language': project.programming_language,
        'created_at': project.created_at.isoformat()
    }), 201

@xuvecode_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    files = [{
        'id': file.id,
        'filename': file.filename,
        'path': file.path,
        'is_directory': file.is_directory,
        'updated_at': file.updated_at.isoformat()
    } for file in project.files]
    
    result = {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'programming_language': project.programming_language,
        'files': files,
        'created_at': project.created_at.isoformat(),
        'updated_at': project.updated_at.isoformat()
    }
    
    return jsonify(result)

@xuvecode_bp.route('/projects/<int:project_id>/files', methods=['POST'])
def create_file(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json
    
    # Validate the data
    if not data or not data.get('filename'):
        return jsonify({'error': 'Filename is required'}), 400
    
    file = CodeFile(
        project_id=project.id,
        filename=data['filename'],
        path=data.get('path', ''),
        content=data.get('content', ''),
        is_directory=data.get('is_directory', False)
    )
    
    db.session.add(file)
    db.session.commit()
    
    return jsonify({
        'id': file.id,
        'filename': file.filename,
        'path': file.path,
        'is_directory': file.is_directory,
        'created_at': file.created_at.isoformat()
    }), 201

@xuvecode_bp.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    file = CodeFile.query.get_or_404(file_id)
    
    result = {
        'id': file.id,
        'project_id': file.project_id,
        'filename': file.filename,
        'path': file.path,
        'content': file.content,
        'is_directory': file.is_directory,
        'created_at': file.created_at.isoformat(),
        'updated_at': file.updated_at.isoformat()
    }
    
    return jsonify(result)

@xuvecode_bp.route('/files/<int:file_id>', methods=['PUT'])
def update_file(file_id):
    file = CodeFile.query.get_or_404(file_id)
    data = request.json
    
    if 'content' in data:
        file.content = data['content']
    
    if 'filename' in data:
        file.filename = data['filename']
    
    if 'path' in data:
        file.path = data['path']
    
    db.session.commit()
    
    return jsonify({
        'id': file.id,
        'filename': file.filename,
        'path': file.path,
        'updated_at': file.updated_at.isoformat()
    })

@xuvecode_bp.route('/generate', methods=['POST'])
def generate_code_api():
    data = request.json
    
    # Validate the data
    if not data or not data.get('prompt'):
        return jsonify({'error': 'Prompt is required'}), 400
    
    if not data.get('project_id'):
        return jsonify({'error': 'Project ID is required'}), 400
    
    project = Project.query.get_or_404(data['project_id'])
    
    # Create a record of the code generation request
    generation = AICodeGeneration(
        project_id=project.id,
        prompt=data['prompt'],
        language=data.get('language', project.programming_language),
        model_used=data.get('model', 'gpt-4'),
        parameters=data.get('parameters', {})
    )
    
    db.session.add(generation)
    db.session.commit()
    
    # Generate the code (in a real app, this would be a background task)
    try:
        generated_code = generate_code(
            prompt=data['prompt'],
            language=generation.language,
            model=generation.model_used,
            parameters=generation.parameters
        )
        
        generation.generated_code = generated_code
        generation.status = 'completed'
        db.session.commit()
        
        return jsonify({
            'id': generation.id,
            'generated_code': generated_code,
            'status': 'completed'
        })
    
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        generation.status = 'failed'
        db.session.commit()
        
        return jsonify({
            'error': f"Failed to generate code: {str(e)}",
            'status': 'failed'
        }), 500
