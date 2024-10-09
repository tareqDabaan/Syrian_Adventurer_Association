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
        n = request.data.get('n',5)  
        pictures = ['https://unsplash.com/photos/brown-dome-tent-near-trees-at-night-8f_VQ3EFbTg']
        activity_names = ["Mountain Trekking", "Beach Camping", "City Hiking", "Forest Adventure", "River Rafting",
                          "Desert Safari","Island Hopping","Coastal Kayaking","Jungle Expedition","Canyon Climbing","Glacier Hiking",
                          "Waterfall Rappelling","Savannah Wildlife Tour","Coral Reef Diving","Sunset Sailing","Cave Exploration",
                          "Volcanic Trail Trekking","Alpine Skiing","Mangrove Boat Tour","Arctic Snowshoeing","Cliffside Camping","Wilderness Survival Training","Hot Air Ballooning",
                          "Coastal Trail Running","Historical City Tour"
                          ]
        
        
        locations = ["Lattakia", "Tartus", "Homs", "Mashqita", "Alqadmus", "Safita", "Kafroun", "Maloula", "Slunfa", "Kasab"
                     ,"Chalma" , "Wadi Qandil" , "Al ghzlan island" , "Al badrousia", "Al Sheir" , "Raas al basit" , "jableh" , "al qurdaha"
                     ]
        
        
        descriptions = [
            "A thrilling adventure on the mountains.",
            "A serene camping experience by the beach.",
            "Exploring the city trails.",
            "An adventurous trip through the forest.",
            "Exciting river rafting activity.",
            "An exhilarating journey through the desert dunes.",
            "Explore multiple islands on this adventurous trip.",
            "Paddle along the scenic coastline in a kayak.",
            "A deep dive into the heart of the jungle.",
            "Scale the towering canyons on this climbing adventure.",
            "A breathtaking hike across glacial terrains.",
            "Descend waterfalls with thrilling rappelling techniques.",
            "Experience the wild on a tour through the savannah.",
            "Dive into vibrant coral reefs teeming with marine life.",
            "Sail into the sunset with picturesque views.",
            "Discover hidden caves and underground mysteries.",
            "Trek along volcanic trails with stunning landscapes.",
            "Ski down the slopes of majestic alpine mountains.",
            "Navigate through lush mangroves on a boat.",
            "Trek across the snowy Arctic landscape with snowshoes.",
            "Camp on the edge of cliffs for a stunning view.",
            "Learn essential survival skills in the wilderness.",
            "Float high above the landscape in a hot air balloon.",
            "Run along the beautiful coastal trails.",
            "Explore the rich history of a city on foot."            
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
                activity_fee=round(random.uniform(60000, 900000), 2),
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