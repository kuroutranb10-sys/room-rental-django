import json
from pathlib import Path

from django.core.management.base import BaseCommand

from rooms.models import City, Ward


class Command(BaseCommand):

    help = 'Import dữ liệu tỉnh/thành phố và phường/xã từ JSON'

    def handle(self, *args, **options):

        # =====================================================
        # ĐƯỜNG DẪN ĐẾN administrative_units.json
        # =====================================================

        json_path = (
            Path(__file__).resolve().parents[2]
            / 'templates'
            / 'data'
            / 'administrative_units.json'
        )


        self.stdout.write(
            f'Đang tìm file: {json_path}'
        )


        # =====================================================
        # KIỂM TRA FILE
        # =====================================================

        if not json_path.exists():

            self.stdout.write(
                self.style.ERROR(
                    f'Không tìm thấy file: {json_path}'
                )
            )

            return


        # =====================================================
        # ĐỌC JSON
        # =====================================================

        with open(
            json_path,
            'r',
            encoding='utf-8'
        ) as file:

            data = json.load(file)


        # =====================================================
        # IMPORT
        # =====================================================

        city_count = 0
        ward_count = 0


        for city_data in data.get('cities', []):

            city, created = City.objects.update_or_create(

                code=city_data.get('code'),

                defaults={
                    'name': city_data['name']
                }
            )


            if created:
                city_count += 1


            for ward_data in city_data.get('wards', []):

                Ward.objects.update_or_create(

                    code=ward_data.get('code'),

                    defaults={
                        'name': ward_data['name'],
                        'city': city,
                        'ward_type': ward_data.get(
                            'ward_type',
                            'commune'
                        ),
                        'district': None
                    }
                )


                ward_count += 1


        # =====================================================
        # KẾT QUẢ
        # =====================================================

        self.stdout.write(
            self.style.SUCCESS(
                '======================================'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                'IMPORT THÀNH CÔNG'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'City mới: {city_count}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Ward đã import: {ward_count}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                '======================================'
            )
        )