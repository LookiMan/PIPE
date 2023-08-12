import { init_file_input } from '../utils.js'; 
import { renderTable } from '../utils.js'; 
import { TABLE_TYPE } from '../utils.js';
import { Watcher } from '../utils.js';


$(document).ready(function () {
    $('#upload-item').closest('li').addClass('active');

    const fileSelectInput = $('.hidden-file-input');
    const watcher = new Watcher(() => {renderTable(TABLE_TYPE.Remove)}, 1000*10); // 10 seconds
    watcher.trigger();

    init_file_input(fileSelectInput);

    $('#upload-button').on('click', function (event) {
        const target = $(event.currentTarget);
        const files = fileSelectInput.prop('files');

        if (files.length === 0) {
            swal('Warning', 'Select a file to upload', 'warning');
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
                swal('Success', response, 'success');
                watcher.trigger();
                // Reset file input 
                fileSelectInput.val('');
                fileSelectInput.next().find('span.placeholder').removeClass('d-none');
                fileSelectInput.next().find('span.filename').addClass('d-none').html('');
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
                watcher.trigger();
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });
});
