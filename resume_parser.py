import os
import re
from pdfminer.high_level import extract_text
from docx import Document
import PyPDF2
import io

class ResumeParser:
    def __init__(self):
        self.skills_database = {
            # Programming Languages
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
            'javascript': ['javascript', 'js', 'node.js', 'express.js', 'react', 'angular', 'vue.js', 'jquery'],
            'java': ['java', 'spring', 'spring boot', 'hibernate', 'maven', 'gradle'],
            'c++': ['c++', 'cpp', 'stl', 'boost'],
            'c#': ['c#', 'asp.net', '.net', 'entity framework'],
            'php': ['php', 'laravel', 'symfony', 'wordpress'],
            'ruby': ['ruby', 'rails', 'sinatra'],
            'go': ['go', 'golang'],
            'rust': ['rust'],
            
            # Web Technologies
            'html': ['html', 'html5', 'xhtml'],
            'css': ['css', 'css3', 'sass', 'scss', 'less', 'bootstrap', 'tailwind'],
            'sql': ['sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'mongodb', 'redis'],
            
            # Cloud & DevOps
            'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda', 'rds'],
            'azure': ['azure', 'microsoft azure'],
            'gcp': ['gcp', 'google cloud', 'google cloud platform'],
            'docker': ['docker', 'containerization'],
            'kubernetes': ['kubernetes', 'k8s'],
            'jenkins': ['jenkins', 'ci/cd'],
            'git': ['git', 'github', 'gitlab', 'bitbucket'],
            
            # Tools & Platforms
            'jira': ['jira', 'atlassian'],
            'confluence': ['confluence'],
            'slack': ['slack'],
            'trello': ['trello'],
            'figma': ['figma'],
            'photoshop': ['photoshop', 'adobe photoshop'],
            'illustrator': ['illustrator', 'adobe illustrator'],
            
            # Data Science & Analytics
            'machine learning': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
            'deep learning': ['deep learning', 'neural networks'],
            'data analysis': ['data analysis', 'data analytics'],
            'tableau': ['tableau'],
            'power bi': ['power bi', 'powerbi'],
            'excel': ['excel', 'microsoft excel'],
            
            # Methodologies
            'agile': ['agile', 'scrum', 'kanban', 'sprint'],
            'devops': ['devops'],
            'microservices': ['microservices'],
            'rest api': ['rest', 'rest api', 'api'],
            'graphql': ['graphql'],
            
            # Security
            'cybersecurity': ['cybersecurity', 'security', 'penetration testing', 'ethical hacking'],
            'blockchain': ['blockchain', 'ethereum', 'bitcoin'],
            
            # Other
            'iot': ['iot', 'internet of things'],
            'mobile development': ['android', 'ios', 'react native', 'flutter', 'xamarin']
        }
        
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'university', 'college', 'school',
            'bsc', 'msc', 'mba', 'phd', 'diploma', 'certificate', 'certification'
        ]
        
        self.experience_keywords = [
            'experience', 'work', 'employment', 'job', 'position', 'role',
            'years', 'months', 'senior', 'junior', 'lead', 'manager'
        ]

    def parse(self, file_path):
        """Parse resume file and extract information"""
        try:
            # Extract text based on file type
            text = self._extract_text(file_path)
            
            # Clean and normalize text
            text = self._clean_text(text)
            
            # Extract information
            skills = self._extract_skills(text)
            education = self._extract_education(text)
            experience = self._extract_experience(text)
            contact = self._extract_contact(text)
            
            return {
                'skills': skills,
                'education': education,
                'experience': experience,
                'contact': contact,
                'raw_text': text,
                'file_path': file_path
            }
            
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")

    def _extract_text(self, file_path):
        """Extract text from different file formats"""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            return self._extract_from_docx(file_path)
        elif file_extension == 'txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _extract_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            # Try pdfminer first
            text = extract_text(file_path)
            if text.strip():
                return text
            
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
                
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def _extract_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    def _extract_from_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()

    def _clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.@\+]', ' ', text)
        
        return text.strip()

    def _extract_skills(self, text):
        """Extract skills from text"""
        found_skills = []
        
        for skill_category, skill_variants in self.skills_database.items():
            for variant in skill_variants:
                if variant in text:
                    found_skills.append(skill_category.title())
                    break  # Avoid duplicates
        
        return list(set(found_skills))  # Remove duplicates

    def _extract_education(self, text):
        """Extract education information"""
        education_info = []
        
        # Look for education-related patterns
        education_patterns = [
            r'(bachelor|master|phd|bsc|msc|mba)\s+.*?(?:in|of)\s+([^,\n]+)',
            r'(university|college|school)\s+of\s+([^,\n]+)',
            r'([^,\n]+)\s+university',
            r'([^,\n]+)\s+college'
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                education_info.append(match.group(0))
        
        return list(set(education_info))

    def _extract_experience(self, text):
        """Extract experience information"""
        experience_info = []
        
        # Look for experience-related patterns
        experience_patterns = [
            r'(\d+)\s+(?:years?|yrs?)\s+(?:of\s+)?experience',
            r'(senior|junior|lead|manager|director)\s+([^,\n]+)',
            r'(\d+)\s+(?:months?|mos?)\s+(?:of\s+)?experience'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                experience_info.append(match.group(0))
        
        return list(set(experience_info))

    def _extract_contact(self, text):
        """Extract contact information"""
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Phone
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
        
        return contact_info
