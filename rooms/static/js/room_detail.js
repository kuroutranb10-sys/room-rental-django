async function shareRoomImage(imageUrl) {

    try {

        const response = await fetch(imageUrl);

        if (!response.ok) {
            throw new Error("Không thể tải ảnh");
        }

        const blob = await response.blob();

        const file = new File(
            [blob],
            "anh-phong.jpg",
            {
                type: blob.type
            }
        );

        if (
            navigator.share &&
            navigator.canShare &&
            navigator.canShare({
                files: [file]
            })
        ) {

            await navigator.share({
                files: [file]
            });

        } else {

            alert(
                "Thiết bị hoặc trình duyệt không hỗ trợ chia sẻ ảnh."
            );

        }

    } catch (error) {

        if (error.name !== "AbortError") {

            console.error(
                "Lỗi chia sẻ ảnh:",
                error
            );

            alert(
                "Không thể chia sẻ ảnh."
            );

        }

    }

}


document.addEventListener("DOMContentLoaded", function() {

    document
        .querySelectorAll(".share-image-button")
        .forEach(function(button) {

            button.addEventListener(
                "click",
                function() {

                    const imageUrl =
                        this.dataset.imageUrl;

                    shareRoomImage(imageUrl);

                }
            );

        });

});