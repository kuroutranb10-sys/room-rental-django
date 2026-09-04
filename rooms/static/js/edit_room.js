document.addEventListener('DOMContentLoaded', function () {

    /* =====================================================
       CITY → WARD
       ===================================================== */

    const citySelect = document.getElementById('id_city');
    const wardSelect = document.getElementById('id_ward');


    function resetWard() {

        if (!wardSelect) {
            return;
        }

        wardSelect.innerHTML = '<option value="">---------</option>';
        wardSelect.disabled = true;
    }


    function loadWards(cityId, selectedWardId = '') {

        if (!wardSelect) {
            return;
        }

        resetWard();

        if (!cityId) {
            return;
        }


        wardSelect.disabled = false;


        fetch(`/rooms/api/wards/?city_id=${encodeURIComponent(cityId)}`)

            .then(function (response) {

                if (!response.ok) {
                    throw new Error(
                        'Không thể lấy danh sách phường/xã.'
                    );
                }

                return response.json();
            })


            .then(function (data) {

                data.forEach(function (ward) {

                    const option =
                        document.createElement('option');

                    option.value = ward.id;
                    option.textContent = ward.name;

                    wardSelect.appendChild(option);
                });


                /*
                 * Nếu đang sửa phòng,
                 * chọn lại phường hiện tại.
                 */
                if (selectedWardId) {
                    wardSelect.value = selectedWardId;
                }

            })


            .catch(function (error) {

                console.error(
                    'Lỗi lấy danh sách phường/xã:',
                    error
                );

                wardSelect.innerHTML =
                    '<option value="">Không thể tải dữ liệu</option>';

                wardSelect.disabled = true;
            });
    }


    if (citySelect && wardSelect) {

        /*
         * Khi người dùng thay đổi thành phố
         */
        citySelect.addEventListener(
            'change',
            function () {

                const cityId = this.value;

                /*
                 * Không truyền selectedWardId
                 * vì đây là thành phố mới.
                 */
                loadWards(cityId);
            }
        );


        /*
         * Khi mở trang edit
         */
        const cityId = citySelect.value;
        const selectedWardId = wardSelect.value;


        if (cityId) {

            loadWards(
                cityId,
                selectedWardId
            );

        } else {

            resetWard();
        }
    }


    /* =====================================================
       MONEY FORMAT
       ===================================================== */

    const moneyFields = [
        document.getElementById('id_price'),
        document.getElementById('id_electricity_price'),
        document.getElementById('id_water_price'),
        document.getElementById('id_deposit')
    ];


    /*
     * Định dạng tiền:
     *
     * 1500000
     *      ↓
     * 1.500.000
     */
    function formatMoney(input) {

        if (!input) {
            return;
        }


        let value = input.value.replace(/\D/g, '');


        if (value) {

            input.value =
                Number(value).toLocaleString('vi-VN');

        } else {

            input.value = '';
        }
    }


    /*
     * Định dạng ngay khi mở trang edit.
     *
     * Ví dụ database có:
     *
     * 1500000
     *
     * thì giao diện sẽ hiện:
     *
     * 1.500.000
     */
    moneyFields.forEach(function (input) {

        if (!input) {
            return;
        }


        formatMoney(input);


        input.addEventListener(
            'input',
            function () {

                formatMoney(this);
            }
        );
    });


    /* =====================================================
       FORM SUBMIT
       ===================================================== */

    const form =
        document.getElementById('edit-room-form');


    if (form) {

        form.addEventListener(
            'submit',
            function () {

                /*
                 * Trước khi gửi form:
                 *
                 * 1.500.000
                 *      ↓
                 * 1500000
                 */
                moneyFields.forEach(
                    function (input) {

                        if (!input) {
                            return;
                        }

                        input.value =
                            input.value.replace(/\./g, '');
                    }
                );
            }
        );
    }


    /* =====================================================
       DELETE SECONDARY IMAGE
       ===================================================== */

    const deleteButtons =
        document.querySelectorAll(
            '.delete-image-button'
        );


    deleteButtons.forEach(function (button) {

        button.addEventListener(
            'click',
            function () {

                const imageId =
                    this.dataset.id;

                const deleteUrl =
                    this.dataset.url;


                /*
                 * Xác nhận trước khi xóa
                 */
                const confirmed =
                    confirm(
                        'Bạn có chắc muốn xóa ảnh phụ này không?'
                    );


                if (!confirmed) {
                    return;
                }


                /*
                 * Disable button trong lúc xử lý
                 */
                button.disabled = true;
                button.innerText = '...';


                /*
                 * Lấy CSRF token
                 */
                const csrfInput =
                    document.querySelector(
                        '[name=csrfmiddlewaretoken]'
                    );


                if (!csrfInput) {

                    console.error(
                        'Không tìm thấy CSRF token.'
                    );

                    alert(
                        'Không thể thực hiện thao tác.'
                    );

                    button.disabled = false;
                    button.innerText = '🗑';

                    return;
                }


                const csrfToken =
                    csrfInput.value;


                /*
                 * Gửi request POST
                 */
                fetch(deleteUrl, {

                    method: 'POST',

                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })


                .then(function (response) {

                    /*
                     * Backend có thể trả về 403
                     * nếu user không có quyền.
                     */
                    if (response.status === 403) {

                        throw new Error(
                            'Bạn không có quyền xóa ảnh này.'
                        );
                    }


                    if (!response.ok) {

                        throw new Error(
                            'Không thể xóa ảnh.'
                        );
                    }


                    return response.json();
                })


                .then(function (data) {

                    if (!data.success) {

                        throw new Error(
                            data.message ||
                            'Không thể xóa ảnh.'
                        );
                    }


                    /*
                     * Tìm gallery-item tương ứng
                     */
                    const imageElement =
                        document.getElementById(
                            'room-image-' + imageId
                        );


                    /*
                     * Xóa khỏi giao diện
                     */
                    if (imageElement) {

                        imageElement.remove();
                    }


                    /*
                     * Nếu không còn ảnh phụ
                     * thì xóa luôn khu vực gallery.
                     */
                    const gallery =
                        document.getElementById(
                            'gallery'
                        );


                    if (
                        gallery &&
                        gallery.children.length === 0
                    ) {

                        const currentImages =
                            gallery.closest(
                                '.current-images'
                            );


                        if (currentImages) {

                            currentImages.remove();
                        }
                    }

                })


                .catch(function (error) {

                    console.error(
                        'Lỗi xóa ảnh:',
                        error
                    );


                    alert(
                        error.message ||
                        'Có lỗi xảy ra khi xóa ảnh.'
                    );


                    /*
                     * Khôi phục button
                     */
                    button.disabled = false;
                    button.innerText = '🗑';
                });
            }
        );
    }

});