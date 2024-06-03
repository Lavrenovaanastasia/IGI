from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.views import LoginView
import requests
from django.views.generic import *
from django.views import View
from django.contrib.auth.models import auth
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone
from datetime import datetime
from tzlocal import get_localzone
from django.forms import inlineformset_factory
import pytz
import requests
import logging


logging.basicConfig(level=logging.INFO, filename='logging.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s')

def home(request):
    user_timezone = get_localzone()

    current_date_utc = timezone.now()
    current_date_user_tz = current_date_utc.astimezone(user_timezone)
    latest_article = News.objects.latest('date')
    user_id = request.user.id
    is_staff = request.user.is_staff 
    is_super = request.user.is_superuser

    context = {
        'current_date_utc': current_date_utc.strftime('%d/%m/%Y %H:%M:%S'),
        'current_date_user_tz': current_date_user_tz.strftime('%d/%m/%Y %H:%M:%S'),
        'user_timezone': user_timezone.key,
        'latest_article': latest_article, 
        'user_id': user_id, 
        'is_staff': is_staff, 
        'is_super': is_super    
        }
    return render(request, 'home.html', context)

def about_company(request):
    user_id = request.user.id
    info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'company_info': info, 'user_id': user_id})

def news(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news': news})

def promocodes(request):
    promocodes = Promocode.objects.all()
    return render(request, 'promocodes.html', {'promocodes': promocodes})

def faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'faqs.html', {'faqs': faqs})

def contacts(request):
    contacts = Contact.objects.all()
    is_super = request.user.is_superuser
    return render(request, 'contacts.html', {'contacts': contacts, 'is_super': is_super})

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['description', 'user', 'photo']

class ContactCreateView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contacts_form.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            logging.info(f"Contact '{contact.user.username}' was created")
            return redirect('contacts')  # Замените 'department_info' на правильное имя вашего URL для страницы с информацией об отделениях
        return render(request, 'contacts_form.html', {'form': form})

