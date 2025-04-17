from flask import Flask, render_template, request
from collections import defaultdict

app = Flask(__name__)

# Organized Job Role Database with Required Skills and Career Advice
job_roles = [
    {
        "name": "Software Developer",
        "skills": {"Python", "Java", "C++", "JavaScript", "HTML", "CSS"},
        "advice": "Focus on learning more advanced programming languages and frameworks."
    },
    {
        "name": "Java Developer",
        "skills": {"Java", "Spring", "Hibernate", "SQL", "JavaScript"},
        "advice": "Master the Java ecosystem and build a strong understanding of OOP principles."
    },
    {
        "name": "Full Stack Developer",
        "skills": {"HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB", "SQL"},
        "advice": "Master both frontend and backend technologies to build full-stack applications."
    },
    {
        "name": "Web Developer",
        "skills": {"HTML", "CSS", "JavaScript", "React", "Node.js", "Express"},
        "advice": "Keep improving on frontend technologies and start exploring backend development."
    },
    {
        "name": "Mobile App Developer",
        "skills": {"Java", "Kotlin", "Swift", "React Native", "Android", "iOS"},
        "advice": "Develop apps for both Android and iOS platforms and keep up with mobile design patterns."
    },
    {
        "name": "DevOps Engineer",
        "skills": {"Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Terraform"},
        "advice": "Strengthen your skills in cloud platforms and automation tools for seamless integration and delivery."
    },
    {
        "name": "Cloud Engineer",
        "skills": {"AWS", "Azure", "Google Cloud", "Terraform", "Docker", "Kubernetes"},
        "advice": "Learn about cloud architecture and how to manage scalable cloud infrastructure."
    },
    {
        "name": "Data Scientist",
        "skills": {"Python", "R", "Machine Learning", "Statistics", "SQL", "Data Visualization"},
        "advice": "Enhance your knowledge in data manipulation, algorithms, and machine learning models."
    },
    {
        "name": "Machine Learning Engineer",
        "skills": {"Python", "TensorFlow", "Keras", "Scikit-Learn", "Data Preprocessing", "Model Deployment"},
        "advice": "Master data science principles and learn how to scale machine learning models."
    },
    {
        "name": "Data Analyst",
        "skills": {"Excel", "SQL", "Python", "Data Visualization", "Statistics"},
        "advice": "Refine your ability to analyze large datasets and communicate insights effectively."
    },
    {
        "name": "Database Administrator",
        "skills": {"SQL", "MySQL", "PostgreSQL", "Database Optimization", "Data Backup", "Replication"},
        "advice": "Focus on database design, performance tuning, and understanding scalability for large data."
    },
    {
        "name": "Network Engineer",
        "skills": {"TCP/IP", "DNS", "HTTP", "Routing", "Switching", "Cisco", "Linux"},
        "advice": "Focus on gaining deep knowledge of network protocols and network security."
    },
    {
        "name": "Cybersecurity Analyst",
        "skills": {"Penetration Testing", "Firewalls", "Encryption", "Network Security", "Vulnerability Management"},
        "advice": "Stay updated with the latest security threats and best practices."
    },
    {
        "name": "Systems Administrator",
        "skills": {"Linux", "Windows Server", "Networking", "Cloud Computing", "Virtualization", "Scripting"},
        "advice": "Strengthen your expertise in server management and automation scripting."
    },
    {
        "name": "Product Manager",
        "skills": {"Agile", "Scrum", "Product Roadmaps", "User Stories", "Stakeholder Management"},
        "advice": "Focus on developing strong communication and leadership skills for effective product management."
    },
    {
        "name": "UX/UI Designer",
        "skills": {"Adobe XD", "Figma", "Wireframing", "Prototyping", "User Research", "Usability Testing"},
        "advice": "Keep honing your design skills and focus on user-centered design principles."
    },
    {
        "name": "Game Developer",
        "skills": {"C++", "Unity", "Unreal Engine", "Game Design", "3D Modeling", "Game Physics"},
        "advice": "Explore game engines and focus on game mechanics and interactive design."
    },
    {
        "name": "SEO Specialist",
        "skills": {"SEO", "Google Analytics", "Keyword Research", "Link Building", "Content Optimization"},
        "advice": "Stay updated with search engine algorithms and optimize content for better rankings."
    },
    {
        "name": "Salesforce Developer",
        "skills": {"Salesforce", "Apex", "Visualforce", "Lightning", "SOQL"},
        "advice": "Specialize in Salesforce's ecosystem and become proficient in customizing and deploying solutions."
    },
    {
        "name": "Quality Assurance Engineer",
        "skills": {"Automation Testing", "Selenium", "Jenkins", "Bug Tracking", "Test Plans"},
        "advice": "Learn automated testing tools and focus on the quality of software deliverables."
    },
    {
    "name": "Python Web Developer",
    "skills": {"Python", "Django", "Flask", "HTML", "CSS", "JavaScript", "SQL"},
    "advice": "Master Python-based frameworks like Django and Flask to build scalable web apps."
    }

]

