from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new provider."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
  


    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username','name','phone_number','language','currency','password']

    def create(self, validated_data):

        return User.objects.register_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255,read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
   
        username = data.get('username', None)
        password = data.get('password', None)

        # Raise an exception if a
        # username is not provided.
        if username is None:
            raise serializers.ValidationError(
                'A username is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )


        user = authenticate(username=username, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'token': user.token
        }










class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""


    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )


    # We want to get the `bio` and `image` fields from the related Profile
    # model.
    
    class Meta:
        model = User
        fields = ('email', 'username', 'name','language','currency','phone_number','password')

        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})


        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.

            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        for (key, value) in profile_data.items():
        # We're doing the same thing as above, but this time we're making
        # changes to the Profile model.

            setattr(instance.profile, key, value)

            # Save the profile just like we saved the user.
            instance.profile.save()

        return instance

