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

    function loadWards(
        cityId,
        selectedWardId = ''
    ) {

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


            // =========================
            // KHÔI PHỤC PHƯỜNG CŨ
            // =========================

            if (selectedWardId) {

                wardSelect.value =
                    selectedWardId;

            }

        })

        .catch(error => {

            console.error(
                'Lỗi lấy phường/xã:',
                error
            );

        });

    }


    // =========================
    // KHI ĐỔI TỈNH
    // =========================

    citySelect.addEventListener(
        'change',
        function () {

            const cityId =
                this.value;


            // Nếu người dùng đổi tỉnh
            // thì phải bỏ phường cũ

            loadWards(
                cityId
            );

        }
    );


    // =========================
    // KHỞI TẠO EDIT
    // =========================

    const cityId =
        citySelect.value;

    const selectedWardId =
        wardSelect.value;


    if (cityId) {

        loadWards(
            cityId,
            selectedWardId
        );

    } else {

        resetWard();

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

/*
 * ============================================
 * XÓA ẢNH PHỤ
 * ============================================
 */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const deleteButtons =
            document.querySelectorAll(
                ".delete-image-button"
            );


        deleteButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const imageId =
                            this.dataset.id;

                        const deleteUrl =
                            this.dataset.url;


                        const confirmed =
                            confirm(
                                "Bạn có chắc muốn xóa ảnh phụ này không?"
                            );


                        if (!confirmed) {
                            return;
                        }


                        /*
                         * Khóa nút trong lúc xóa
                         */

                        button.disabled = true;

                        button.innerText =
                            "Đang xóa...";


                        /*
                         * Lấy CSRF TOKEN
                         */

                        const csrfToken =
                            document.querySelector(
                                "[name=csrfmiddlewaretoken]"
                            ).value;


                        /*
                         * Gửi yêu cầu POST
                         */

                        fetch(
                            deleteUrl,
                            {
                                method: "POST",

                                headers: {
                                    "X-CSRFToken":
                                        csrfToken,

                                    "X-Requested-With":
                                        "XMLHttpRequest"
                                }
                            }
                        )


                        .then(
                            function (response) {

                                if (!response.ok) {

                                    throw new Error(
                                        "Không thể xóa ảnh"
                                    );

                                }

                                return response.json();

                            }
                        )


                        .then(
                            function (data) {

                                if (data.success) {

                                    /*
                                     * Xóa ảnh khỏi giao diện
                                     */

                                    const imageElement =
                                        document.getElementById(
                                            "room-image-" +
                                            imageId
                                        );


                                    if (imageElement) {

                                        imageElement.remove();

                                    }


                                    /*
                                     * Nếu không còn ảnh phụ
                                     */

                                    const gallery =
                                        document.getElementById(
                                            "gallery"
                                        );


                                    if (
                                        gallery &&
                                        gallery.children.length === 0
                                    ) {

                                        const box =
                                            gallery.closest(
                                                ".current-images"
                                            );

                                        if (box) {
                                            box.remove();
                                        }

                                    }

                                } else {

                                    alert(
                                        data.message ||
                                        "Không thể xóa ảnh."
                                    );


                                    button.disabled = false;

                                    button.innerText =
                                        "🗑 Xóa";

                                }

                            }
                        )


                        .catch(
                            function (error) {

                                console.error(error);


                                alert(
                                    "Có lỗi xảy ra khi xóa ảnh."
                                );


                                button.disabled = false;

                                button.innerText =
                                    "🗑 Xóa";

                            }
                        );

                    }
                );

            }
        );

    }
);