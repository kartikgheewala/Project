from django.shortcuts import render, redirect
from testapp.models import Registration, Registration_OTP, Chatting
from django.contrib import messages
import re
import random
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
MOBILE_NO_REGEX = re.compile(r"^[56789]{1}\d{9}$")

# Create your views here.

def Index(request):
      return render(request, 'Login.html')

def Reg_View(request):
      return render(request, 'Reg.html')

def Registration_View(request):

      #make sure all data is valid
      #create record in data base (Registration)
      #store user_id in session to show login status


      password = ''
      error = False
      Profile_Photo = request.FILES['upload']

      if(len(request.POST['txt_firstname']) < 2):
            messages.error(request, "First Name must be 2 or more character")
            error = True

      elif(len(request.POST['txt_lastname']) < 2):
            messages.error(request, "Last Name must be 2 or more character")
            error = True

      elif not (request.POST['txt_firstname'].isalpha()):
            messages.error(request, "First Name must be alphabetical character")
            error = True

      elif not (request.POST['txt_lastname'].isalpha()):
            messages.error(request, "Last Name must be alphabetical character")
            error = True

      elif not (EMAIL_REGEX.match(request.POST['txt_email'])):
            messages.error(request, "Email is invalid")
            error = True

      elif not (MOBILE_NO_REGEX.match(request.POST['txt_mobno'])):
            messages.error(request, "Mobile no should be 10 digits !")
            error = True

      elif Profile_Photo.size > 4000000:
            messages.error(request, 'Image Size Must Lessthan 3mb.')
            error = True


      elif not (Profile_Photo.content_type == 'image/jpeg' or
                Profile_Photo.content_type == 'image/jpg' or
                Profile_Photo.content_type == 'image/png'):
            messages.error(request, 'File must be select a (.jpeg|.jpg|.png) File.')
            error = True

      elif(len(request.POST['txt_password']) < 5):
            messages.error(request, "password is too short !")
            error = True

      elif(request.POST['txt_password'] != request.POST['txt_conpassword']):
            messages.error(request, "Password or Con-Password must be same !")
            error = True

      elif(Registration.objects.filter(Email=request.POST['txt_email']).exists()):
            messages.error(request, "Email already taken !")
            error = True

      if(error):
            return redirect('/Reg')

      else:
            pwd = request.POST['txt_password']

            for i in range(0, len(pwd)):
                  password = password + chr(ord(pwd[i]) - 2)

            # qry = File_Upload(Image=upload_file.name)
            # qry.save()
            # fs = FileSystemStorage('media/image/')
            # fs.save(upload_file.name, upload_file)

            qry_registration = Registration(FirstName=request.POST['txt_firstname'],
                                LastName=request.POST['txt_lastname'],
                                Email=request.POST['txt_email'],
                                MobileNo=request.POST['txt_mobno'],
                                Profile_Photo=Profile_Photo.name,
                                Password=password)
            qry_registration.save()

            # ******************************** Photo save a Profile_Photos in media directory ---START--- **************************************
            FS = FileSystemStorage('media/Profile_Photos/')
            FS.save(Profile_Photo.name, Profile_Photo)
            # ******************************** Photo save a Profile_Photos in media directory ---END--- **************************************

            # ******************************** OTP send at EMAIL ---START--- **************************************
            email = request.POST['txt_email']
            Generate_OTP = str(random.randint(100000, 999999))

            qry_otp = Registration_OTP(otp=Generate_OTP,
                                       Email=request.POST['txt_email'])          # Generate_OTP will be going to database
            qry_otp.save()                                                       # Generate_OTP will be save in database

            Subject = "Registration OTP"
            Main_Text = "Your Registration OTP is " + Generate_OTP
            From_mail = settings.EMAIL_HOST_USER
            To_mail = [email]
            send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
            # ******************************** OTP send at EMAIL ----OVER--- ***************************************

            return redirect('/OTP')



def Reg_OTP(request):
      return render(request, 'Reg_OTP.html')

def Conform_OTP(request):

      OTP_REGEX = re.compile(r"^\d{6}$")
      error = False

      if not (OTP_REGEX.match(request.POST['txt_otp'])):
            messages.error(request, "OTP must be six digits")
            error = True

      if(error):
            return redirect('/OTP')

      else:
            qry_otp = Registration_OTP.objects.filter(otp=request.POST['txt_otp'])
            if not qry_otp:
                  messages.error(request, "Incorrect OTP !")
                  return redirect('/OTP')
            else:
                  u = Registration_OTP.objects.all()
                  u.delete()
                  return redirect('/')