skill_categories = {
    "Languages": {"Python", "Java", "C++", "R", "Kotlin", "Swift"},
    "Web Technologies": {"HTML", "CSS", "JavaScript", "React", "Node.js", "Express"},
    "Web Frameworks": {"Django", "Flask", "Spring", "Hibernate"},
    "Cloud & DevOps": {"AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "CI/CD", "Terraform"},
    "Databases": {"SQL", "MySQL", "PostgreSQL", "MongoDB", "Database Optimization", "Data Backup", "Replication"},
    "Data & AI": {"Machine Learning", "Statistics", "Data Visualization", "TensorFlow", "Keras", "Scikit-Learn", "Data Preprocessing", "Model Deployment"},
    "Mobile & Game Development": {"Android", "iOS", "React Native", "Unity", "Unreal Engine", "Game Design", "3D Modeling", "Game Physics"},
    "Cybersecurity & Networking": {"Penetration Testing", "Firewalls", "Encryption", "Network Security", "Vulnerability Management", "TCP/IP", "DNS", "HTTP", "Routing", "Switching", "Cisco"},
    "UI/UX & Tools": {"Adobe XD", "Figma", "Wireframing", "Prototyping", "User Research", "Usability Testing"},
    "Testing & Automation": {"Automation Testing", "Selenium", "Jenkins", "Bug Tracking", "Test Plans"},
    "Others": {"Excel", "Agile", "Scrum", "Product Roadmaps", "User Stories", "Stakeholder Management", "Spring", "Hibernate", "Linux", "Windows Server", "Networking", "Cloud Computing", "Virtualization", "Scripting", "Salesforce", "Apex", "Visualforce", "Lightning", "SEO", "Google Analytics", "Keyword Research", "Link Building", "Content Optimization"}
}


@app.route('/')
def index():
    
    all_skills = set()
    for job in job_roles:
        all_skills.update(job["skills"])

    
    categorized_skills = defaultdict(list)
    for category, keywords in skill_categories.items():
        for skill in sorted(all_skills):
            if skill in keywords:
                categorized_skills[category].append(skill)

    return render_template('index.html', skills=dict(categorized_skills))

@app.route('/result', methods=['POST'])
def result():
    selected_skills = set(request.form.getlist('skills'))

    best_match = None
    max_score = 0

    for job in job_roles:
        score = len(job["skills"].intersection(selected_skills))
        if score > max_score:
            max_score = score
            best_match = job

    if best_match and max_score > 0:
        role = best_match['name']
        advice = best_match['advice']
        matched_skills = best_match['skills'].intersection(selected_skills)
        reason = f"Matched {max_score} skill(s): {', '.join(sorted(matched_skills))}"
    else:
        role = "Unknown"
        advice = "Please explore more skills or consult with a career advisor."
        reason = "The skills selected were insufficient for a clear match."

    return render_template('result.html', role=role, advice=advice, reason=reason)

if __name__ == '__main__':
    app.run(debug=True)