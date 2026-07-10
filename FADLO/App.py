import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fadlo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ------------------------------------------------------------------
# Project Data (for examples page)
# ------------------------------------------------------------------
PROJECTS = [
    {
        'id': 1,
        'title': 'SBT ACADEMY',
        'description': 'Multi‑role school management platform with real‑time progress tracking for students, teachers, and parents.',
        'icon': 'fa-graduation-cap',
        'gradient': 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)',
        'link': 'https://sbtacaedemy.pythonanywhere.com/',
        'tags': ['Python', 'Flask', 'JavaScript'],
        'service': 'web'
    },
    {
        'id': 2,
        'title': 'IMPACTO ⚡',
        'description': 'Modern platform for entrepreneurs with multi‑language support and team dashboard.',
        'icon': 'fa-bolt',
        'gradient': 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
        'link': 'https://impacto.pythonanywhere.com/login',
        'tags': ['Python', 'Flask', 'JavaScript'],
        'service': 'web'
    },
    {
        'id': 3,
        'title': 'Fashion Store UI Kit',
        'description': 'Complete mobile‑first UI design for an online fashion store – Figma prototypes and React components.',
        'icon': 'fa-shopping-cart',
        'gradient': 'linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%)',
        'link': '#',
        'tags': ['Figma', 'React', 'Styled‑Components'],
        'service': 'ui'
    },
    {
        'id': 4,
        'title': 'Analytics Pro Dashboard',
        'description': 'Interactive marketing dashboard with real‑time data visualisation, campaign tracking, and ROI analysis.',
        'icon': 'fa-chart-pie',
        'gradient': 'linear-gradient(135deg, #3b82f6 0%, #6366f1 100%)',
        'link': '#',
        'tags': ['Python', 'Plotly', 'Dash'],
        'service': 'marketing'
    },
    {
        'id': 5,
        'title': 'Personal Portfolio 2026',
        'description': 'Minimalist, glass‑morphism portfolio design with smooth animations and full responsiveness.',
        'icon': 'fa-user-tie',
        'gradient': 'linear-gradient(135deg, #0ea5e9 0%, #22d3ee 100%)',
        'link': '#',
        'tags': ['Figma', 'HTML/CSS', 'JavaScript'],
        'service': 'ui'
    },
    {
        'id': 6,
        'title': 'LearnPro Platform',
        'description': 'Full‑stack e‑learning platform with video streaming, quizzes, and progress tracking for students.',
        'icon': 'fa-video',
        'gradient': 'linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%)',
        'link': '#',
        'tags': ['Python', 'Flask', 'JavaScript', 'SQLite'],
        'service': 'web'
    },
    {
        'id': 7,
        'title': 'FADLO Platform',
        'description': 'A modern personal platform built with Flask, featuring glass‑morphism design, multi‑language support, team management, and real‑time messaging.',
        'icon': 'fa-crown',
        'gradient': 'linear-gradient(135deg, #0ea5e9 0%, #22d3ee 100%)',
        'link': '/',
        'tags': ['Flask', 'Python', 'JavaScript', 'Bootstrap'],
        'service': 'web'
    }
]

