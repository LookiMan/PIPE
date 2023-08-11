import { renderRemoveButton } from '../utils.js'; 


$(document).ready(function () {
    $('#upload-item').closest('li').addClass('active');

    $('#upload-button').on('click', function (event) {
        const target = $(event.currentTarget);
        const files = $('input[type=file]').prop('files');

        if (files.length === 0) {
            swal('Warning', 'Select a file to download', 'warning');
            return;
        }

        const form = new FormData();
        form.append('file', files[0]);

        $.ajax({
            url: $(target).data('url'),
            type: 'POST',
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            data: form,
            success: function (response) {
                swal('Success', response?.message || response, 'success');

                if (response.file) {
                    $('.table .responsive-body').append(renderRemoveButton(response.file));
                };
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });

    /*
    setInterval(() => {

    }, 15*1000)
    */
});
