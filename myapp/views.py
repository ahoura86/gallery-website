from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import ImageForm
user_info = {
    "i" : 0,
    "n" : "",
    "e" : "",
    "p" : ""
}
context = {
    "form" : ImageForm,
    "validation_and_success" : "",
    "images" : Image.objects.all(),
    "categories" : [],
    "chosen_category" : "",
    "registered" : False,
    "i" : user_info["i"],
    "n" : user_info["n"],
    "e" : user_info["e"],
    "p" : user_info["p"]
}
for category in Image.categories:
    context["categories"].append(category[1])


# repository clas
class repository:

    # sign up function
    def create(self, input_name, input_email, input_password):
        username_check = user.objects.filter(name=input_name)
        useremail_check = user.objects.filter(email=input_email)
        if username_check or useremail_check:
            context["validation_and_success"] = "این اطلاعات قبلا ثبت شده است"
            return False
        else:
            object = user(name=input_name, email=input_email, password=input_password)
            try:
                object.save()
                user_info["i"] = object.id
                user_info["n"] = object.name
                user_info["e"] = object.email
                user_info["p"] = object.password
                context["registered"] = True
                return True
            except:
                context["validation_and_success"] = "اطلاعات وارد شده معتبر نیست"
                return False


    # log in function
    def log_in(self, input_name, input_email, input_password):
        users = user.objects.all()
        for i in users:
            if i.name == input_name and i.email == input_email and i.password == input_password:
                user_info["i"] = i.id
                user_info["n"] = i.name
                user_info["e"] = i.email
                user_info["p"] = i.password
                context["registered"] = True
                return True
        context["validation_and_success"] = "کاربری با این اطلاعات یافت نشد"
        return False
repos = repository


# website home page
def images_show_view(request):
    if context["chosen_category"] == "" :
        context["images"] = Image.objects.all()
    if request.method == 'POST':
        search = request.POST["search"]
        if search != "" :
            context["images"] = Image.objects.filter(name__icontains=str(search))
            context["chosen_category"] = ""
            return render(request, "gallery.html", context)
        else:
            context["images"] = Image.objects.all()
            context["chosen_category"] = ""
            return render(request, "gallery.html", context)
    else:
        context["chosen_category"] = ""
        return render(request, "gallery.html", context)


# choosing category for showing images
def images_category_show(request, c):
    for english_category in Image.categories:
        if english_category[1] == c:
            context["chosen_category"] = english_category[0]
            context["images"] = Image.objects.filter(Image_category=context["chosen_category"])
            return HttpResponseRedirect("/gallery")


# clicking an image for showing it in a specific page
def image_click(request, id):
    chosen_image = Image.objects.filter(Image_id=id).first()
    context["images"] = Image.objects.filter(Image_category=chosen_image.Image_category)
    context["chosen_image"] = chosen_image
    return render(request, "image_click.html", context)


# downloading the selected image
def image_download(request, id):
    image = Image.objects.get(Image_id=id)
    response = HttpResponse(image.img, content_type='image/jpeg')
    response["Content-Disposition"] = 'attachment;filename="StarGallery.jpg"'
    return response



# website gallery image upload form
def gallery_form(request):
    # check if user has registered
    if context["registered"]:
        # if user click on submit button
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            # if information is valid
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.image_owner_id = user_info["i"]
                form_instance.save()
                context["validation_and_success"] = "عکس با موفقیت آپلود شد"
                return render(request, "gallery_form.html", context)
            else:
                context["validation_and_success"] = "اطلاعات وارد شده معتبر نیست!"
                return render(request, "gallery_form.html", context)
        # if user has just entered the page
        else:
            context["validation_and_success"] = ""
            return render(request, "gallery_form.html", context)
    else:
        return HttpResponseRedirect("/signup_form")




# login page
def user_logIn(request):
    context["validation_and_success"] = ""
    if request.method == 'POST':
        i = repos.log_in(repository, request.POST["name"], request.POST["email"], request.POST["password"])
        if i:
            return HttpResponseRedirect("/user_page")
        else:
            return render(request, "user_login.html", context)
    else:
        return render(request, "user_login.html", context)



#sign up page
def user_signUp(request):
    context["validation_and_success"] = ""
    if request.method == 'POST':
        i = repos.create(repository, request.POST["name"], request.POST["email"], request.POST["password"])
        if i:
            context["validation_and_success"] = ""
            return HttpResponseRedirect("/user_page")
        else:
            return render(request, "user_signup.html", context)
    else:
        return render(request, "user_signup.html", context)




# user personal page
def user_page(request):
    if context["registered"]:
        context["images"] = Image.objects.filter(image_owner_id=user_info["i"])
        return render(request, "user_page.html", context)
    else:
        return HttpResponseRedirect("/signup_form")


# user log out
def user_logout(request):
    if context["registered"]:
        user_info["i"] = 0
        user_info["n"] = ""
        user_info["e"] = ""
        user_info["p"] = ""
        context["registered"] = False
        return render(request, "user_logout.html", context)
    else:
        return HttpResponseRedirect("/signup_form")





