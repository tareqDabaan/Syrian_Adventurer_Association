# Third-part library imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError, RefreshToken

# Local modules imports
from users.models import *

# Django imports
from django.contrib.auth.password_validation import validate_password
import datetime

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'current_city', 'phone']
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

    def to_representation(self, instance: User):
        full_name = "{} {}".format(instance.first_name, instance.last_name)
        
        return {
            "id": instance.id
            , "email": instance.email
            , "full_name": full_name
            , "location": instance.current_city
            , "phone": instance.phone
            # todo, "image":instance.image.split(",")
        }


class SignupSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=64, write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=64, write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        #? To not show the password
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        #? Hashing the password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
    
    def validate(self, attrs):

       password, password2 = attrs.get("password"), attrs.pop("password2")

       if password != password2:
           raise serializers.ValidationError({"password": "Password fields must match."})

       return attrs
       
    """
    Will be used later to verify phone number 
    
    phone = attrs.get("phone")
    reg_exp = re.search("^[00963]\d{12,15}$", phone)
    if not reg_exp:
        raise serializers.ValidationError(
            {"phone error": "Phone number must be between 12, 15 digits and starts with a 00963"})
    """
    

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6, required=True)
    
    def validate_otp(self, otp):
        if not otp.isdigit():
            raise serializers.ValidationError("OTP should only contain digits.")
        
        if len(otp) != 6:
            raise serializers.ValidationError("OTP should be a six-digit code.")
        
        return otp

    # def validate(self, attrs):
    #     super().validate(attrs)
    #     email = attrs["email"]
    #     otp = attrs["otp"]

    #     user = User.objects.filter(email=email).first()

    #     # Update user's account status
    #     user.is_verified = True
    #     user.save()


class LogInSerializer(TokenObtainPairSerializer):
    
    default_error_messages = {
        'detail': 'Invalid email or password.'  # Use your preferred message here
    }

    
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        attrs = super().validate(attrs)
        user = self.user
       
        if not user.is_verified:
            raise serializers.ValidationError({'is_verified':'Your account is not verified, please verify confirm your email'})
    
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token':{'Token expired or invalid'}
    }
    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

        
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPcheck(serializers.Serializer):
    otp = serializers.CharField(max_length = 6)


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(required = True)
    re_password = serializers.CharField(required = True)


class CompleteSignUpSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=256)
    birth_day = serializers.DateField()
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'mother_name',  'gender', 'martial_status', 'work', 'emergency_number',  'current_city', 'phone', 'birth_day', 'age'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
  
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

    def validate(self, data):

        #? Overriding validation so we can split the full name entered by the user and store it in the database as (first_name, mid_name, last_name)
        full_name = data.get('full_name')
        names = full_name.split()

        #? getting the birthday to store the age in the database 
        birthday_date = data.get('birth_day')
        today = datetime.date.today()
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

        if len(names) == 2:
            first_name, last_name = names
            mid_name = ''
        
        elif len(names) == 3:
            first_name, mid_name, last_name = names
        
        else:
            raise serializers.ValidationError("Invalid full name format.")

        data['age'] = age
        data['first_name'] = first_name
        data['mid_name'] = mid_name
        data['last_name'] = last_name

        return data
    
    def to_representation(self, instance: User):
        full_name = "{} {} {}".format(instance.first_name, instance.mid_name, instance.last_name)

        return {
            "id": instance.id
            , "full_name": full_name
            , "mother_name": instance.mother_name
            , "gender": instance.gender
            , "martial_status":instance.martial_status
            , "work":instance.work
            , "emergency_number":instance.emergency_number
            , "current_city":instance.current_city
            , "phone": instance.phone
            , "age": instance.age
        }
    


class ListMemberDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'age', 'date_joined', 'current_city', 'social_media_profiles']

    def to_representation(self, instance):
        full_name = "{} {}".format(instance.first_name, instance.last_name)

        return {
            "id": instance.id
            , "full_name": full_name
            , "current_city":instance.current_city
            , "started_at": instance.date_joined
            , "age": instance.age
            , "social_media_accounts": instance.social_media_profiles
        }