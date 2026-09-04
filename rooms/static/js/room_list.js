document.addEventListener('DOMContentLoaded', function () {

    const citySelect = document.getElementById('filter_city');
    const wardSelect = document.getElementById('filter_ward');

    if (!citySelect || !wardSelect) {
        console.error('Không tìm thấy city hoặc ward.');
        return;
    }


    // =========================
    // URL API LẤY PHƯỜNG/XÃ
    // =========================

    const wardsUrl = wardSelect.dataset.url;

    if (!wardsUrl) {
        console.error('Không tìm thấy URL API phường/xã.');
        return;
    }


    // =========================
    // RESET PHƯỜNG/XÃ
    // =========================

    function resetWard() {

        wardSelect.innerHTML =
            '<option value="">Tất cả</option>';

        wardSelect.disabled = true;
    }


    // =========================
    // LẤY PHƯỜNG/XÃ THEO TỈNH
    // =========================

    function loadWards(cityId, selectedWard = '') {

        if (!cityId) {

            resetWard();

            return;
        }


        wardSelect.disabled = true;

        wardSelect.innerHTML =
            '<option value="">Đang tải...</option>';


        fetch(`${wardsUrl}?city_id=${cityId}`)

            .then(function (response) {

                if (!response.ok) {
                    throw new Error(
                        `HTTP error: ${response.status}`
                    );
                }

                return response.json();

            })

            .then(function (data) {

                wardSelect.innerHTML =
                    '<option value="">Tất cả</option>';


                data.forEach(function (ward) {

                    const option =
                        document.createElement('option');

                    option.value = ward.id;

                    option.textContent = ward.name;


                    if (
                        String(ward.id) ===
                        String(selectedWard)
                    ) {

                        option.selected = true;

                    }


                    wardSelect.appendChild(option);

                });


                wardSelect.disabled = false;

            })

            .catch(function (error) {

                console.error(
                    'Lỗi khi tải phường/xã:',
                    error
                );


                wardSelect.innerHTML =
                    '<option value="">Không thể tải dữ liệu</option>';

                wardSelect.disabled = true;

            });
    }


    // =========================
    // CHỌN TỈNH/THÀNH PHỐ
    // =========================

    citySelect.addEventListener(
        'change',
        function () {

            const cityId = citySelect.value;

            loadWards(cityId);

        }
    );


    // =========================
    // KHÔI PHỤC FILTER TỪ URL
    // =========================

    const params =
        new URLSearchParams(
            window.location.search
        );


    const selectedCity =
        params.get('city');

    const selectedWard =
        params.get('ward');


    // Nếu URL có tỉnh
    if (selectedCity) {

        citySelect.value = selectedCity;

        loadWards(
            selectedCity,
            selectedWard
        );

    } else {

        resetWard();

    }

});