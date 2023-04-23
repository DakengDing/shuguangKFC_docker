from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRenwu
from .route import Route
import json
from django.contrib.auth.models import User
from .models import Renwu,Juntuan
from django.conf.urls.static import static
from .esi import Esi



def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "已登录")
            return redirect('home')
        else:
            messages.success(request, "用户名或密码错误")
            return redirect('home')
    return render(request, 'home.html', {})


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
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def dao_hang(request):
    route_list= None
    if request.method == 'GET':
        # Get form data
        from_system = request.GET.get('from')
        to_system = request.GET.get('to')
        ship_type = request.GET.get('ship')


        if ship_type == "Black OP":
            maxRange = 8
        elif ship_type == 'Jump Freighters':
            maxRange = 10
        elif ship_type == "Jump Gate":
            maxRange = 5
        else:
            maxRange = 7;

        graph_file = open('graph.json', 'r',encoding='utf8')
        graph = json.load(graph_file)
        graph_file.close()
        Route.graph = graph

        # print(graph[0]["security"])

        # print(maxRange)

        if from_system is not None and to_system is not None:
            systemFrom = from_system.upper()
            systemFromNoSpace = systemFrom.replace(" ","")
            systemTo = to_system.upper()
            systemToNoSpace = systemTo.replace(" ","")
            sysFrom = Route.find_system(systemFromNoSpace)
            sysTo = Route.find_system(systemToNoSpace)
            route_list = Route.calculate_route(sysFrom,sysTo,maxRange)
            if len(route_list) == 0:
                print("No route found.")

    return render(request,'daohang.html',{"route_list":route_list})


def add_renwu(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            id = request.POST.get('id')
            if Renwu.objects.filter(name = id).exists():
                messages.success(request, "角色已绑定")
                return render(request, 'add_renwu.html', {})
            else:
                info = Esi.get_ids(character_names=id)
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
        #juntuan = Juntuan.objects.get(juntuan_id = yiBangDing.juntuan_id)
        #print(yiBangDing[0].juntuan_id)
        #record = {'name':yiBangDing.name,'juntuan':juntuan.name}
        renwu_dict = []
        for renwu in yiBangDing:
            juntuan_name = Juntuan.objects.get(juntuan_id = renwu.juntuan_id).name
            #alliance = Juntuan.objects.get(juntuan_id = renwu.juntuan_id).alliance
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

    return render(request,'dengjijiandui.html',{})