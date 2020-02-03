import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from user.forms import LoginForm, RegForm

def get_days_hot_blogs(days):
    today = timezone.now().date()
    date = today-datetime.timedelta(days=days)
    blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gte=date).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 缓存
    week_hot_blogs = cache.get('week_hot_blogs')
    if week_hot_blogs is None:
        week_hot_blogs = get_days_hot_blogs(7)
        cache.set('week_hot_blogs', week_hot_blogs, 60)

    month_hot_blogs = cache.get('month_hot_blogs')
    if month_hot_blogs is None:
        month_hot_blogs = get_days_hot_blogs(30)
        cache.set('month_hot_blogs', month_hot_blogs, 60)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['week_hot_blogs'] = week_hot_blogs
    context['month_hot_blogs'] = month_hot_blogs
    return render(request, 'home.html', context)