# ------------------------------------------------------------------
# Translations (Arabic default, English, French)
# ------------------------------------------------------------------
translations = {
    'ar': {
        # Navigation & general
        'home': 'الرئيسية',
        'portfolio': 'أعمالي',
        'services': 'خدماتي',
        'examples': 'نماذج',
        'about': 'عني',
        'welcome': 'مرحباً بك في منصة فدلو',
        'intro': 'منصتي الشخصية لعرض أعمالي وخدماتي',
        'footer_text': 'جميع الحقوق محفوظة © 2026 فدلو',
        'language': 'اللغة',
        'dashboard': 'لوحة التحكم',
        'team': 'الفريق',
        'messages': 'الرسائل',
        'tasks': 'المهام',
        'clients': 'العملاء',
        'profile': 'الملف الشخصي',
        'login': 'تسجيل الدخول',
        'logout': 'تسجيل الخروج',
        'username': 'اسم المستخدم',
        'password': 'كلمة المرور',
        'login_title': 'مرحباً بعودتك',
        'login_subtitle': 'سجل الدخول لاستكشاف منصة فدلو',
        'login_button': 'دخول',
        'welcome_user': 'مرحباً، {username}',
        'invalid_credentials': 'اسم المستخدم أو كلمة المرور غير صحيحة',
        'stats_projects': 'مشاريع',
        'stats_clients': 'عملاء',
        'stats_experience': 'سنوات الخبرة',
        'dashboard_title': 'لوحة التحكم',
        'dashboard_desc': 'لوحة تحكم منصة فدلو',
        'add_member': 'إضافة عضو',
        'member_name': 'الاسم',
        'member_role': 'الدور',
        'send_message': 'إرسال رسالة',
        'message_content': 'محتوى الرسالة',
        'no_members': 'لا يوجد أعضاء حتى الآن',
        'no_messages': 'لا توجد رسائل',
        'delete': 'حذف',
        'total_members': 'إجمالي الأعضاء',
        'total_messages': 'إجمالي الرسائل',
        'total_projects': 'إجمالي المشاريع',
        'total_clients': 'إجمالي العملاء',
        'member_added': 'تمت إضافة العضو بنجاح',
        'member_deleted': 'تم حذف العضو',
        'message_sent': 'تم إرسال الرسالة',
        'edit_profile': 'تعديل الملف',
        'full_name': 'الاسم الكامل',
        'email': 'البريد الإلكتروني',
        'avatar': 'الصورة الشخصية',
        'update_profile': 'تحديث الملف',
        'add_client': 'إضافة عميل',
        'edit': 'تعديل',
        'status': 'الحالة',
        'pending': 'قيد الانتظار',
        'in_progress': 'قيد التنفيذ',
        'completed': 'مكتمل',
        'assign_task': 'تعيين مهمة',
        'deadline': 'الموعد النهائي',
        'description': 'الوصف',
        'new_task': 'مهمة جديدة',
        'upload_file': 'رفع ملف',
        'type_message': 'اكتب رسالتك...',
        'send': 'إرسال',
        'download': 'تحميل',
        'no_clients': 'لا يوجد عملاء',
        'client_name': 'اسم العميل',
        'company': 'الشركة',
        'phone': 'الهاتف',
        'actions': 'إجراءات',
        'to': 'إلى',
        'notifications': 'الإشعارات',
        'mark_all_read': 'تحديد الكل كمقروء',
        'no_notifications': 'لا توجد إشعارات',
        'conversations': 'المحادثات',
        'type_here': 'اكتب هنا...',
        'attach_file': 'إرفاق ملف',
        'team_chat': 'محادثة الفريق',
        'private_chat': 'محادثة خاصة',
        'view_profile': 'عرض الملف',
        'portfolio_title': 'أعمالي',
        'services_title': 'خدماتي',
        'service1': 'تصميم واجهات المستخدم',
        'service2': 'تطوير الويب',
        'service3': 'التسويق الرقمي',
        'example1': 'مشروع 1',
        'example2': 'مشروع 2',
        'example3': 'مشروع 3',
        'about_title': 'عن فدلو',
        'about_text': 'أنا فدلو، مطور ومصمم محترف، أعمل على إنشاء تجارب رقمية مذهلة.',
        'about_description': 'أنا مطور ومصمم شغوف، أحب إنشاء تجارب رقمية جميلة ووظيفية. مع أكثر من 5 سنوات من الخبرة، عملت على كل شيء بدءاً من المنصات التعليمية إلى الشركات الناشئة في مجال التكنولوجيا المالية.',
        # Project specific
        'project_sbt_title': 'أكاديمية SBT',
        'project_sbt_desc': 'منصة تعليمية شاملة تخدم الطلاب والمعلمين وأولياء الأمور والإداريين. تتميز بتسجيل الدخول متعدد الأدوار، وإدارة الفصول الدراسية، وتتبع التقدم في الوقت الفعلي.',
        'project_impacto_title': 'IMPACTO ⚡',
        'project_impacto_desc': 'منصة حديثة لرواد الأعمال والمبتكرين. تدعم عدة لغات (العربية، الإنجليزية، الفرنسية)، مع نظام مصادقة متكامل ولوحة تحكم أنيقة مصممة للفرق.',
        'project_fadlo_title': 'منصة فدلو',
        'project_fadlo_desc': 'منصة شخصية حديثة مبنية بإطار Flask، تتميز بتصميم الزجاج الشفاف، دعم متعدد اللغات، إدارة الفريق، والمراسلة الفورية. تعرض أعمالي وخدماتي.',
        'view_project': 'عرض المشروع',
        'details': 'تفاصيل',
        # Service page & UI keys
        'view_examples': 'عرض الأمثلة',
        'see_all_projects': 'عرض جميع المشاريع',
        'services_description': 'استكشف خدماتي الأساسية – انقر على أي بطاقة لرؤية أمثلة حقيقية من عملي في هذا المجال.',
        'coming_soon': 'قريباً',
        'no_examples': 'لا توجد أمثلة لهذه الخدمة.',
        'view_all_examples': 'عرض جميع الأمثلة',
        'back_home': 'العودة إلى الرئيسية',
        'skills_title': 'المهارات والخبرات',
        'experience_title': 'الخبرات',
        'lets_work_together': 'لنعمل معاً',
        'lets_work_desc': 'هل لديك مشروع في ذهنك؟ دعنا نتعاون لتحقيق أفكارك.',
        'get_in_touch': 'تواصل معي',
        'access_portal': 'بوابة الدخول:',
        'admin_login': 'دخول المدير',
        'team_login': 'دخول الفريق',
        # Service bullet points (Arabic)
        'service1_desc': 'تصميم واجهات جميلة تتمحور حول المستخدم.',
        'service1_point1': 'بحث المستخدم وشخصيات',
        'service1_point2': 'تخطيط ونماذج أولية',
        'service1_point3': 'التصميم البصري وأنظمة التصميم',
        'service1_point4': 'اختبار قابلية الاستخدام',
        'service2_desc': 'تطوير كامل المكدس باستخدام Python و Flask و JavaScript الحديثة.',
        'service2_point1': 'تطبيقات ويب مخصصة',
        'service2_point2': 'واجهات برمجة التطبيقات RESTful والخدمات المصغرة',
        'service2_point3': 'تصميم قواعد البيانات وتحسينها',
        'service2_point4': 'النشر و DevOps',
        'service3_desc': 'استراتيجيات قائمة على البيانات لتنمية حضورك على الإنترنت.',
        'service3_point1': 'تحسين محركات البحث واستراتيجية المحتوى',
        'service3_point2': 'إدارة وسائل التواصل الاجتماعي',
        'service3_point3': 'التحليل وإعداد التقارير',
        'service3_point4': 'إعلانات الدفع لكل نقرة والحملات الإعلانية',
        'examples': 'أمثلة',
    },
    'en': {
        'home': 'Home',
        'portfolio': 'Portfolio',
        'services': 'Services',
        'examples': 'Examples',
        'about': 'About',
        'welcome': 'Welcome to FADLO Platform',
        'intro': 'My personal platform to showcase my work and services',
        'footer_text': 'All rights reserved © 2026 FADLO',
        'language': 'Language',
        'dashboard': 'Dashboard',
        'team': 'Team',
        'messages': 'Messages',
        'tasks': 'Tasks',
        'clients': 'Clients',
        'profile': 'Profile',
        'login': 'Login',
        'logout': 'Logout',
        'username': 'Username',
        'password': 'Password',
        'login_title': 'Welcome Back',
        'login_subtitle': 'Sign in to explore the FADLO platform',
        'login_button': 'Sign In',
        'welcome_user': 'Welcome, {username}',
        'invalid_credentials': 'Invalid username or password',
        'stats_projects': 'Projects',
        'stats_clients': 'Clients',
        'stats_experience': 'Years Experience',
        'dashboard_title': 'Dashboard',
        'dashboard_desc': 'FADLO Platform Dashboard',
        'add_member': 'Add Member',
        'member_name': 'Name',
        'member_role': 'Role',
        'send_message': 'Send Message',
        'message_content': 'Message Content',
        'no_members': 'No members yet',
        'no_messages': 'No messages',
        'delete': 'Delete',
        'total_members': 'Total Members',
        'total_messages': 'Total Messages',
        'total_projects': 'Total Projects',
        'total_clients': 'Total Clients',
        'member_added': 'Member added successfully',
        'member_deleted': 'Member deleted',
        'message_sent': 'Message sent',
        'edit_profile': 'Edit Profile',
        'full_name': 'Full Name',
        'email': 'Email',
        'avatar': 'Avatar',
        'update_profile': 'Update Profile',
        'add_client': 'Add Client',
        'edit': 'Edit',
        'status': 'Status',
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'completed': 'Completed',
        'assign_task': 'Assign Task',
        'deadline': 'Deadline',
        'description': 'Description',
        'new_task': 'New Task',
        'upload_file': 'Upload File',
        'type_message': 'Type your message...',
        'send': 'Send',
        'download': 'Download',
        'no_clients': 'No clients yet',
        'client_name': 'Client Name',
        'company': 'Company',
        'phone': 'Phone',
        'actions': 'Actions',
        'to': 'To',
        'notifications': 'Notifications',
        'mark_all_read': 'Mark all as read',
        'no_notifications': 'No notifications',
        'conversations': 'Conversations',
        'type_here': 'Type here...',
        'attach_file': 'Attach file',
        'team_chat': 'Team Chat',
        'private_chat': 'Private Chat',
        'view_profile': 'View Profile',
        'portfolio_title': 'My Portfolio',
        'services_title': 'My Services',
        'service1': 'UI/UX Design',
        'service2': 'Web Development',
        'service3': 'Digital Marketing',
        'example1': 'Project 1',
        'example2': 'Project 2',
        'example3': 'Project 3',
        'about_title': 'About FADLO',
        'about_text': 'I am FADLO, a professional developer and designer, creating amazing digital experiences.',
        'about_description': "I'm a passionate developer and designer with a love for creating beautiful, functional digital experiences. With 5+ years of experience, I've worked on everything from educational platforms to fintech startups.",
        'project_sbt_title': 'SBT ACADEMY',
        'project_sbt_desc': 'A comprehensive educational management platform serving students, teachers, parents, and administrators. Features multi‑role authentication, class management, and real‑time progress tracking.',
        'project_impacto_title': 'IMPACTO ⚡',
        'project_impacto_desc': 'A modern platform for entrepreneurs and innovators. Features multi‑language support (Arabic, English, French), user authentication, and a sleek dashboard designed for teams.',
        'project_fadlo_title': 'FADLO Platform',
        'project_fadlo_desc': 'A modern personal platform built with Flask, featuring glass‑morphism design, multi‑language support, team management, and real‑time messaging. Showcases my work and services.',
        'view_project': 'View Project',
        'details': 'Details',
        'view_examples': 'View examples',
        'see_all_projects': 'See All Projects',
        'services_description': 'Explore my core services – click on any card to see real examples of my work in that area.',
        'coming_soon': 'Coming soon',
        'no_examples': 'No examples found for this service.',
        'view_all_examples': 'View all examples',
        'back_home': 'Back to Home',
        'skills_title': 'Skills & Expertise',
        'experience_title': 'Experience',
        'lets_work_together': "Let's Work Together",
        'lets_work_desc': "Have a project in mind? Let's collaborate and bring your ideas to life.",
        'get_in_touch': 'Get in Touch',
        'access_portal': 'Access your portal:',
        'admin_login': 'Admin Login',
        'team_login': 'Team Login',
        # Service bullet points (English)
        'service1_desc': 'Crafting beautiful, user-centered interfaces that delight.',
        'service1_point1': 'User Research & Personas',
        'service1_point2': 'Wireframing & Prototyping',
        'service1_point3': 'Visual Design & Design Systems',
        'service1_point4': 'Usability Testing',
        'service2_desc': 'Full-stack development with Python, Flask, and modern JavaScript.',
        'service2_point1': 'Custom Web Applications',
        'service2_point2': 'RESTful APIs & Microservices',
        'service2_point3': 'Database Design & Optimization',
        'service2_point4': 'Deployment & DevOps',
        'service3_desc': 'Data-driven strategies to grow your online presence.',
        'service3_point1': 'SEO & Content Strategy',
        'service3_point2': 'Social Media Management',
        'service3_point3': 'Analytics & Reporting',
        'service3_point4': 'PPC & Ad Campaigns',
        'examples': 'Examples',
    },
    'fr': {
        'home': 'Accueil',
        'portfolio': 'Portfolio',
        'services': 'Services',
        'examples': 'Exemples',
        'about': 'À propos',
        'welcome': 'Bienvenue sur la plateforme FADLO',
        'intro': 'Ma plateforme personnelle pour présenter mon travail et mes services',
        'footer_text': 'Tous droits réservés © 2026 FADLO',
        'language': 'Langue',
        'dashboard': 'Tableau de bord',
        'team': 'Équipe',
        'messages': 'Messages',
        'tasks': 'Tâches',
        'clients': 'Clients',
        'profile': 'Profil',
        'login': 'Connexion',
        'logout': 'Déconnexion',
        'username': "Nom d'utilisateur",
        'password': 'Mot de passe',
        'login_title': 'Bon retour',
        'login_subtitle': 'Connectez‑vous pour explorer la plateforme FADLO',
        'login_button': 'Se connecter',
        'welcome_user': 'Bienvenue, {username}',
        'invalid_credentials': "Nom d'utilisateur ou mot de passe incorrect",
        'stats_projects': 'Projets',
        'stats_clients': 'Clients',
        'stats_experience': "Années d'expérience",
        'dashboard_title': 'Tableau de bord',
        'dashboard_desc': 'Tableau de bord de la plateforme FADLO',
        'add_member': 'Ajouter un membre',
        'member_name': 'Nom',
        'member_role': 'Rôle',
        'send_message': 'Envoyer un message',
        'message_content': 'Contenu du message',
        'no_members': 'Aucun membre pour le moment',
        'no_messages': 'Aucun message',
        'delete': 'Supprimer',
        'total_members': 'Total des membres',
        'total_messages': 'Total des messages',
        'total_projects': 'Total des projets',
        'total_clients': 'Total des clients',
        'member_added': 'Membre ajouté avec succès',
        'member_deleted': 'Membre supprimé',
        'message_sent': 'Message envoyé',
        'edit_profile': 'Modifier le profil',
        'full_name': 'Nom complet',
        'email': 'Email',
        'avatar': 'Avatar',
        'update_profile': 'Mettre à jour',
        'add_client': 'Ajouter un client',
        'edit': 'Modifier',
        'status': 'Statut',
        'pending': 'En attente',
        'in_progress': 'En cours',
        'completed': 'Terminé',
        'assign_task': 'Attribuer une tâche',
        'deadline': 'Date limite',
        'description': 'Description',
        'new_task': 'Nouvelle tâche',
        'upload_file': 'Télécharger un fichier',
        'type_message': 'Écrivez votre message...',
        'send': 'Envoyer',
        'download': 'Télécharger',
        'no_clients': 'Aucun client',
        'client_name': 'Nom du client',
        'company': 'Société',
        'phone': 'Téléphone',
        'actions': 'Actions',
        'to': 'À',
        'notifications': 'Notifications',
        'mark_all_read': 'Tout marquer comme lu',
        'no_notifications': 'Aucune notification',
        'conversations': 'Conversations',
        'type_here': 'Écrivez ici...',
        'attach_file': 'Joindre un fichier',
        'team_chat': 'Chat d\'équipe',
        'private_chat': 'Chat privé',
        'view_profile': 'Voir le profil',
        'portfolio_title': 'Mon Portfolio',
        'services_title': 'Mes Services',
        'service1': 'Design UI/UX',
        'service2': 'Développement Web',
        'service3': 'Marketing Digital',
        'example1': 'Projet 1',
        'example2': 'Projet 2',
        'example3': 'Projet 3',
        'about_title': 'À propos de FADLO',
        'about_text': 'Je suis FADLO, développeur et designer professionnel, créant des expériences numériques incroyables.',
        'about_description': "Je suis un développeur et designer passionné, j'aime créer des expériences numériques belles et fonctionnelles. Avec plus de 5 ans d'expérience, j'ai travaillé sur tout, des plateformes éducatives aux startups fintech.",
        'project_sbt_title': 'SBT ACADEMY',
        'project_sbt_desc': 'Une plateforme de gestion éducative complète au service des étudiants, des enseignants, des parents et des administrateurs. Fonctionnalités : authentification multi‑rôles, gestion des classes et suivi en temps réel.',
        'project_impacto_title': 'IMPACTO ⚡',
        'project_impacto_desc': 'Une plateforme moderne pour les entrepreneurs et les innovateurs. Prend en charge plusieurs langues (arabe, anglais, français), avec une authentification utilisateur et un tableau de bord élégant conçu pour les équipes.',
        'project_fadlo_title': 'Plateforme FADLO',
        'project_fadlo_desc': 'Une plateforme personnelle moderne construite avec Flask, offrant un design en verre, un support multi‑langues, une gestion d’équipe et une messagerie en temps réel. Présente mon travail et mes services.',
        'view_project': 'Voir le projet',
        'details': 'Détails',
        'view_examples': 'Voir les exemples',
        'see_all_projects': 'Voir tous les projets',
        'services_description': 'Explorez mes services principaux – cliquez sur une carte pour voir des exemples réels de mon travail dans ce domaine.',
        'coming_soon': 'Bientôt disponible',
        'no_examples': 'Aucun exemple pour ce service.',
        'view_all_examples': 'Voir tous les exemples',
        'back_home': 'Retour à l\'accueil',
        'skills_title': 'Compétences et expertise',
        'experience_title': 'Expérience',
        'lets_work_together': 'Travaillons ensemble',
        'lets_work_desc': 'Vous avez un projet en tête ? Collaborons pour donner vie à vos idées.',
        'get_in_touch': 'Contactez‑moi',
        'access_portal': 'Accédez à votre portail :',
        'admin_login': 'Connexion Admin',
        'team_login': 'Connexion Équipe',
        # Service bullet points (French)
        'service1_desc': "Créer des interfaces belles et centrées sur l'utilisateur.",
        'service1_point1': 'Recherche utilisateur & Personas',
        'service1_point2': 'Wireframing & Prototypage',
        'service1_point3': 'Design visuel & Systèmes de design',
        'service1_point4': "Tests d'utilisabilité",
        'service2_desc': 'Développement full-stack avec Python, Flask et JavaScript moderne.',
        'service2_point1': 'Applications Web personnalisées',
        'service2_point2': 'API RESTful & Microservices',
        'service2_point3': 'Conception et optimisation de bases de données',
        'service2_point4': 'Déploiement & DevOps',
        'service3_desc': 'Stratégies basées sur les données pour développer votre présence en ligne.',
        'service3_point1': 'SEO & Stratégie de contenu',
        'service3_point2': 'Gestion des réseaux sociaux',
        'service3_point3': 'Analytique & Rapports',
        'service3_point4': 'PPC & Campagnes publicitaires',
        'examples': 'Exemples',
    }
}

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def get_lang():
    return session.get('lang', 'ar')

