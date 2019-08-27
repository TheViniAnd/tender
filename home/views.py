import os
from django.shortcuts import render, get_object_or_404
from .models import Post, GoTender, BuyTender
from django.utils import timezone
from .forms import PostForm, CashForm, BuyForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .forms import MyUserCreationForm

class RegisterFormView(FormView):
    form_class = MyUserCreationForm
    success_url = "/login/"
    template_name = "auth/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def home_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'home.html',{'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    cash = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    #if request.user.is_authenticated:
    path = str(post.pk) + '.pdf'
    pats = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pas = pats + "/media/docs/" + path
    canvas = Canvas(pas, pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    canvas.setFont('FreeSans', 12)
    author_text = 'Автор: ' + str(post.author)
    title_text = str(post.title)
    opis_text = 'Описание: ' + str(post.text)
    city_p_text = 'Место поставки: ' + 'г. '+str(post.supply)
    reg_text = 'Регион закупки: ' + str(post.region)
    cost_text = 'Стоимость: ' + str(post.cost) + ' руб.'
    start_text = 'Дата размещения: ' + str(post.start)
    end_text = 'Окончание приёма предложений: ' + str(post.ending)
    comp_text = 'Компания: ' + str(post.compania)
    inn_text = 'Инн: ' + str(post.inn)
    kpp_text = 'Кпп: ' + str(post.kpp)
    phone_text = 'Телефон: ' + str(post.phone)
    number_text = '№' + str(post.pk)
    canvas.drawString(10, 820, number_text)
    canvas.drawString(10, 800, author_text)
    canvas.drawString(100, 770, title_text)
    canvas.drawString(10, 730, opis_text)
    canvas.drawString(10, 680, city_p_text)
    canvas.drawString(10, 660, reg_text)
    canvas.drawString(10, 620, cost_text)
    canvas.drawString(10, 580, start_text)
    canvas.drawString(10, 560, end_text)

    canvas.drawString(10, 520, comp_text)
    canvas.drawString(10, 500, inn_text)
    canvas.drawString(10, 480, kpp_text)
    canvas.drawString(10, 460, phone_text)
    canvas.showPage()
    canvas.save()


    return render(request, 'detail.html',{'post': post, 'cash':cash, 'path':path})

def cash_tender(request):
    cash = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'cash.html', {'cahs':cash})

def view_tender(request):
    cash = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    buy = BuyTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'tender_accaount.html', {'cahs': cash, 'post':post, 'buy':buy})

@login_required
def account(request):

    if request.user.is_authenticated:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        cash = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        buys = BuyTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        if request.method == "POST":
            buy = BuyForm(request.POST)
            if buy.is_valid():
                postss = buy.save(commit=False)
                postss.author = request.user
                #tenders = Post.objects.get(title = Post.title)
                #posts.tenders = tenders
                #client = BuyTender.objects.get(client=buyp.client)
                #print(client)
                postss.published_date = timezone.now()
                postss.save()
                return redirect('/')
        else:
            buy = BuyForm()

        return render(request, 'account.html', {'posts': posts, 'cash': cash, 'buy': buy, 'buys':buys})

def user_buy_tender(request,pk):
    if request.user.is_authenticated:
        cas = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        cash = get_object_or_404(GoTender, pk = pk)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        #post = get_object_or_404(Post, pk=pk)
        #print('post = ', post.title)
        if request.method == "POST":
            cashss = BuyForm(request.POST)
            if cashss.is_valid():
                pos = cashss.save(commit=False)
                pos.author = request.user
                tenders = GoTender.objects.get(tenders=cash.tenders, pk=pk)
                client = GoTender.objects.get(author=cash.author, pk=pk)
                pos.tenders = tenders.tenders
                pos.client = client.author

                pos.published_date = timezone.now()
                pos.save()
                return HttpResponseRedirect('/')
                #return redirect('post_detail', pk=post.pk)
        else:
            cashss = BuyForm()
        return render(request, 'user_buy.html', {'cashss': cashss,  'cash':cash, 'posts':posts, 'cas':cas})

def buy_ok(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            buy = BuyForm(request.POST)
            if buy.is_valid():
                posts = buy.save(commit=False)
                posts.author = request.user
                posts.save()
                return HttpResponseRedirect('/')
            else:
                print('wto')
        else:
            print('one')
            buy = BuyForm()
        return render(request, 'home.html', {'buy':buy})

def cash_new(request, pk, **kwargs):
    if request.user.is_authenticated:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        post = get_object_or_404(Post, pk=pk)
        cash = GoTender.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        if request.method == "POST":
            cashs = CashForm(request.POST)
            if cashs.is_valid():
                posti = cashs.save(commit=False)
                posti.author = request.user
                tenders = Post.objects.get(title = post.title)
                posti.tenders = tenders
                posti.published_date = timezone.now()
                posti.save()
                return redirect('post_detail', pk=post.pk)
        else:
            cashs = CashForm()
        return render(request, 'cash.html', {'cashs': cashs, 'post':post, 'cash':cash, 'posts':posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            if request.FILES['nameFile'] is not None:
                handle_uploaded_file(request.FILES['nameFile'])
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            print('error')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form':form})

def handle_uploaded_file(file_path):
    dest = open("media/"+file_path.name,"wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()

