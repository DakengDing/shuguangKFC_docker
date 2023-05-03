from datetime import datetime

from django.db.models import Sum, Count, Q, OuterRef, Subquery
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRenwu
from .route import Route
import json
from django.contrib.auth.models import User
from .models import Renwu,Juntuan,Jiandui,Fc
from django.conf.urls.static import static
from .esi import Esi
from .trans import Trans
from django.contrib.auth.decorators import login_required
from .signals import add_user_fc



def home(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "已登录")
            return redirect('my_jiandui')
        else:
            messages.success(request, "用户名或密码错误")
            return redirect('home')
    return render(request, 'home.html', {})


@login_required(login_url='home')
def my_chuqin(request):
    user_name = request.user.username
    user_id = User.objects.get(username = user_name)
    game_names = list(Renwu.objects.filter(user_name_id=user_id).values_list('name',flat=True))
    jiandui_dict = []


    for user_name in game_names:
        
        user_jiandui_queryset = Jiandui.objects.filter(member__has_key=user_name)
        if user_jiandui_queryset.exists():

            user_jiandui_queryset = Jiandui.objects.filter(member__has_key=user_name)

            # user_jianduis = Jiandui.objects.get(member__has_key = user_name)
            for user_jiandui in user_jiandui_queryset:
                info = {}
                info['game_id'] = user_name
                info['jiandui_id'] = user_jiandui.jiandui_id
                info['time'] = user_jiandui.timeCreate
                info['spr'] = user_jiandui.spr
                jiandui_dict.append(info)

    return render(request, 'my_jiandui.html', {'user_jianduis':jiandui_dict})

def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, "已登出")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            login(request, user)
            messages.success(request, "注册成功")

            user_ins = User.objects.get(username=username)
            try:
                fc = Fc.objects.get(user_name=user_ins)
                fc.fc = False
                fc.save()
            except Fc.DoesNotExist:
                fc = Fc.objects.create(user_name=user_ins, fc=False)
                fc.save()
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def dao_hang(request):
    route_list, time, total_fuel = [], 0, 0
    if request.method == 'GET':
        # Get form data
        from_system = request.GET.get('from')
        to_system = request.GET.get('to')
        ship_type = request.GET.get('ship')





        graph_file = open('graph.json', 'r',encoding='utf8')
        graph = json.load(graph_file)
        graph_file.close()
        Route.graph = graph

        if from_system is not None and to_system is not None:
            systemFrom = from_system.upper()
            systemFromNoSpace = systemFrom.replace(" ","")
            systemTo = to_system.upper()
            systemToNoSpace = systemTo.replace(" ","")
            sysFrom = Route.find_system(systemFromNoSpace)
            sysTo = Route.find_system(systemToNoSpace)
            route_list,total_fuel = Route.calculate_route(sysFrom,sysTo,ship_type)
            if len(route_list) == 0:
                print("No route found.")

    return render(request,'daohang.html',{"route_list":route_list,"total_fuel": total_fuel})


def add_renwu(request):
    if request.user.is_authenticated:
        user_name = request.user.username
        user_id = User.objects.get(username=user_name)
        if request.method =="POST":
            id = request.POST.get('id')
            if Renwu.objects.filter(name = id).exists():
                if Renwu.objects.get(name = id).user_name_id is None:
                    renwu = Renwu.objects.get(name = id)
                    renwu.user_name_id = user_id
                    renwu.save()
                    messages.success(request, "添加成功")

                else:
                    messages.success(request, "角色已被其他用户绑定")

                return render(request, 'add_renwu.html', {})
            else:
                info = Esi.get_ids(character_names=[id])
                if info is not None:
                    game_id = info[0].id
                    juntuan_id = info[0].corporation_id

                    if Juntuan.objects.filter(juntuan_id = juntuan_id).exists():
                        task = Renwu(game_id=game_id, name=id, point=0, juntuan_id=juntuan_id,
                                     user_name_id=request.user.id)
                        task.save()
                    else:
                        juntuan_task = Juntuan(juntuan_id=juntuan_id,name=info[0].corporation_name)
                        juntuan_task.save()
                        task = Renwu(game_id=game_id, name=id, point=0, juntuan_id=juntuan_id,
                                     user_name_id=request.user.id)
                        task.save()
                    messages.success(request,"添加成功")




            return render(request, 'add_renwu.html', {})
        else:
            return render(request, 'add_renwu.html', {})

    else:
        messages.success(request, "请登录你的账号")
        return redirect('home')


