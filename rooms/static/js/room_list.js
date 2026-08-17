document.addEventListener('DOMContentLoaded', function () {

    const citySelect =
        document.getElementById('filter_city');

    const wardSelect =
        document.getElementById('filter_ward');


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

        wardSelect.value = '';

        wardSelect.disabled = true;

        const options =
            wardSelect.querySelectorAll(
                'option[data-city]'
            );

        options.forEach(function (option) {

            option.hidden = true;

        });

    }


    // =========================
    // LỌC PHƯỜNG/XÃ THEO TỈNH
    // =========================

    function filterWards() {

        const cityId =
            citySelect.value;


        if (!cityId) {

            resetWard();

            return;
        }


        wardSelect.disabled = false;


        const options =
            wardSelect.querySelectorAll(
                'option[data-city]'
            );


        options.forEach(function (option) {

            if (
                option.dataset.city === cityId
            ) {

                option.hidden = false;

            } else {

                option.hidden = true;

            }

        });


        const current =
            wardSelect.options[
                wardSelect.selectedIndex
            ];


        if (
            current &&
            current.dataset.city &&
            current.dataset.city !== cityId
        ) {

            wardSelect.value = '';

        }

    }


    // =========================
    // CHỌN TỈNH
    // =========================

    citySelect.addEventListener(
        'change',
        function () {

            wardSelect.value = '';

            filterWards();

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


    if (selectedCity) {

        citySelect.value =
            selectedCity;

    }


    filterWards();


    if (selectedWard) {

        wardSelect.value =
            selectedWard;

    }

});