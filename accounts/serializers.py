import re
from datetime import date
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, VoterProfile



def alphanumeric_validator(value):
    if not re.fullmatch(r"[A-Za-z0-9]+", value):
        raise serializers.ValidationError(
            "This field must contain only letters and numbers."
        )
    return value



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    national_id = serializers.CharField(
        validators=[alphanumeric_validator]
    )

    vin = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[alphanumeric_validator]
    )

    class Meta:
        model = User
        fields = [
            "national_id",
            "first_name",
            "last_name",
            "dob",
            "state",
            "lga",
            "profile_pic",
            "vin",
            "password",
        ]

    def validate_dob(self, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )
        if age < 18:
            raise serializers.ValidationError(
                "You must be at least 18 years old to register."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    national_id = serializers.CharField(
        validators=[alphanumeric_validator]
    )
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        national_id = str(data.get("national_id", "")).strip()
        password = data.get("password")

        if not national_id or not password:
            raise serializers.ValidationError({
                "non_field_errors": "Both national_id and password are required."
            })

        user = authenticate(
            national_id=national_id,
            password=password
        )

        if not user:
            raise serializers.ValidationError({
                "non_field_errors": "Invalid national_id or password."
            })

        data["user"] = user
        return data



class VoteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoterProfile
        fields = "__all__"




# from rest_framework import serializers
# from .models import User,VoterProfile


# from rest_framework import serializers
# from datetime import date
# from .models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "national_id",
#             "first_name",
#             "last_name",
#             "dob",
#             "state",
#             "lga",
#             "profile_pic",
#             "vin",
#             "password",
#         ]

#     def validate_dob(self, value):
#         today = date.today()
#         age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
#         if age < 18:
#             raise serializers.ValidationError("You must be at least 18 years old to register.")
#         return value

#     def create(self, validated_data):
#         password = validated_data.pop("password")
#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


# from django.contrib.auth import authenticate
# from rest_framework import serializers

# class LoginSerializer(serializers.Serializer):
#     national_id = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         national_id = data.get("national_id", "").strip()
#         password = data.get("password")

#         if not national_id or not password:
#             raise serializers.ValidationError({
#                 "non_field_errors": "Both national_id and password are required."
#             })

#         user = authenticate(national_id=national_id, password=password)
#         if not user:
#             raise serializers.ValidationError({
#                 "non_field_errors": "Invalid national_id or password."
#             })

#         data["user"] = user
#         return data




# class VoteProfileserializer(serializers.Serializer):
#     class Meta:
#         model =VoterProfile
#         fields = "__all__"

