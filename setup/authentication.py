from rest_framework_simplejwt.authentication import JWTAuthentication


class NoChallengeJWTAuthentication(JWTAuthentication):
    def authenticate_header(self, request):
        return None
