
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
                swal('Success', response, 'success');
            },
            error: function (error) {
                swal('Fail', JSON.stringify(error.responseText), 'error');
            },
        });
    });

    $('#upload-item').addClass('active');
});
