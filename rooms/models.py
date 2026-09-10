from django.db import models


class City(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class District(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Ward(models.Model):

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        related_name='wards',
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    # THÊM FIELD MỚI
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wards'
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    ward_type = models.CharField(
        max_length=20,
        choices=[
            ('commune', 'Xã'),
            ('ward', 'Phường'),
            ('special', 'Đặc khu'),
        ],
        default='commune'
    )

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(
        max_length=200
    )

    address = models.CharField(
        max_length=300
    )

    # Đơn vị hành chính cấp tỉnh
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Đơn vị hành chính cấp xã
    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=12, decimal_places=0)
    area = models.FloatField()

    electricity_price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    water_price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    deposit = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    floor = models.IntegerField(default=1)

    max_people = models.IntegerField(default=1)

    has_wifi = models.BooleanField(default=False)
    has_air_conditioner = models.BooleanField(default=False)
    has_bed = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_refrigerator = models.BooleanField(default=False)
    has_wardrobe = models.BooleanField(default=False)
    has_table_chairs = models.BooleanField(default=False)

    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )

    STATUS_CHOICES = [
        ('available', 'Đang trống'),
        ('rented', 'Đã cho thuê'),
        ('reserved', 'Đang giữ chỗ'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            (
                'view_dashboard',
                'Can view dashboard'
            ),
        ]

    def __str__(self):
        return self.name

class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='rooms/gallery/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.room.name} - {self.id}"