def renwu_record(request):
    if request.user.is_authenticated:
        #查询已绑定人物信息
        pk = request.user.id
        user = User.objects.get(id=pk)
        yiBangDing = user.renwu_set.all()

        renwu_dict = []
        for renwu in yiBangDing:
            juntuan_name = Juntuan.objects.get(juntuan_id = renwu.juntuan_id).name
            renwu_dict.append({
                "name":renwu.name,"juntuan":juntuan_name
            })
        return render(request,'renwu_bangding.html',{'yiBangDing':renwu_dict})



    else:
        messages.success(request,"请先登录！")
        return  redirect('home')


def add_jiandui(request):
    if request.user.is_authenticated:
        pk = request.user.id
        fc_ins = Fc.objects.get(user_name_id = pk)
        is_fc = fc_ins.fc
        if is_fc:
            jiandui_dict = {}
            if request.method =="POST":
                fcName = request.POST.get('id')
                if not Renwu.objects.filter(name=fcName).exists():

                    messages.success((request,"FC 名字输入有误"))
                    return render(request,'dengjijiandui.html',{})
                else:
                    text = request.POST.get('member')

                    members = Trans.parseFleet(text)

                    names = list(members.keys())

                    existing_names = Renwu.objects.filter(name__in=names).values_list('name', flat=True)
                    non_existing_names = list(set(names) - set(existing_names))
                    if len(non_existing_names) != 0:

                        res = Esi.get_ids(non_existing_names)
                        for character in res:
                            task = Renwu(game_id=character.id, name=character.name, point=0, juntuan_id=character.corporation_id)
                            task.save()

                    for name in names:
                        player = Renwu.objects.get(name=name)
                        player.point += 1
                        player.save()

                    fc_name_id = Renwu.objects.get(name=fcName).game_id
                    spr = False
                    if 'spr' in request.POST:
                        spr =True
                    jiandui = Jiandui(fc_name_id=fc_name_id,spr=spr, member = members)
                    jiandui.save()
                    messages.success(request,'舰队登记成功')
                    jiandui_id = jiandui.jiandui_id
                    jiandui_info = {}
                    jiandui_info['jiandui_id'] = jiandui_id
                    jiandui_info['FC'] = fcName
                    return render(request,'dengjijiandui.html',{'members':members,'jiandui_info':jiandui_info,'is_fc':is_fc})
            else:
                return render(request,'dengjijiandui.html',{'is_fc':is_fc})
    return render(request,'dengjijiandui.html',{})

def juntuan_scores(request):
    juntuans_to_exclude = ['高卧东山一片云','猫猫虫收割者','怪物猎人']
    juntuans = Juntuan.objects.exclude(name__in=juntuans_to_exclude).annotate(score = Sum('renwu__point')).order_by('-score')
    print(juntuans)

    return render(request, 'juntuan_scores.html', {'juntuans': juntuans})
# def juntuan_scores(request):
#     current_month = datetime.now().month
#     current_year = datetime.now().year
#
#     renwu_jiandui_count = Renwu.objects.filter(
#         jiandui__timeCreate__month=current_month,
#         jiandui__timeCreate__year=current_year,
#     ).annotate(
#         jiandui_count=Count("jiandui")
#     ).select_related("juntuan")
#
#     return render(request, "juntuan_scores.html", {"renwu_jiandui_count": renwu_jiandui_count})