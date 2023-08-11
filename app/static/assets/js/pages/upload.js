import { renderRemoveButton } from '../utils.js'; 
import { watcher } from '../utils.js'; 
import { ButtonType } from '../utils.js'; 


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
                swal('Success', response.message, 'success');
                $('.table .responsive-body').prepend(renderRemoveButton(response.file));
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });

    $('body').on('click', '.remove-button', (event) => {
        event.preventDefault();

        const target = $(event.currentTarget);

        $.ajax({
            url: target.attr('href'),
            type: 'DELETE',
            success: function () {
                swal('Success', 'File successfully removed', 'success');
                target.closest('.table-row').remove();
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });

    setInterval(() => {
        watcher(ButtonType.Remove);
    }, 10*1000)

    watcher(ButtonType.Remove);
});
