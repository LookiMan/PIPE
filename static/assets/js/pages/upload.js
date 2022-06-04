
$(document).ready(function () {

    $('#upload-button').on('click', function (event) {
        const files = $('input[type=file]').prop('files');

        if (files.length === 0) {
            swal('Упс!', 'Выберите файл для загрузки', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', files[0]);

        $.ajax({
            url: '/uploader',
            type: 'POST',
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            data: formData,
            success: function (response) {
                swal('Успех!', response.description, 'success');
            },
            error: function (error) {
                swal('Упс!', JSON.stringify(error), 'error');
            },
        });
    });

    $('#upload-item').addClass('active');
});
