from rest_framework.decorators import api_view
import random
from rest_framework.response import Response
from activities import models
from datetime import datetime, timedelta
from members.models import Member
from PIL import Image
import io
from django.core.files.base import ContentFile

def generate_image():
    # Create a simple image using PIL
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return ContentFile(byte_im, name='mock_image.png')


@api_view(['POST'])
def create_mock_activities(request):
    try:
        n = request.data.get('n', 5)  
        pictures = ['https://unsplash.com/photos/brown-dome-tent-near-trees-at-night-8f_VQ3EFbTg']
        
        
        activity_names = ["Mountain Trekking", "Beach Camping", "City Hiking", "Forest Adventure", "River Rafting"]
        locations = ["Lattakia, Mashqita, جزيرة الاكواخ", "Tartus, Al-Qadmus, قمة النبي شيث", "Yosemite Park", "Amazon Rainforest", "Nile River"]
        descriptions = [
            "A thrilling adventure on the mountains.",
            "A serene camping experience by the beach.",
            "Exploring the city trails.",
            "An adventurous trip through the forest.",
            "Exciting river rafting activity."
        ]
        activity_types = models.ActivityType.objects.all()
        members = list(Member.objects.all())
        for i in range(n):
            start_time = datetime.now() + timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(hours=random.randint(1, 5))
            registration_deadline = start_time - timedelta(days=random.randint(1, 3))

            activity = models.Activity.objects.create(
                activity_type=random.choice(activity_types),
                point_on_map='MULTIPOINT((12.9715987 77.5945627))',
                start_at=start_time,
                ends_at=end_time,
                max_participants=random.randint(50, 100),
                activity_name=random.choice(activity_names),
                activity_fee=round(random.uniform(10, 100), 2),
                activity_description=random.choice(descriptions),
                registration_deadline=registration_deadline.date(),
                location=random.choice(locations),
                image=random.choice(pictures)
            )
            random_members = random.sample(members, k=min(len(members), random.randint(1,2)))
            activity.members.set(random_members)
        
        return Response({"message": "Mock activities created successfully."}, status=201)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
        print(e)