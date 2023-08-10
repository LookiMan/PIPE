import { renderItem } from '../utils.js'; 


$(document).ready(function () {

    $('#upload-button').on('click', function (event) {
        const target = $(event.currentTarget);
        const files = $('input[type=file]').prop('files');

        if (files.length === 0) {
            swal('Warning', 'Select a file to download', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', files[0]);

        $.ajax({
            url: $(target).data('url'),
            type: 'POST',
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            data: formData,
            success: function (response) {
                swal('Success', response?.message || response, 'success');

                if (response.file) {
                    $('.table .responsive-body').append(renderItem(response));
                };
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });

    $('#upload-item').addClass('active');
});
