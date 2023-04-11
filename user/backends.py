import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class FirebaseBackend(BaseBackend):
    def authenticate(self, request, id_token=None, **kwargs):
        try:
            cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            decoded_token = auth.verify_id_token(id_token)
            email = decoded_token["email"]
            user = self.get_or_create_user(email)
            return user
        except auth.InvalidIdTokenError:
            return None
        except ValueError:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def get_or_create_user(self, email):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            return user
        except UserModel.DoesNotExist:
            user = UserModel.objects.create_user(email=email, password=None)
            return user


class AdmissionIdBackend(BaseBackend):
    def authenticate(self, request, admission_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(admission_number=admission_number)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
