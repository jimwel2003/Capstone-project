from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import auth, home, user, organic, reservation, certificate

urlpatterns = [
    path('', home.index, name='index'),
    path('register', home.register, name='register'),
    path('validation/<str:id>', user.validation, name='validation'),
    path('profile/<str:id>', user.profile, name='profile'),
    path('organic', organic.index, name='organic'),
    path('fertilizer', organic.fertilizer, name='fertilizer'),
    path('fertilizer-details/<str:id>', organic.fertilizer_details, name='fertilizer-details'),
    path('post-fertilizer-feedback/<str:id>', organic.post_fertilizer_feedback, name='post-fertilizer-feedback'),
    path('fertilizer-conversion', organic.fertilizer_conversion, name='fertilizer-conversion'),
    path('pesticide', organic.pesticide, name='pesticide'),
    path('pesticide-details/<str:id>', organic.pesticide_details, name='pesticide-details'),
    path('post-pesticide-feedback/<str:id>', organic.post_pesticide_feedback, name='post-pesticide-feedback'),
    path('pesticide-conversion', organic.pesticide_conversion, name='pesticide-conversion'),
    path('reservations', reservation.index, name='reservations'),
    path('new-reservation', reservation.add, name='new-reservation'),
    path('admin-reservation', reservation.admin_reservation, name='admin-reservation'),
    path('reservation-details/<str:id>', reservation.reservation_details, name='reservation-details'),
    path('signin', auth.signin, name='signin'),
    path('signout', auth.signout, name='signout'),
    path('forgot-password', auth.forgot, name='forgot-password'),
    path('new-password/<str:id>', auth.new_password, name='new-password'),
    path('certificate', certificate.index, name='certificate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
