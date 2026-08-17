import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from rooms.models import City, Ward, District, Room


class Command(BaseCommand):
    help = "Import 34 tỉnh/thành + 3.321 xã/phường/đặc khu an toàn, không xóa dữ liệu."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="rooms/templates/data/administrative_units.json",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Chỉ kiểm tra, không ghi database.",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.exists():
            raise CommandError(f"Không tìm thấy file: {path}")

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise CommandError(f"JSON không hợp lệ: {e}")

        cities_data = payload.get("cities", [])
        if len(cities_data) != 34:
            raise CommandError(
                f"JSON phải có 34 city, hiện có {len(cities_data)}."
            )

        expected_wards = sum(len(c.get("wards", [])) for c in cities_data)
        if expected_wards != 3321:
            raise CommandError(
                f"JSON phải có 3321 ward/xã/phường/đặc khu, hiện có {expected_wards}."
            )

        seen_city_codes = set()
        seen_ward_codes = set()

        for c in cities_data:
            code = str(c["code"])
            if code in seen_city_codes:
                raise CommandError(f"Trùng mã tỉnh: {code}")
            seen_city_codes.add(code)

            for w in c.get("wards", []):
                code_w = str(w["code"])
                if code_w in seen_ward_codes:
                    raise CommandError(f"Trùng mã cấp xã: {code_w}")
                seen_ward_codes.add(code_w)

        if options["dry_run"]:
            self.stdout.write(self.style.SUCCESS(
                f"DRY RUN OK: {len(cities_data)} tỉnh/thành, "
                f"{expected_wards} xã/phường/đặc khu."
            ))
            return

        city_created = city_updated = ward_created = ward_updated = 0

        with transaction.atomic():
            for c in cities_data:
                city_code = str(c["code"])
                city_name = c["name"]

                # Ưu tiên City đã có đúng code.
                city = City.objects.filter(code=city_code).first()

                if city is None:
                    # Nếu database cũ đã có cùng tên nhưng chưa có code,
                    # dùng bản ghi đang được Room sử dụng nhiều nhất.
                    candidates = City.objects.filter(name=city_name)
                    if candidates.exists():
                        city = max(
                            candidates,
                            key=lambda x: (
                                Room.objects.filter(city=x).count(),
                                -x.id,
                            ),
                        )
                        city.code = city_code
                        city.name = city_name
                        city.save(update_fields=["code", "name"])
                        city_updated += 1
                    else:
                        city = City.objects.create(
                            name=city_name,
                            code=city_code,
                        )
                        city_created += 1
                else:
                    changed = False
                    if city.name != city_name:
                        city.name = city_name
                        changed = True
                    if changed:
                        city.save(update_fields=["name"])
                    city_updated += 1

                for w in c.get("wards", []):
                    ward_code = str(w["code"])
                    ward_name = w["name"]
                    ward_type = w["ward_type"]

                    ward, created = Ward.objects.update_or_create(
                        code=ward_code,
                        defaults={
                            "name": ward_name,
                            "city": city,
                            "ward_type": ward_type,
                        },
                    )

                    if created:
                        ward_created += 1
                    else:
                        ward_updated += 1

        self.stdout.write(self.style.SUCCESS("IMPORT THÀNH CÔNG"))
        self.stdout.write(f"City tạo mới: {city_created}")
        self.stdout.write(f"City cập nhật: {city_updated}")
        self.stdout.write(f"Ward tạo mới: {ward_created}")
        self.stdout.write(f"Ward cập nhật: {ward_updated}")
        self.stdout.write(
            "Không xóa City/Ward/District/Room cũ."
        )
