from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Домашняя страница"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodeCV - Резюме для разработчиков</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
            }
            .btn {
                display: inline-block;
                margin: 10px;
                padding: 15px 30px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: translateY(-5px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 CodeCV</h1>
            <p>Интерактивное резюме для разработчиков на Django</p>
            <p><strong>Проект успешно запущен!</strong></p>

            <div style="margin: 30px 0;">
                <a href="/admin/" class="btn">Админ-панель</a>
                <a href="/dashboard/" class="btn">Дашборд</a>
            </div>

            <div style="margin-top: 40px; background: rgba(0,0,0,0.2); padding: 20px; border-radius: 10px;">
                <h3>Доступные URL:</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="/admin/" style="color: white;">/admin/</a> - Админ-панель</li>
                    <li><a href="/dashboard/" style="color: white;">/dashboard/</a> - Личный кабинет</li>
                    <li><a href="/api/" style="color: white;">/api/</a> - API</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """)


def dashboard(request):
    """Пример дашборда"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Дашборд - CodeCV</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .header { background: #4CAF50; color: white; padding: 20px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Дашборд CodeCV</h1>
            <p>Здесь будет ваш личный кабинет</p>
        </div>
        <p><a href="/">← На главную</a></p>
    </body>
    </html>
    """)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path('', home, name='home'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