class ContactUpdateView(View):

    def get(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        form = ContactForm(instance=contact)
        return render(request, 'contacts_form.html', {'form': form, 'contact': contact})

    def post(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            logging.info(f"Contact '{contact.user.username}' was updated")
            return redirect('contacts') 
        return render(request, 'contacts_form.html', {'form': form, 'contact': contact})


class ContactDeleteView(View):
    def post(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return redirect('contacts')  # Или замените 'cars' на правильный URL для списка медикаментов

def vacancies(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label='Оценка', min_value=1, max_value=5)
    class Meta:
        model = Review
        fields = ['title', 'rating','text']
        labels = {
            'title': 'Тема',
            'rating': 'Оценка',
            'text': 'Текст',
        }

class ReviewCreateView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated and request.user.status == 'client':
            
            logging.info(f"{request.user.username} called ReviewCreateView (status: {request.user.status}) | user's Timezone: {request.user.timezone}")

            form = ReviewForm()
            is_staff = request.user.is_staff 

            return render(request, 'review_create_form.html', {'form': form, 'is_staff': is_staff})
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == 'client':
            form = ReviewForm(request.POST)
            if form.is_valid():
                logging.info(f"ReviewForm has no errors)")

                title = form.cleaned_data['title']
                rating = form.cleaned_data['rating']
                text = form.cleaned_data['text']

                review = Review.objects.create(title=title, rating=rating, text=text, user=request.user)
                logging.info(f"Review '{review.title}' was created by {request.user.username} ")
                return redirect('reviews')
        logging.warning("User is not authenticated")
        return redirect('login')

class ReviewEditView(View):
    def get(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id)
        if request.user.is_authenticated and review.user == request.user:
            form = ReviewForm(instance=review)
            return render(request, 'review_edit.html', {'form': form, 'review': review})
        return redirect('login')

    def post(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id)
        if request.user.is_authenticated and review.user == request.user:
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews')
        return render(request, 'review_edit.html', {'form': form, 'review': review})

class ReviewDeleteView(View):
    def get(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id)
        if request.user.is_authenticated and review.user == request.user:
            review.delete()
        return redirect('reviews')

def privacy_policy(request):
    return render(request, 'privacy.html')



class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        
        fields = ['username', 'first_name', 'last_name', 'age', 'phone', 'address', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'age': 'Возраст',
            'phone': 'Телефон', 
            'address': 'Адрес',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }


class UserRegistrationView(CreateView):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logging.info("Registration form has no errors")
            user = form.save(commit=False)
            user.save()

            if request.user.is_authenticated:
                user.timezone = request.user.timezone
            else:
                user.timezone = get_localzone_name()
                        
            user.save()

            logging.info(f"{user.username} REGISTER (status: {user.status}) | user's Timezone: {user.timezone}")
            return redirect('login')
        else:
            logging.warning("Registration form is invalid")
            return render(request, 'registration.html', {'form': form})


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    def get_success_url(self):  
        logging.info("User LOGIN")
        return reverse_lazy('home')
            
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logging.info(f"{request.user.username} LOGOUT (status: {request.user.status}) | user's Timezone: {request.user.timezone}")
            auth.logout(request)
        return redirect('home')


class CarsListView(View):
    model = Cars
    #context_object_name = 'car_list'
    queryset = Cars.objects.all()
    

    def get(self, request, *args, **kwargs):
        no_results = False
        is_super = request.user.is_superuser

        min_cost = request.GET.get('min_cost')
        if not min_cost:
            min_cost = 0
        max_cost = request.GET.get('max_cost')
        if not max_cost:
            max_cost = 1000

        search_query = request.GET.get('search')

        
        pribors = self.filter_pribor(min_cost, max_cost)


        if search_query:
            pribors = pribors.filter(name__icontains=search_query)
            if not pribors:
                no_results = True
        else:
            pribors = self.filter_pribor(min_cost, max_cost)

        pribors = pribors.order_by('name')

        data_list = []
        for pribor in pribors:
            data_list.append({
                'id': pribor.id,
                'name': pribor.name,
                'cost': pribor.cost,
            })
        return render(request, "cars_list.html", {'cars': data_list, 'no_results': no_results, 'is_super': is_super})

    @staticmethod
    def filter_pribor(min=None, max=None):
        pribor = Cars.objects.all()

        filtered = None

        if min is not None and max is not None:
            filtered = pribor.filter(cost__gte=min, cost__lte=max)
        elif min is not None:
            filtered = pribor.filter(cost__gte=min)
        elif max is not None:
            filtered = pribor.filter(cost__lte=max)

        if filtered is not None:
            return filtered
        return pribor


class CarsDetailView(View):
    model = Cars

    def get(self, request, *args, **kwargs):
        
        pribor = get_object_or_404(Cars, pk=self.kwargs['pk'])
        departments = DepartmentCar.objects.filter(car=pribor)
        suppliers = pribor.suppliers
        is_staff = request.user.is_staff 
        is_super = request.user.is_superuser

        context = {
            'car': pribor,
            'departments': departments,
            'suppliers': suppliers,
            'is_staff': is_staff,
            'is_super': is_super,
        }
        return render(request, "car_detail.html", context)

class CarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['name', 'code', 'instructions', 'description', 'cost', 'photo', 'categories']  # Убираем 'suppliers'
        labels = {
            'name': 'Название',
            'code': 'Код',
            'instructions': 'Инструкция',
            'description': 'Описание',
            'cost': 'Стоимость',
            'photo': 'Фото',
            'categories': 'Категория',
        }

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['supplier']
        labels = {
            'supplier': 'Поставщик',
        }

class DepartmentCarForm(forms.ModelForm):
    class Meta:
        model = DepartmentCar
        fields = ['department', 'quantity']
        labels = {
            'department': 'Отделение',
            'quantity': 'Количество',
        }

DepartmentCarFormSet = inlineformset_factory(
    Cars, DepartmentCar, form=DepartmentCarForm, extra=1
)
class CarCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CarForm()
        supply_form = SupplyForm()
        department_car_formset = DepartmentCarFormSet()
        return render(request, 'car_form.html', {
            'form': form,
            'supply_form': supply_form,
            'department_car_formset': department_car_formset
        })

    def post(self, request, *args, **kwargs):
        form = CarForm(request.POST, request.FILES)
        supply_form = SupplyForm(request.POST)
        department_car_formset = DepartmentCarFormSet(request.POST)
        if form.is_valid() and supply_form.is_valid() and department_car_formset.is_valid():
            car = form.save(commit=False)
            supplier = supply_form.cleaned_data['supplier']
            car.suppliers = supplier  # Установить поставщика для лекарства
            car.save()
            supply = supply_form.save(commit=False)
            supply.car = car
            supply.save()
            department_car_formset.instance = car
            department_car_formset.save()
            return redirect('cars')  # Замените на правильное имя URL для списка лекарств
        return render(request, 'car_form.html', {
            'form': form,
            'supply_form': supply_form,
            'department_car_formset': department_car_formset
        })

class CarUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        car = get_object_or_404(Cars, pk=pk)
        form = CarForm(instance=car)
        supply = Supply.objects.filter(car=car).first()
        supply_form = SupplyForm(instance=supply)
        department_car_formset = DepartmentCarFormSet(instance=car)
        return render(request, 'car_form.html', {
            'form': form,
            'supply_form': supply_form,
            'department_car_formset': department_car_formset
        })

    def post(self, request, pk, *args, **kwargs):
        car = get_object_or_404(Cars, pk=pk)
        form = CarForm(request.POST, request.FILES, instance=car)
        supply = Supply.objects.filter(car=car).first()
        supply_form = SupplyForm(request.POST, instance=supply)
        department_car_formset = DepartmentCarFormSet(request.POST, instance=car)
        if form.is_valid() and supply_form.is_valid() and department_car_formset.is_valid():
            car = form.save(commit=False)
            supplier = supply_form.cleaned_data['supplier']
            car.suppliers = supplier  # Установить поставщика для лекарства
            car.save()
            supply_form.save()
            department_car_formset.save()
            return redirect('car_detail', pk=pk)  # Замените на правильное имя URL для деталей лекарства
        return render(request, 'car_form.html', {
            'form': form,
            'supply_form': supply_form,
            'department_car_formset': department_car_formset
        })

class CarDeleteView(View):
    def post(self, request, pk):
        car = get_object_or_404(Cars, pk=pk)
        car.delete()
        return redirect('cars')  # Или замените 'cars' на правильный URL для списка медикаментов
    
def privacy_policy(request):
    return render(request, 'privacy.html')

class CatigoriesListView(View):
    model = Categories

    def get(self, request, *args, **kwargs):
        type_med = Categories.objects.all()
        return render(request, "car_categories.html", {'categories': type_med})
    
class OrderForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    department = forms.ModelChoiceField(queryset=Department.objects.none(), empty_label="Выберете филиал")
    promocode = forms.CharField(max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        pribor_id = kwargs.pop('pribor_id', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if pribor_id:
            self.fields['department'].queryset = Department.objects.filter(departmentcar__car_id=pribor_id).distinct()

class OrderCreateView(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "client" and Cars.objects.filter(pk=pk).exists():
            logging.info(f"{request.user.username} called OrderCreateView | user's Timezone: {request.user.timezone}")
            pribor = Cars.objects.get(pk=pk)
            form = OrderForm(pribor_id=pk)  # передаем pribor_id в форму
            return render(request, 'order_create_form.html', {'form': form, 'pribor': pribor})
        
        logging.error(f"Call failed OrderCreateView")
        return HttpResponseNotFound('Страница не найдена')
    
    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "client":
            pribor = Cars.objects.get(pk=pk)
            form = OrderForm(request.POST, pribor_id=pk)  # передаем pribor_id в форму
            if form.is_valid():
                logging.info(f"OrderForm has no errors")

                amount = form.cleaned_data['amount']
                department = form.cleaned_data['department']
                code = form.cleaned_data['promocode']

                try:
                    department_car = DepartmentCar.objects.get(department_id=department.id, car_id=pribor.id)
                    quantity = department_car.quantity

                    if amount > quantity:
                        logging.warning(f"{amount} is greater than {quantity}")
                        return HttpResponse("Выберете другой филиал или ожидайте поставки деталей")
                    promocode = Promocode.objects.filter(code=code).first()

                    sale = Sale.objects.create(
                        user=request.user,
                        department=department,
                        car=pribor,
                        quantity=amount,
                        promocode=promocode,
                        price=pribor.cost * amount,
                        price_prom=pribor.cost * amount
                    ) 
                    department_car.quantity -= amount
                    department_car.save()

                    if promocode:
                        logging.info(f"Promocode {promocode.code} used by {request.user.username}")
                        sale.use_discount(promocode)

                    url = reverse('user_order', kwargs={"pk": sale.user_id, "jk": sale.id})
                    return redirect(url)
                
                except DepartmentCar.DoesNotExist:
                    logging.error(f"Car {pribor.id} does not exist in department {department.id}")
                    return render(request, 'order_create_form.html', {'form': form, 'pribor': pribor, 'error_message': 'Выберете другой филиал или ожидайте поставки деталей'})

            return render(request, 'order_create_form.html', {'form': form, 'pribor': pribor})

        elif request.user.is_authenticated and request.user.status == "staff":
            logging.error(f"{request.user.username} has status {request.user.status}")
            return HttpResponseNotFound("Только для клиентов")
        else:
            logging.error(f"User is not authenticated")
            return HttpResponse('Войдите в аккуант чтобы сделать заказ')


class UserOrderView(View):
    def get(self, request, pk, jk, *args, **kwargs):
        if request.user.is_authenticated and request.user.id==int(pk) and Sale.objects.filter(user_id=int(pk), id=int(jk)).exists():
            logging.info(f"{request.user.username} called SpecificOrderView | user's Timezone: {request.user.timezone}")

            order = Sale.objects.filter(user_id=pk, id=jk).first()

            return render(request, 'order_detail.html', {'order': order})
        return HttpResponseNotFound("Страница не найдена")

class UserOrdersListView(View):
    def get(self, request, pk, *args, **kwargs):

        if request.user.is_authenticated and request.user.id==int(pk):
            logging.info(f"{request.user.username} called UserOrderView | user's Timezone: {request.user.timezone}")
            order = Sale.objects.filter(user_id=pk)
            return render(request, "orders_list.html", {'orders': order})

        logging.error(f"Call failed UserOrderView")
        return HttpResponseNotFound("Страница не найдена")

class OrderCancelView(View):
    def post(self, request, pk, jk, *args, **kwargs):
        if request.user.is_authenticated and request.user.id == int(pk):
            sale = get_object_or_404(Sale, user_id=pk, id=jk)
            if not sale.is_canceled:
                sale.is_canceled = True
                sale.save()
                logging.info(f"Order '{sale.id}' was canceled by {request.user.username}")
                department_car = get_object_or_404(DepartmentCar, department=sale.department, car=sale.car)
                department_car.quantity += sale.quantity
                department_car.save()
            return redirect('user_order', pk=pk, jk=jk)
        return HttpResponseNotFound("Страница не найдена")


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['no', 'address', 'master', 'close', 'open']
        # labels = {
        #     'no', 'address', 'close', 'open'
        # }

class DepartmentDeleteView(View):
    def post(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return redirect('departments')  # Или замените 'cars' на правильный URL для списка 

class DepartmentCreateView(View):
    def get(self, request):
        form = DepartmentForm()
        return render(request, 'department_form.html', {'form': form})

    def post(self, request):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            logging.info(f"Department '{department.no}' was created")
            return redirect('departments')  # Замените 'department_info' на правильное имя вашего URL для страницы с информацией об отделениях
        return render(request, 'department_form.html', {'form': form})


class DepartmentUpdateView(View):
    def get(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(instance=department)
        return render(request, 'department_form.html', {'form': form, 'department': department})

    def post(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            logging.info(f"Department '{department.no}' was updated")
            return redirect('departments')  # Замените 'department_info' на правильное имя вашего URL для страницы с информацией об отделениях
        return render(request, 'department_form.html', {'form': form, 'department': department})
    

class DepartmentInfo(View):
    model = Department

    def get(self, request, *args, **kwargs):
        is_super = request.user.is_superuser

        if request.user.is_authenticated:
            logging.info(f"{request.user.username} called DepartmentInfo | user's Timezone: {request.user.timezone}")
            points = Department.objects.all()
            return render(request, "department_info.html", {'points': points, 'is_super': is_super})
        logging.error(f"Call failed DepartmentInfo")
        return HttpResponseNotFound('Страница не найдена')

class OrderListView(View):
    def get(self, request, *args, **kwargs):      
        if request.user.is_authenticated and request.user.status == "staff":

            logging.info(f"{request.user.username} called OrderListView (status: {request.user.status}) | user's Timezone: {request.user.timezone}")
            
            sales = Sale.objects.filter(is_canceled=False)      
            total_revenue = sum(sale.price_prom for sale in sales)

            revenue_by_department = {}
            for sale in sales:
                department_name = sale.department.no
                revenue_by_department[department_name] = revenue_by_department.get(department_name, 0) + sale.price
            return render(request, 
                        'staff_order.html', {
                        'sales': sales,
                        'total_revenue': total_revenue,
                        'revenue_by_department': revenue_by_department
                        })
            #return render(request, "staff_order.html", {'sales': sales})


        logging.error(f"{request.user.username} has status {request.user.status}") 
        return HttpResponseNotFound("Страница не найдена")
    
class SupplierListView(View):  
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.status == "staff":
            is_super = request.user.is_superuser

            logging.info(f"{request.user.username} called SupplierListView (status: {request.user.status}) | user's Timezone: {request.user.timezone}")
            suppliers = Supplier.objects.all().prefetch_related('supply__car')
            return render(request, "suppliers.html", {'suppliers': suppliers, 'is_super': is_super})
        logging.error(f"{request.user.username} tried to call SupplierListView (status: {request.user.status})")
        return HttpResponseNotFound("Только для персонала")    


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'phone']
        labels = {
            'name': 'Название',
            'address': 'Адрес',
            'phone': 'Телефон',
        }

class SupplierCreateView(View):
    def get(self, request):
        form = SupplierForm()
        return render(request, 'supplier_form.html', {'form': form})

    def post(self, request):
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            logging.info("Supplier was created")
            return redirect('suppliers')  
        return render(request, 'supplier_form.html', {'form': form})  

class SupplierUpdateView(View):
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        form = SupplierForm(instance=supplier)
        return render(request, 'supplier_form.html', {'form': form, 'supplier': supplier})

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            logging.info(f"Supplier '{supplier.name}' was updated")
            return redirect('suppliers')  
        return render(request, 'supplier_form.html', {'form': form, 'supplier': supplier})

class SupplierDeleteView(View):
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})
    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return redirect('suppliers')  # Или замените 'cars' на правильный URL для списка 

#API

class MedicalFactsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            url = 'https://api.nhtsa.gov/recalls/'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                
                
                facts = []
                if 'results' in data and data['results']:
                    for result in data['results']:
                        fact = result.get('description', '')
                        if fact:
                            facts.append(fact)
                return render(request, 'deteil_facts.html', {'facts': facts})
            else:
                return render(request, 'deteil_facts.html', {'error': 'Failed to fetch data from API'})
        return HttpResponseNotFound("Page not found")
        


