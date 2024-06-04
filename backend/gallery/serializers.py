from rest_framework import serializers
from gallery.models import Gallery
        
        
from rest_framework import serializers



# Work on delete (not working)
# Add Create 
class GallerySerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SerializerMethodField()  # New field

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'uploaded_at', 'description', 'uploaded_by')

    def get_uploaded_by(self, obj):
        # Access the related user object
        user = obj.uploaded_by
        if user:
            return user.email  # Assuming username is the desired field
        else:
            return None  # Handle cases where uploaded_by might be null
