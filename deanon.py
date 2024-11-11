import requests
import json
import socket
from datetime import datetime

def get_my_ip():
    """
    Получает текущий IP адрес пользователя, используя несколько сервисов
    """
    services = [
        'https://api.ipify.org?format=json',
        'https://api.myip.com',
        'https://ipinfo.io/json',
        'https://api.ip.sb/jsonip'
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('ip') or data.get('query')
        except:
            continue
    return None

def get_detailed_ip_info(ip_address):
    """
    Получает расширенную информацию об IP адресе, комбинируя несколько API
    """
    try:
        # Получаем базовую информацию от ipapi
        ipapi_response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        ipapi_data = ipapi_response.json() if ipapi_response.status_code == 200 else {}
        
        # Получаем дополнительную информацию от ipinfo
        ipinfo_response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        ipinfo_data = ipinfo_response.json() if ipinfo_response.status_code == 200 else {}
        
        # Комбинируем данные из обоих источников
        return {
            'ip': ip_address,
            'город': ipapi_data.get('city') or ipinfo_data.get('city'),
            'регион': ipapi_data.get('region') or ipinfo_data.get('region'),
            'страна': ipapi_data.get('country_name') or ipinfo_data.get('country'),
            'провайдер': ipapi_data.get('org') or ipinfo_data.get('org'),
            'широта': ipapi_data.get('latitude') or (ipinfo_data.get('loc', ',').split(',')[0] if 'loc' in ipinfo_data else None),
            'долгота': ipapi_data.get('longitude') or (ipinfo_data.get('loc', ',').split(',')[1] if 'loc' in ipinfo_data else None),
            'часовой пояс': ipapi_data.get('timezone') or ipinfo_data.get('timezone'),
            'почтовый индекс': ipapi_data.get('postal') or ipinfo_data.get('postal'),
            'точность геолокации': 'средняя (город/район)',
            'AS номер': ipapi_data.get('asn') or ipinfo_data.get('asn'),
            'хостинг': ipinfo_data.get('hosting', 'Нет данных')
        }
    except Exception as e:
        return f"Произошла ошибка при получении данных: {str(e)}"

def get_multiple_map_links(ip_address):
    """
    Генерирует несколько ссылок на разные карты для сравнения местоположения
    """
    try:
        ip_data = get_detailed_ip_info(ip_address)
        if isinstance(ip_data, dict):
            lat = ip_data.get('широта')
            lon = ip_data.get('долгота')
            if lat and lon:
                return {
                    'Google Maps': f"https://www.google.com/maps?q={lat},{lon}",
                    'OpenStreetMap': f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12",
                    'Yandex Maps': f"https://yandex.ru/maps/?ll={lon},{lat}&z=12"
                }
        return None
    except:
        return None

def print_ip_info(ip_address):
    """
    Выводит расширенную информацию об IP адресе
    """
    info = get_detailed_ip_info(ip_address)
    if isinstance(info, dict):
        print("\n=== Подробная информация об IP адресе ===")
        print("⚠️ Примечание: геолокация по IP адресу даёт приблизительные результаты")
        print("   и обычно определяет город/район, а не точный адрес.")
        print("\nОсновная информация:")
        for key, value in info.items():
            if value:
                print(f"{key}: {value}")
        
        print("\nСсылки на карты для сравнения:")
        map_urls = get_multiple_map_links(ip_address)
        if map_urls:
            for service, url in map_urls.items():
                print(f"{service}: {url}")
        
        if info.get('хостинг') == 'true':
            print("\n⚠️ Внимание: Этот IP принадлежит хостинг-провайдеру")
            print("   и может использоваться для VPN/прокси.")
    else:
        print(info)

def main():
    """
    Основная функция для взаимодействия с пользователем
    """
    while True:
        print("\n=== IP Геолокация ===")
        print("1. Показать информацию о моем IP")
        print("2. Ввести другой IP адрес")
        print("3. Выход")
        
        choice = input("\nВыберите действие (1-3): ")
        
        if choice == "1":
            my_ip = get_my_ip()
            if my_ip:
                print(f"\nВаш IP адрес: {my_ip}")
                print_ip_info(my_ip)
            else:
                print("\nНе удалось определить ваш IP адрес")
        elif choice == "2":
            ip = input("\nВведите IP адрес (например, 8.8.8.8): ")
            print_ip_info(ip)
        elif choice == "3":
            print("\nПрограмма завершена.")
            break
        else:
            print("\nНеверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()



