from django.db import models

# saving user data
class user(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='نام کاربری')
    email = models.EmailField(verbose_name="آدرس ایمیل")
    password = models.CharField(max_length=50, verbose_name="رمز عبور")


#saving uploaded images
class Image(models.Model):
    categories = (
        ('cars', 'خودرو'),
        ('animation', 'انیمیشن'),
        ('abstract', 'اجسام سه بعدی'),
        ('nature', 'طبیعت'),
        ('space', 'فضا'),
        ('movies', 'فیلم'),
        ('games', 'گیم'),
        ('typography', 'تایپوگرافی'),
        ('architecture', 'معماری'),
        ('fashion', 'فشن')
    )
    Image_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default=None, verbose_name="عنوان تصویر")
    img = models.ImageField(upload_to='images/', default=None, verbose_name="بارگزاری تصویر")
    Image_description = models.CharField(max_length=1000, verbose_name="توضیحات عکس")
    Image_category = models.CharField(max_length=100, choices=categories, verbose_name="دسته بندی عکس")
    image_owner_id = models.IntegerField()