@app.context_processor
def inject_translations():
    lang = get_lang()
    t = translations.get(lang, translations['ar'])
    return dict(t=t, lang=lang)

@app.context_processor
def utility_processor():
    def unread_count():
        if session.get('user_id'):
            user_id = session['user_id']
            return Message.query.filter(
                (Message.receiver_id == None) | 
                (Message.receiver_id == user_id)
            ).count()
        return 0
    def get_user(user_id):
        if user_id:
            return User.query.get(user_id)
        return None
    return dict(unread_count=unread_count, get_user=get_user)

# ------------------------------------------------------------------
# Database Models
# ------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='member')
    avatar = db.Column(db.String(200), default='https://i.pravatar.cc/150?img=1')
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin', role='admin',
                     full_name='Admin', email='admin@fadlo.com')
        db.session.add(admin)
        db.session.commit()

# ------------------------------------------------------------------
# Helpers: admin_required, login_required
# ------------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ------------------------------------------------------------------
# Public Routes
# ------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', username=session.get('username'))

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', username=session.get('username'))

@app.route('/services')
def services():
    return render_template('services.html', username=session.get('username'))

@app.route('/examples')
def examples():
    service = request.args.get('service')
    if service:
        filtered_projects = [p for p in PROJECTS if p['service'] == service]
    else:
        filtered_projects = PROJECTS
    return render_template('examples.html', projects=filtered_projects, username=session.get('username'))

