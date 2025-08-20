from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from skills_analyzer import SkillsAnalyzer

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, DOC, or TXT files.'}), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        # Parse resume
        parser = ResumeParser()
        resume_data = parser.parse(filepath)
        
        # Analyze skills
        analyzer = SkillsAnalyzer()
        skills_analysis = analyzer.analyze_skills(resume_data['skills'])
        
        # Find matching jobs
        matcher = JobMatcher()
        job_matches = matcher.find_matching_jobs(resume_data['skills'])
        
        # Store results in session
        session['resume_data'] = {
            'filename': file.filename,
            'upload_time': datetime.now().isoformat(),
            'resume_data': resume_data,
            'skills_analysis': skills_analysis,
            'job_matches': job_matches
        }
        
        return jsonify({
            'success': True,
            'message': 'Resume analyzed successfully!',
            'data': {
                'resume_data': resume_data,
                'skills_analysis': skills_analysis,
                'job_matches': job_matches
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route("/results")
def results():
    if 'resume_data' not in session:
        return redirect(url_for('home'))
    
    return render_template('results.html', data=session['resume_data'])

@app.route("/api/skills")
def get_skills():
    """API endpoint to get all available skills"""
    skills = [
        "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust",
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
        "Django", "Flask", "FastAPI", "Spring Boot", "Laravel", "ASP.NET",
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
        "Git", "GitHub", "GitLab", "JIRA", "Confluence", "Slack", "Trello",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Tableau", "Power BI",
        "Excel", "PowerPoint", "Word", "Photoshop", "Illustrator", "Figma",
        "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "REST API", "GraphQL",
        "Microservices", "Serverless", "Blockchain", "IoT", "Cybersecurity"
    ]
    return jsonify(skills)

@app.route("/api/jobs")
def get_jobs():
    """API endpoint to get job categories"""
    jobs = {
        "Software Development": [
            "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Mobile Developer", "DevOps Engineer", "Software Architect"
        ],
        "Data & Analytics": [
            "Data Scientist", "Data Analyst", "Business Analyst",
            "Machine Learning Engineer", "Data Engineer", "BI Developer"
        ],
        "Design & Creative": [
            "UI/UX Designer", "Graphic Designer", "Product Designer",
            "Web Designer", "Creative Director", "Art Director"
        ],
        "Management": [
            "Project Manager", "Product Manager", "Engineering Manager",
            "Scrum Master", "Technical Lead", "Team Lead"
        ]
    }
    return jsonify(jobs)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