def Login(request):

      try:
            check_password = ''
            error = False
            get_password = request.POST['txt_password']

            for i in range(0, len(get_password)):
                  check_password = check_password + chr(ord(get_password[i]) - 2)

            qry_user_login = Registration.objects.get(Email=request.POST['txt_email'])

            request.session['user_id'] = qry_user_login.Registration_ID
            request.session['user_name'] = qry_user_login.FirstName

            if qry_user_login.Password != check_password:
                  messages.error(request, "Password is Incorrect !")
                  error = True

            # jaba = request.POST.getlist('ckb_remember-me')
            #
            # if 'checked' in jaba:
            #       pass



      except (Registration.DoesNotExist):
            messages.error(request, "Email is Incorrect !")
            error = True

      if error:
            return redirect('/')
      else:
            return redirect('/Home')


      # id = request.session['user_id']
      # request.session['user_id'] = id
      #
      # request.session['user_id'] = qry_registration.Registration_ID


      #******************* Done without Encrypt *************************************************
      # eml = request.POST['login_email']
      # ps = request.POST['login_password']
      # print("----------------------------------------------------------", eml)
      # print("----------------------------------------------------------", ps)
      #
      # user = Registration.objects.filter(Email=eml, Password=ps)
      #
      # print("------This is user------", user)
      # if not user:
      #       messages.error(request, "Incorrect email or password !")
      #       return redirect('/')
      # else:
      #       id = request.session['user_id']
      #       print('------------------------------------------', id)
      #       request.session['user_id'] = id
      #       # login(request, user)
      #       return redirect('/Success')
      #****************** Done over *************************************************************

def Home(request):

      if not 'user_id' in request.session:
            return redirect('/')
      else:
            qry_reg = Registration.objects.all()
            qry_foreign = Chatting.objects.all().order_by('-Chatting_Id')
            context = {
                  'User_Name': request.session['user_name'],
                  'User_Id': request.session['user_id'],
                  'qry_foreign': qry_foreign,
                  'qry_reg': qry_reg,

            }
            return render(request, 'Home.html', context)

def Profile(request):
      if not 'user_id' in request.session:
            return redirect('/')
      else:
            qry_info = Registration.objects.all()
            context = {
                  'User_Id': request.session['user_id'],
                  'qry_info': qry_info,

            }
            return render(request, 'Profile.html', context)

def Update_Profile(request,id):
      error = False

      if not 'user_id' in request.session:
            return redirect('/')
      else:
            if (len(request.POST['txt_firstname']) < 2):
                  messages.error(request, "First Name must be 2 or more character")
                  error = True

            elif(len(request.POST['txt_lastname']) < 2):
                  messages.error(request, "Last Name must be 2 or more character")
                  error = True

            elif not (request.POST['txt_firstname'].isalpha()):
                  messages.error(request, "First Name must be alphabetical character")
                  error = True

            elif not (request.POST['txt_lastname'].isalpha()):
                  messages.error(request, "Last Name must be alphabetical character")
                  error = True

            elif not (MOBILE_NO_REGEX.match(request.POST['txt_mobileno'])):
                  messages.error(request, "Mobile no should be 10 digits !")
                  error = True

            if (error):
                  return redirect('/Profile')
            else:
                  qry_update_info = Registration.objects.get(Registration_ID=id)
                  qry_update_info.FirstName = request.POST['txt_firstname']
                  qry_update_info.LastName = request.POST['txt_lastname']
                  qry_update_info.MobileNo = request.POST['txt_mobileno']
                  qry_update_info.Updated_Date = datetime.datetime.now()
                  qry_update_info.save()

                  return redirect('/Profile')

def Update_Image(request,id):
      error = False
      Update_Photo = request.FILES['upload']

      if not 'user_id' in request.session:
            return redirect('/')
      else:
            if Update_Photo.size > 4000000:
                  messages.error(request, 'Image Size Must Lessthan 3mb.')
                  error = True


            elif not (Update_Photo.content_type == 'image/jpeg' or
                      Update_Photo.content_type == 'image/jpg' or
                      Update_Photo.content_type == 'image/png'):
                  messages.error(request, 'File must be select a (.jpeg|.jpg|.png) File.')
                  error = True

            if (error):
                  return redirect('/Profile')
            else:
                  qry_update_info = Registration.objects.get(Registration_ID=id)
                  qry_update_info.Profile_Photo = Update_Photo.name
                  qry_update_info.Updated_Date = datetime.datetime.now()
                  qry_update_info.save()

                  # ******************************** Photo save a Profile_Photos in media directory ---START--- **************************************
                  FS = FileSystemStorage('media/Profile_Photos/')
                  FS.save(Update_Photo.name, Update_Photo)
                  # ******************************** Photo save a Profile_Photos in media directory ---END--- **************************************

                  return redirect('/Profile')

def Send_Message(request):
      if not 'user_id' in request.session:
            return redirect('/')
      else:
            error = False

            if request.POST['txt_message'] == "":
                  messages.error(request, "Type some message")
                  error = True

            if error:
                  return redirect('/Home')
            else:
                  qry_message = Chatting(Registration_Id_id=request.session['user_id'], Message=request.POST['txt_message'], Created_Date=datetime.datetime.now())
                  qry_message.save()
                  return redirect('/Home')

def Logout(request):
      if not 'user_id' in request.session:
            return redirect('/')
      else:
            request.session.flush()
            return redirect('/')