@app.route('/about')
def about():
    return render_template('about.html', username=session.get('username'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user.avatar = url_for('static', filename='uploads/' + filename)
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user, username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['last_read'] = datetime.utcnow().isoformat()
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/lang/<lang>')
def set_lang(lang):
    if lang in translations:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

# ------------------------------------------------------------------
# Notification API
# ------------------------------------------------------------------
@app.route('/api/notifications')
@login_required
def get_notifications():
    user_id = session['user_id']
    messages = Message.query.filter(
        (Message.receiver_id == None) | 
        (Message.receiver_id == user_id)
    ).order_by(Message.timestamp.desc()).limit(10).all()
    notifs = []
    for msg in messages:
        sender = User.query.get(msg.sender_id)
        notifs.append({
            'id': msg.id,
            'sender': sender.full_name or sender.username,
            'content': msg.content[:50] + '...' if len(msg.content) > 50 else msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M %d-%m'),
            'is_team': msg.receiver_id is None,
            'url': url_for('messages')
        })
    return jsonify(notifs)

@app.route('/api/mark_read')
@login_required
def mark_read():
    session['last_read'] = datetime.utcnow().isoformat()
    return jsonify({'status': 'ok'})

# ------------------------------------------------------------------
# Admin & Team Routes
# ------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    is_admin = (user.role == 'admin')
    if is_admin:
        total_projects = 50
        total_clients = Client.query.count()
        total_team = User.query.filter_by(role='member').count()
        total_tasks = Task.query.count()
        pending_tasks = Task.query.filter_by(status='pending').count()
        members = User.query.filter_by(role='member').all()
        performance = []
        for m in members:
            done = Task.query.filter_by(assigned_to=m.id, status='completed').count()
            performance.append({'name': m.full_name or m.username, 'done': done})
        return render_template('dashboard.html',
                               is_admin=True,
                               total_projects=total_projects,
                               total_clients=total_clients,
                               total_team=total_team,
                               total_tasks=total_tasks,
                               pending_tasks=pending_tasks,
                               performance=performance,
                               username=session.get('username'))
    else:
        my_tasks = Task.query.filter_by(assigned_to=user.id).all()
        return render_template('dashboard.html',
                               is_admin=False,
                               my_tasks=my_tasks,
                               username=session.get('username'))

@app.route('/dashboard/team', methods=['GET', 'POST'])
@login_required
def team():
    user = User.query.get(session['user_id'])
    is_admin = (user.role == 'admin')
    if request.method == 'POST' and is_admin:
        username = request.form.get('username')
        password = request.form.get('password') or '123456'
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        if not username:
            flash('Username is required.', 'danger')
            return redirect(url_for('team'))
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password, role='member',
                            full_name=full_name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Member added!', 'success')
        else:
            flash('Username already exists.', 'danger')
        return redirect(url_for('team'))
    members = User.query.filter_by(role='member').all()
    return render_template('team.html', members=members, is_admin=is_admin, username=session.get('username'))

@app.route('/dashboard/team/delete/<int:user_id>')
@admin_required
def delete_team_member(user_id):
    user = User.query.get(user_id)
    if user and user.role != 'admin':
        db.session.delete(user)
        db.session.commit()
        flash('Member deleted.', 'info')
    return redirect(url_for('team'))

@app.route('/dashboard/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    user = User.query.get(session['user_id'])
    is_admin = (user.role == 'admin')
    if request.method == 'POST' and is_admin:
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        deadline = request.form.get('deadline')
        if title and assigned_to:
            task = Task(title=title, description=description,
                        assigned_to=int(assigned_to),
                        assigned_by=session['user_id'],
                        deadline=datetime.strptime(deadline, '%Y-%m-%d') if deadline else None)
            db.session.add(task)
            db.session.commit()
            flash('Task assigned!', 'success')
        return redirect(url_for('tasks'))
    if is_admin:
        members = User.query.filter_by(role='member').all()
        all_tasks = Task.query.all()
        return render_template('tasks.html', members=members, tasks=all_tasks, is_admin=True, username=session.get('username'))
    else:
        my_tasks = Task.query.filter_by(assigned_to=user.id).all()
        return render_template('tasks.html', tasks=my_tasks, is_admin=False, username=session.get('username'))

@app.route('/dashboard/tasks/update/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get(task_id)
    if task and (task.assigned_to == session['user_id'] or session.get('role') == 'admin'):
        task.status = request.form.get('status')
        db.session.commit()
        flash('Task updated.', 'success')
    else:
        flash('You are not authorized.', 'danger')
    return redirect(url_for('tasks'))

@app.route('/dashboard/tasks/delete/<int:task_id>')
@admin_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'info')
    return redirect(url_for('tasks'))

@app.route('/dashboard/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if request.method == 'POST':
        content = request.form.get('content')
        receiver_id = request.form.get('receiver_id')
        file = request.files.get('file')
        file_path = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_path = url_for('static', filename='uploads/' + filename)
        if content or file_path:
            msg = Message(
                sender_id=session['user_id'],
                receiver_id=int(receiver_id) if receiver_id else None,
                content=content or '',
                file_path=file_path
            )
            db.session.add(msg)
            db.session.commit()
            flash('Message sent!', 'success')
        return redirect(url_for('messages'))

    user_id = session['user_id']
    messages_list = Message.query.filter(
        (Message.receiver_id == None) |
        (Message.sender_id == user_id) |
        (Message.receiver_id == user_id)
    ).order_by(Message.timestamp.asc()).all()
    members = User.query.filter(User.id != user_id).all()
    return render_template('messages.html', messages=messages_list, members=members, username=session.get('username'))

@app.route('/dashboard/clients', methods=['GET', 'POST'])
@admin_required
def clients():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        if name:
            client = Client(name=name, email=email, phone=phone,
                            company=company, created_by=session['user_id'])
            db.session.add(client)
            db.session.commit()
            flash('Client added!', 'success')
        return redirect(url_for('clients'))
    clients_list = Client.query.all()
    return render_template('clients.html', clients=clients_list, username=session.get('username'))

@app.route('/dashboard/clients/delete/<int:client_id>')
@admin_required
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted.', 'info')
    return redirect(url_for('clients'))

@app.route('/dashboard/clients/edit/<int:client_id>', methods=['POST'])
@admin_required
def edit_client(client_id):
    client = Client.query.get(client_id)
    if client:
        client.name = request.form.get('name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.company = request.form.get('company')
        db.session.commit()
        flash('Client updated.', 'success')
    return redirect(url_for('clients'))

# ------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)