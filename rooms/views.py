from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Room, City, Ward, RoomImage
from .forms import RoomForm


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')


    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('dashboard')


        return render(
            request,
            'rooms/login.html',
            {
                'error_message':
                    'Tên đăng nhập hoặc mật khẩu không đúng.'
            }
        )


    return render(
        request,
        'rooms/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')


# =========================================================
# API: LẤY PHƯỜNG/XÃ/ĐẶC KHU THEO TỈNH/THÀNH PHỐ
# =========================================================

def get_wards(request):

    city_id = request.GET.get('city_id')

    wards = Ward.objects.filter(
        city_id=city_id
    ).order_by('name')

    data = [
        {
            'id': ward.id,
            'name': ward.name
        }
        for ward in wards
    ]

    return JsonResponse(data, safe=False)


# =========================================================
# DANH SÁCH PHÒNG
# =========================================================
@login_required
def room_list(request):

    rooms = Room.objects.all()

    city_id = request.GET.get('city')
    ward_id = request.GET.get('ward')

    max_price = request.GET.get('max_price')
    min_area = request.GET.get('min_area')
    address = request.GET.get('address')


    # =====================================================
    # LỌC THÀNH PHỐ
    # =====================================================

    if city_id:

        rooms = rooms.filter(
            city_id=city_id
        )


    # =====================================================
    # LỌC PHƯỜNG/XÃ/ĐẶC KHU
    # =====================================================

    if ward_id:

        rooms = rooms.filter(
            ward_id=ward_id
        )


    # =====================================================
    # GIÁ TỐI ĐA
    # =====================================================

    if max_price:

        try:

            rooms = rooms.filter(
                price__lte=max_price
            )

        except (ValueError, TypeError):

            pass


    # =====================================================
    # DIỆN TÍCH TỐI THIỂU
    # =====================================================

    if min_area:

        try:

            rooms = rooms.filter(
                area__gte=min_area
            )

        except (ValueError, TypeError):

            pass


    # =====================================================
    # TÌM ĐỊA CHỈ
    # =====================================================

    if address:

        rooms = rooms.filter(
            address__icontains=address
        )


    cities = City.objects.all().order_by('name')

    wards = Ward.objects.all().order_by('name')


    return render(
        request,
        'rooms/room_list.html',
        {
            'rooms': rooms,

            'cities': cities,

            'wards': wards,

            'selected_city': city_id,

            'selected_ward': ward_id,

            'max_price': max_price,

            'min_area': min_area,

            'address': address,
        }
    )


# =========================================================
# THÊM PHÒNG
# =========================================================
@login_required
def add_room(request):

    if request.method == 'POST':

        form = RoomForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            room = form.save()

            images = request.FILES.getlist('images')

            for image in images:

                RoomImage.objects.create(
                    room=room,
                    image=image
                )

            return redirect('room_list')

    else:

        form = RoomForm()


    return render(
        request,
        'rooms/add_room.html',
        {
            'form': form
        }
    )


# =========================================================
# SỬA PHÒNG
# =========================================================
@login_required
def edit_room(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )


    if request.method == 'POST':

        form = RoomForm(
            request.POST,
            request.FILES,
            instance=room
        )

        if form.is_valid():

            room = form.save()

            images = request.FILES.getlist('images')

            for image in images:

                RoomImage.objects.create(
                    room=room,
                    image=image
                )

            return redirect('room_list')

    else:

        form = RoomForm(
            instance=room
        )


    return render(
        request,
        'rooms/edit_room.html',
        {
            'form': form,
            'room': room
        }
    )

# =========================================================
# XÓA ẢNH PHỤ
# =========================================================
@login_required
def delete_room_image(request, room_id, image_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )

    room_image = get_object_or_404(
        RoomImage,
        id=image_id,
        room=room
    )

    if request.method == 'POST':

        room_image.delete()

        return JsonResponse({
            'success': True,
            'message': 'Đã xóa ảnh thành công.'
        })

    return JsonResponse({
        'success': False,
        'message': 'Phương thức không hợp lệ.'
    }, status=400)

# =========================================================
# XÓA PHÒNG
# =========================================================
@login_required
def delete_room(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )


    if request.method == 'POST':

        room.delete()

        return redirect('room_list')


    return render(
        request,
        'rooms/delete_room.html',
        {
            'room': room
        }
    )

# =========================================================
# CHI TIẾT PHÒNG
# =========================================================
@login_required
def room_detail(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )

    return render(
        request,
        'rooms/room_detail.html',
        {
            'room': room
        }
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    rooms = Room.objects.all()


    # =========================
    # THỐNG KÊ PHÒNG
    # =========================

    total_rooms = rooms.count()


    available_rooms = rooms.filter(
        status='available'
    ).count()


    rented_rooms = rooms.filter(
        status='rented'
    ).count()


    reserved_rooms = rooms.filter(
        status='reserved'
    ).count()


    # =========================
    # TỶ LỆ LẤP ĐẦY
    # =========================

    occupied_rooms = (
        rented_rooms +
        reserved_rooms
    )


    if total_rooms > 0:

        occupancy_rate = round(
            occupied_rooms /
            total_rooms *
            100,
            1
        )

    else:

        occupancy_rate = 0


    # =========================
    # PHÒNG MỚI
    # =========================

    recent_rooms = rooms.order_by(
        '-created_at'
    )[:5]


    # =========================
    # CONTEXT
    # =========================

    context = {

        'total_rooms':
            total_rooms,

        'available_rooms':
            available_rooms,

        'rented_rooms':
            rented_rooms,

        'reserved_rooms':
            reserved_rooms,

        'occupied_rooms':
            occupied_rooms,

        'occupancy_rate':
            occupancy_rate,

        'recent_rooms':
            recent_rooms,

    }


    return render(
        request,
        'rooms/dashboard.html',
        context
    )
