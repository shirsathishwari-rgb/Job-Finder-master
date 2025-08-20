import re
from collections import Counter
import json

class SkillsAnalyzer:
    def __init__(self):
        self.skill_categories = {
            "Programming Languages": [
                "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin"
            ],
            "Web Technologies": [
                "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "FastAPI"
            ],
            "Databases": [
                "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite"
            ],
            "Cloud & DevOps": [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab"
            ],
            "Data Science": [
                "Machine Learning", "Deep Learning", "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn"
            ],
            "Design Tools": [
                "Figma", "Adobe Photoshop", "Adobe Illustrator", "Sketch", "InVision"
            ],
            "Business Tools": [
                "Excel", "Tableau", "Power BI", "JIRA", "Confluence", "Slack", "Trello"
            ],
            "Methodologies": [
                "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "REST API", "GraphQL"
            ]
        }
        
        self.skill_demand_levels = {
            "High Demand": [
                "Python", "JavaScript", "React", "AWS", "Docker", "Machine Learning", 
                "SQL", "Git", "Node.js", "Django", "Flask"
            ],
            "Medium Demand": [
                "Java", "C++", "Angular", "Vue.js", "MongoDB", "Azure", "Kubernetes",
                "TensorFlow", "PyTorch", "Figma", "Tableau"
            ],
            "Emerging": [
                "Rust", "Go", "FastAPI", "GraphQL", "Blockchain", "IoT", "Cybersecurity"
            ]
        }

    def analyze_skills(self, skills):
        """Analyze the extracted skills and provide insights"""
        if not skills:
            return {
                'total_skills': 0,
                'categories': {},
                'demand_analysis': {},
                'recommendations': [],
                'skill_gaps': [],
                'market_trends': {}
            }
        
        analysis = {
            'total_skills': len(skills),
            'categories': self._categorize_skills(skills),
            'demand_analysis': self._analyze_demand(skills),
            'recommendations': self._generate_recommendations(skills),
            'skill_gaps': self._identify_skill_gaps(skills),
            'market_trends': self._get_market_trends(skills)
        }
        
        return analysis

    def _categorize_skills(self, skills):
        """Categorize skills into different areas"""
        categories = {}
        
        for skill in skills:
            for category, category_skills in self.skill_categories.items():
                if skill in category_skills:
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(skill)
                    break
        
        # Add uncategorized skills
        categorized_skills = set()
        for category_skills in categories.values():
            categorized_skills.update(category_skills)
        
        uncategorized = [skill for skill in skills if skill not in categorized_skills]
        if uncategorized:
            categories['Other'] = uncategorized
        
        return categories

    def _analyze_demand(self, skills):
        """Analyze the demand level of skills"""
        demand_counts = {
            'High Demand': 0,
            'Medium Demand': 0,
            'Emerging': 0,
            'Standard': 0
        }
        
        for skill in skills:
            found = False
            for demand_level, demand_skills in self.skill_demand_levels.items():
                if skill in demand_skills:
                    demand_counts[demand_level] += 1
                    found = True
                    break
            
            if not found:
                demand_counts['Standard'] += 1
        
        return demand_counts

    def _generate_recommendations(self, skills):
        """Generate skill development recommendations"""
        recommendations = []
        
        # Check for missing high-demand skills
        high_demand_skills = set(self.skill_demand_levels['High Demand'])
        user_skills = set(skills)
        missing_high_demand = high_demand_skills - user_skills
        
        if missing_high_demand:
            recommendations.append({
                'type': 'High Demand Skills',
                'skills': list(missing_high_demand)[:3],  # Top 3
                'priority': 'High',
                'reason': 'These skills are in high demand and can significantly boost your career prospects.'
            })
        
        # Check for emerging technologies
        emerging_skills = set(self.skill_demand_levels['Emerging'])
        missing_emerging = emerging_skills - user_skills
        
        if missing_emerging:
            recommendations.append({
                'type': 'Emerging Technologies',
                'skills': list(missing_emerging)[:2],  # Top 2
                'priority': 'Medium',
                'reason': 'These emerging technologies can give you a competitive edge in the future.'
            })
        
        # Check for complementary skills
        complementary_recommendations = self._get_complementary_skills(skills)
        if complementary_recommendations:
            recommendations.extend(complementary_recommendations)
        
        return recommendations

    def _get_complementary_skills(self, skills):
        """Get complementary skills based on existing skills"""
        complementary = []
        
        # Programming language complements
        if 'Python' in skills and 'Machine Learning' not in skills:
            complementary.append({
                'type': 'Data Science',
                'skills': ['Machine Learning', 'Pandas', 'NumPy'],
                'priority': 'Medium',
                'reason': 'Python is excellent for data science and machine learning.'
            })
        
        if 'JavaScript' in skills and 'React' not in skills:
            complementary.append({
                'type': 'Frontend Development',
                'skills': ['React', 'Node.js'],
                'priority': 'Medium',
                'reason': 'JavaScript skills can be extended to modern frontend frameworks.'
            })
        
        if 'SQL' in skills and 'Python' in skills and 'Data Analysis' not in skills:
            complementary.append({
                'type': 'Data Analysis',
                'skills': ['Data Analysis', 'Tableau', 'Power BI'],
                'priority': 'Medium',
                'reason': 'Combine SQL and Python for comprehensive data analysis capabilities.'
            })
        
        return complementary

    def _identify_skill_gaps(self, skills):
        """Identify potential skill gaps"""
        gaps = []
        
        # Check for full-stack development gaps
        has_frontend = any(skill in skills for skill in ['HTML', 'CSS', 'JavaScript', 'React', 'Angular'])
        has_backend = any(skill in skills for skill in ['Python', 'Java', 'Node.js', 'PHP', 'Ruby'])
        
        if has_frontend and not has_backend:
            gaps.append({
                'area': 'Backend Development',
                'missing': ['Python', 'Node.js', 'SQL'],
                'impact': 'Limits ability to build complete applications'
            })
        elif has_backend and not has_frontend:
            gaps.append({
                'area': 'Frontend Development',
                'missing': ['HTML', 'CSS', 'JavaScript'],
                'impact': 'Limits ability to create user interfaces'
            })
        
        # Check for DevOps gaps
        has_devops = any(skill in skills for skill in ['Docker', 'AWS', 'Git', 'Jenkins'])
        if not has_devops:
            gaps.append({
                'area': 'DevOps',
                'missing': ['Git', 'Docker', 'AWS'],
                'impact': 'Important for modern software development practices'
            })
        
        return gaps

    def _get_market_trends(self, skills):
        """Get market trends related to the skills"""
        trends = {
            'hot_skills': [],
            'growing_demand': [],
            'stable_skills': [],
            'declining_skills': []
        }
        
        # Identify hot skills (high demand + emerging)
        hot_skills = set(self.skill_demand_levels['High Demand']) & set(self.skill_demand_levels['Emerging'])
        trends['hot_skills'] = [skill for skill in skills if skill in hot_skills]
        
        # Identify growing demand skills
        growing_skills = ['Machine Learning', 'Docker', 'Kubernetes', 'React', 'Python']
        trends['growing_demand'] = [skill for skill in skills if skill in growing_skills]
        
        # Identify stable skills
        stable_skills = ['SQL', 'JavaScript', 'Java', 'Git']
        trends['stable_skills'] = [skill for skill in skills if skill in stable_skills]
        
        return trends

    def get_skill_score(self, skills):
        """Calculate an overall skill score"""
        if not skills:
            return 0
        
        score = 0
        total_possible = 0
        
        for skill in skills:
            # Base score for having the skill
            score += 10
            
            # Bonus for high demand skills
            if skill in self.skill_demand_levels['High Demand']:
                score += 20
            elif skill in self.skill_demand_levels['Medium Demand']:
                score += 15
            elif skill in self.skill_demand_levels['Emerging']:
                score += 25
            
            total_possible += 35  # Max possible per skill
        
        return min(100, (score / total_possible) * 100) if total_possible > 0 else 0

    def get_skill_breakdown(self, skills):
        """Get detailed breakdown of skills"""
        breakdown = {
            'technical_skills': [],
            'soft_skills': [],
            'tools': [],
            'languages': []
        }
        
        # This is a simplified breakdown - in a real application, you'd have more sophisticated categorization
        for skill in skills:
            if skill in ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust']:
                breakdown['languages'].append(skill)
            elif skill in ['Git', 'Docker', 'AWS', 'JIRA', 'Figma', 'Tableau']:
                breakdown['tools'].append(skill)
            elif skill in ['Agile', 'Scrum', 'Leadership', 'Communication']:
                breakdown['soft_skills'].append(skill)
            else:
                breakdown['technical_skills'].append(skill)
        
        return breakdown
