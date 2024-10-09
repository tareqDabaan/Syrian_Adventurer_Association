from rest_framework.decorators import api_view
import random
from members import models
from rest_framework.response import Response

def get_male_names():
    male_names = [
        'Ali', 'Omar', 'Mohammed', 'Ahmed', 'Youssef', 'Khaled', 'Hassan', 'Hussein', 'Mustafa', 'Abdullah',
        'Sami', 'Faisal', 'Hamza', 'Karim', 'Tariq', 'Nasser', 'Salah', 'Bilal', 'Amin', 'Jamil',
        'Rashid', 'Majid', 'Nasir', 'Rami', 'Jamal', 'Imad', 'Ziad', 'Waleed', 'Riad', 'Mahmoud',
        'Mansour', 'Raed', 'Adel', 'Bader', 'Nabil', 'Fadi', 'Hadi', 'Saad', 'Nizar', 'Fawzi',
        'Zakaria', 'Tarik', 'Khalid', 'Musa', 'Abdel', 'Ibrahim', 'Wael', 'Bassem', 'Othman', 'Ismail'
    ]

    return male_names

def get_arabic_female_names():
    arabic_female_names = [
        'Fatima', 'Amina', 'Khadija', 'Zainab', 'Mariam', 'Huda', 'Layla', 'Sara', 'Nour', 'Rana',
        'Hana', 'Lina', 'Rasha', 'Asma', 'Amal', 'Malak', 'Jana', 'Dana', 'Maha', 'Samar',
        'Wafa', 'Ghada', 'Hayat', 'Rawan', 'Maya', 'Nadia', 'Saida', 'Dalal', 'Nada', 'Sana'
    ]
    return arabic_female_names

def get_job_titles():
    job_titles = [
        'Software Engineer', 'Doctor', 'Teacher', 'Accountant', 'Lawyer', 'Nurse', 'Chef', 'Mechanical Engineer',
        'Electrician', 'Plumber', 'Architect', 'Graphic Designer', 'Sales Manager', 'Marketing Specialist',
        'Financial Analyst', 'HR Manager', 'Operations Manager', 'Project Manager', 'Data Analyst', 'Journalist',
        'Pharmacist', 'Dentist', 'Pilot', 'Police Officer', 'Firefighter', 'Professor', 'Research Scientist',
        'Writer', 'Artist', 'Musician', 'Fitness Instructor', 'Real Estate Agent', 'Entrepreneur', 'Consultant',
        'Barista', 'Delivery Driver',
        'Electrician', 'Fashion Designer', 'Photographer', 'Veterinarian', 'Social Worker', 'Librarian',
        'Event Planner', 'Insurance Agent', 'Web Developer'
    ]
    return job_titles

@api_view(['POST'])
def create_mock_users(request):

    try:
        n = request.data.get('n', 5)  
        male_names = get_male_names()
        female_names = get_arabic_female_names()
        job_title = get_job_titles()
        for i in range(n):
            first_name = random.choice(male_names)
            last_name = random.choice(male_names)
            mid_name = random.choice(male_names)
            mother_name = random.choice(female_names)
            job = random.choice(job_title)
            
            models.Member.objects.create(
                first_name=first_name,
                mid_name=mid_name,
                last_name=last_name,
                mother_name=mother_name,
                gender=random.choice(['MALE', 'FEMALE']),
                phone=f'00963456789023{i}',
                current_city=random.choice(['Homs', 'Damascus', 'Lattakia', 'Hama', 'Aleppo', 'Tartus', 'Alqadmus']),
                work=job,
                martial_status=random.choice(['SINGLE', 'MARRIED']),
                email=f'{first_name.lower()}{last_name.lower()}@gmail.com',
                age=random.randint(18, 60),
                social_media_profiles={"instagram":"www.instagram.com","facebook":"www.facebook.com","youtube":"www.youtube.com"},
                is_active=True,
            )
            
        return Response({"message": "Mock users created successfully."}, status=201)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)