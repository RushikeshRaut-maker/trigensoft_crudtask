from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,Group,UserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUserManager(UserManager):

	def __create_user(self, email, password, **extra_fields):
		user=self.model(email=email,**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_admin(self,email=None,password=None,**extra_fields):
		extra_fields.setdefault('is_staff',False)
		extra_fields.setdefault('is_active',False)
		extra_fields.setdefault('is_superuser',False)
		return self.__create_user(email, password, **extra_fields)

	def create_superuser(self,email,password,**extra_fields):
		extra_fields.setdefault('is_staff',True)
		extra_fields.setdefault('is_active',True)
		extra_fields.setdefault('is_superuser',True)
		group,created=Group.objects.get_or_create(name='Superadmin')
		extra_fields.setdefault('role_id',group.id)
		return self.__create_user(email, password, **extra_fields)


class UserPermissionMixin(PermissionsMixin):
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False,
                                       help_text=(
                                           'Designates that this user has all permissions without '
                                           'explicitly assigning them.'))

    groups = None
    user_permissions = None
    is_staff = False

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        pass

    def get_all_permissions(self, obj=None):
        pass




class Users(AbstractBaseUser,UserPermissionMixin):

	role=models.ForeignKey(Group, on_delete=models.CASCADE,null=True,blank=True)

	first_name = models.CharField(_('first name'), max_length=256, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=256, blank=True, null=True)
	email=models.EmailField(unique=True)
	is_active=models.BooleanField(default=True)
	is_staff=models.BooleanField(default=True)
	is_deleted=models.BooleanField(default=False)
	objects=CustomUserManager()

	def __str__(self):
		return str(self.pk)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELD =[]

	
	class Meta:
	    db_table ='user'
	    verbose_name = _('user')
	    verbose_name_plural = _('users')

	def get_full_name(self):
	    """
	    Returns the first_name plus the last_name, with a space in between.
	    """
	    full_name = '%s %s' % (self.first_name, self.last_name)
	    return full_name.strip()

	def get_short_name(self):
	    """
	    Returns the short name for the user.
	    """
	    return self.first_name



class Course(models.Model):

	course_name =models.CharField(max_length=256,null=True,blank=True)
	course_duration =models.CharField(max_length=256,null=True,blank=True)
	course_fees =models.IntegerField()
	Status_choise=(('active','active'),('deactive','deactive'),('deleted','deleted'))
	course_status =models.CharField(choices=Status_choise,max_length=20,default='active')

	is_deleted =models.BooleanField(default=False)



	class Meta:
		db_table='course'

	def __str__(self):
		return  str(self.course_name)


class Student(models.Model):

	first_name=models.CharField(max_length=256,null=True,blank=True)
	last_name=models.CharField(max_length=256,null=True,blank=True)
	address =models.CharField(max_length=256,null=True,blank=True)
	mobile =models.CharField(max_length=10,null=True,blank=True)

	course_fees =models.IntegerField()
	Status_choise=(('active','active'),('deactive','deactive'),('deleted','deleted'))
	course_status =models.CharField(choices=Status_choise,max_length=20,default='active')

	course_taken=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)


	class Meta:
		db_table ='student'

	def __str__(self):
		return  str(self.pk)


class UserAccess(models.Model):

	user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True)

	is_access = models.BooleanField(default=False)
	course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)

	class Meta:
		db_table ='user_access'

	def __str__(self):
		return str(self.pk)


	