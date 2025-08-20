import json
from collections import defaultdict

class JobMatcher:
    def __init__(self):
        self.job_database = {
            "Software Development": {
                "Frontend Developer": {
                    "required_skills": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js"],
                    "preferred_skills": ["TypeScript", "Sass", "Bootstrap", "Tailwind", "Webpack"],
                    "experience_level": "2-5 years",
                    "salary_range": "$60,000 - $120,000",
                    "description": "Build responsive and interactive user interfaces using modern web technologies."
                },
                "Backend Developer": {
                    "required_skills": ["Python", "Java", "Node.js", "SQL", "REST API"],
                    "preferred_skills": ["Django", "Flask", "Spring Boot", "Express.js", "MongoDB"],
                    "experience_level": "3-7 years",
                    "salary_range": "$70,000 - $140,000",
                    "description": "Develop server-side logic and APIs for web applications."
                },
                "Full Stack Developer": {
                    "required_skills": ["HTML", "CSS", "JavaScript", "Python", "SQL", "REST API"],
                    "preferred_skills": ["React", "Node.js", "Django", "Flask", "MongoDB"],
                    "experience_level": "3-8 years",
                    "salary_range": "$80,000 - $150,000",
                    "description": "Handle both frontend and backend development for complete web applications."
                },
                "Mobile Developer": {
                    "required_skills": ["JavaScript", "React Native", "Flutter", "Android", "iOS"],
                    "preferred_skills": ["Java", "Swift", "Kotlin", "Objective-C", "Firebase"],
                    "experience_level": "2-6 years",
                    "salary_range": "$65,000 - $130,000",
                    "description": "Develop mobile applications for iOS and Android platforms."
                },
                "DevOps Engineer": {
                    "required_skills": ["Docker", "Kubernetes", "AWS", "Git", "Jenkins"],
                    "preferred_skills": ["Azure", "Google Cloud", "Terraform", "Ansible", "Linux"],
                    "experience_level": "3-8 years",
                    "salary_range": "$80,000 - $160,000",
                    "description": "Manage infrastructure, deployment, and operational processes."
                }
            },
            "Data & Analytics": {
                "Data Scientist": {
                    "required_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL"],
                    "preferred_skills": ["TensorFlow", "PyTorch", "Scikit-learn", "Tableau", "Power BI"],
                    "experience_level": "3-7 years",
                    "salary_range": "$90,000 - $160,000",
                    "description": "Analyze complex data sets and build predictive models."
                },
                "Data Analyst": {
                    "required_skills": ["SQL", "Excel", "Data Analysis", "Tableau", "Power BI"],
                    "preferred_skills": ["Python", "Pandas", "R", "Google Analytics", "A/B Testing"],
                    "experience_level": "1-5 years",
                    "salary_range": "$50,000 - $100,000",
                    "description": "Collect, analyze, and visualize data to drive business decisions."
                },
                "Business Analyst": {
                    "required_skills": ["Excel", "SQL", "Data Analysis", "Agile", "JIRA"],
                    "preferred_skills": ["Tableau", "Power BI", "Python", "R", "Business Intelligence"],
                    "experience_level": "2-6 years",
                    "salary_range": "$60,000 - $110,000",
                    "description": "Bridge the gap between business needs and technical solutions."
                },
                "Machine Learning Engineer": {
                    "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
                    "preferred_skills": ["Scikit-learn", "AWS", "Docker", "Kubernetes", "MLOps"],
                    "experience_level": "3-8 years",
                    "salary_range": "$100,000 - $180,000",
                    "description": "Build and deploy machine learning models at scale."
                }
            },
            "Design & Creative": {
                "UI/UX Designer": {
                    "required_skills": ["Figma", "Adobe Photoshop", "Adobe Illustrator", "User Research", "Prototyping"],
                    "preferred_skills": ["Sketch", "InVision", "Framer", "Design Systems", "Accessibility"],
                    "experience_level": "2-6 years",
                    "salary_range": "$60,000 - $120,000",
                    "description": "Create intuitive and engaging user experiences through design."
                },
                "Graphic Designer": {
                    "required_skills": ["Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", "Typography", "Color Theory"],
                    "preferred_skills": ["Figma", "Sketch", "Canva", "Brand Identity", "Print Design"],
                    "experience_level": "1-5 years",
                    "salary_range": "$40,000 - $80,000",
                    "description": "Create visual content for various media and platforms."
                },
                "Product Designer": {
                    "required_skills": ["Figma", "User Research", "Prototyping", "Design Systems", "User Testing"],
                    "preferred_skills": ["Adobe Creative Suite", "Sketch", "InVision", "Design Thinking", "Agile"],
                    "experience_level": "3-7 years",
                    "salary_range": "$70,000 - $140,000",
                    "description": "Design products that solve user problems and meet business goals."
                }
            },
            "Management": {
                "Project Manager": {
                    "required_skills": ["Agile", "Scrum", "JIRA", "Project Planning", "Risk Management"],
                    "preferred_skills": ["PMP", "Prince2", "Microsoft Project", "Stakeholder Management", "Budgeting"],
                    "experience_level": "5-10 years",
                    "salary_range": "$80,000 - $150,000",
                    "description": "Lead project teams and ensure successful delivery of projects."
                },
                "Product Manager": {
                    "required_skills": ["Product Strategy", "User Research", "Agile", "Data Analysis", "Stakeholder Management"],
                    "preferred_skills": ["A/B Testing", "SQL", "Tableau", "Roadmapping", "Go-to-Market Strategy"],
                    "experience_level": "4-8 years",
                    "salary_range": "$90,000 - $160,000",
                    "description": "Define product vision and lead product development teams."
                },
                "Engineering Manager": {
                    "required_skills": ["Technical Leadership", "Team Management", "Agile", "Code Review", "Architecture"],
                    "preferred_skills": ["Python", "Java", "JavaScript", "System Design", "Mentoring"],
                    "experience_level": "6-12 years",
                    "salary_range": "$120,000 - $200,000",
                    "description": "Lead engineering teams and drive technical excellence."
                }
            }
        }

    def find_matching_jobs(self, skills, min_match_percentage=30):
        """Find jobs that match the given skills"""
        matches = []
        
        for category, jobs in self.job_database.items():
            for job_title, job_info in jobs.items():
                match_score = self._calculate_match_score(skills, job_info)
                
                if match_score >= min_match_percentage:
                    matches.append({
                        'title': job_title,
                        'category': category,
                        'match_score': match_score,
                        'required_skills': job_info['required_skills'],
                        'preferred_skills': job_info['preferred_skills'],
                        'experience_level': job_info['experience_level'],
                        'salary_range': job_info['salary_range'],
                        'description': job_info['description'],
                        'matched_skills': self._get_matched_skills(skills, job_info),
                        'missing_skills': self._get_missing_skills(skills, job_info)
                    })
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches

    def _calculate_match_score(self, user_skills, job_info):
        """Calculate match percentage between user skills and job requirements"""
        required_skills = set(skill.lower() for skill in job_info['required_skills'])
        preferred_skills = set(skill.lower() for skill in job_info['preferred_skills'])
        user_skills_lower = set(skill.lower() for skill in user_skills)
        
        # Calculate matches
        required_matches = len(required_skills.intersection(user_skills_lower))
        preferred_matches = len(preferred_skills.intersection(user_skills_lower))
        
        # Weight required skills more heavily
        total_required = len(required_skills)
        total_preferred = len(preferred_skills)
        
        if total_required == 0:
            return 0
        
        # Calculate weighted score
        required_score = (required_matches / total_required) * 70  # 70% weight
        preferred_score = (preferred_matches / total_preferred) * 30 if total_preferred > 0 else 0  # 30% weight
        
        return min(100, required_score + preferred_score)

    def _get_matched_skills(self, user_skills, job_info):
        """Get skills that match between user and job"""
        required_skills = set(skill.lower() for skill in job_info['required_skills'])
        preferred_skills = set(skill.lower() for skill in job_info['preferred_skills'])
        user_skills_lower = set(skill.lower() for skill in user_skills)
        
        matched_required = required_skills.intersection(user_skills_lower)
        matched_preferred = preferred_skills.intersection(user_skills_lower)
        
        return {
            'required': list(matched_required),
            'preferred': list(matched_preferred)
        }

    def _get_missing_skills(self, user_skills, job_info):
        """Get skills that the user is missing for the job"""
        required_skills = set(skill.lower() for skill in job_info['required_skills'])
        preferred_skills = set(skill.lower() for skill in job_info['preferred_skills'])
        user_skills_lower = set(skill.lower() for skill in user_skills)
        
        missing_required = required_skills - user_skills_lower
        missing_preferred = preferred_skills - user_skills_lower
        
        return {
            'required': list(missing_required),
            'preferred': list(missing_preferred)
        }

    def get_job_recommendations(self, skills, limit=5):
        """Get top job recommendations based on skills"""
        matches = self.find_matching_jobs(skills)
        return matches[:limit]

    def get_skill_gaps(self, skills, target_job):
        """Get skill gaps for a specific job"""
        for category, jobs in self.job_database.items():
            if target_job in jobs:
                job_info = jobs[target_job]
                return self._get_missing_skills(skills, job_info)
        return None

    def get_all_jobs(self):
        """Get all available jobs"""
        all_jobs = []
        for category, jobs in self.job_database.items():
            for job_title, job_info in jobs.items():
                all_jobs.append({
                    'title': job_title,
                    'category': category,
                    'description': job_info['description'],
                    'experience_level': job_info['experience_level'],
                    'salary_range': job_info['salary_range']
                })
        return all_jobs
