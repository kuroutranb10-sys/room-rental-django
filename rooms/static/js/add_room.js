document.addEventListener('DOMContentLoaded', function () {

    const citySelect =
        document.getElementById('id_city');

    const wardSelect =
        document.getElementById('id_ward');


    if (!citySelect || !wardSelect) {

        console.error(
            'Không tìm thấy city hoặc ward.'
        );

        return;
    }


    // =========================
    // RESET PHƯỜNG/XÃ
    // =========================

    function resetWard() {

        wardSelect.innerHTML =
            '<option value="">---------</option>';

        wardSelect.disabled = true;
    }


    // =========================
    // LOAD PHƯỜNG/XÃ
    // =========================

    function loadWards(cityId) {

        resetWard();


        if (!cityId) {
            return;
        }


        wardSelect.disabled = false;


        fetch(
            `/rooms/api/wards/?city_id=${cityId}`
        )

        .then(response => {

            if (!response.ok) {

                throw new Error(
                    'Không thể lấy danh sách phường/xã'
                );

            }

            return response.json();

        })

        .then(data => {

            data.forEach(function (ward) {

                const option =
                    document.createElement('option');


                option.value =
                    ward.id;


                option.textContent =
                    ward.name;


                wardSelect.appendChild(option);

            });

        })

        .catch(error => {

            console.error(
                'Lỗi lấy phường/xã:',
                error
            );

        });

    }


    // =========================
    // CHỌN TỈNH/THÀNH PHỐ
    // =========================

    citySelect.addEventListener(
        'change',
        function () {

            const cityId =
                this.value;


            loadWards(cityId);

        }
    );


    // =========================
    // TRẠNG THÁI BAN ĐẦU
    // =========================

    if (!citySelect.value) {

        resetWard();

    } else {

        loadWards(
            citySelect.value
        );

    }

});

// =========================
// ĐỊNH DẠNG TIỀN
// =========================

const moneyFields = [
    document.getElementById('id_price'),
    document.getElementById('id_electricity_price'),
    document.getElementById('id_water_price'),
    document.getElementById('id_deposit')
];


moneyFields.forEach(function (input) {

    if (!input) {
        return;
    }


    input.addEventListener('input', function () {

        let value =
            this.value.replace(/\D/g, '');


        if (value) {

            this.value =
                Number(value).toLocaleString('vi-VN');

        } else {

            this.value = '';

        }

    });

});


// =========================
// TRƯỚC KHI SUBMIT
// =========================

const form =
    document.querySelector('form');


if (form) {

    form.addEventListener('submit', function () {

        moneyFields.forEach(function (input) {

            if (!input) {
                return;
            }


            input.value =
                input.value.replace(/\./g, '');

        });

    });

}