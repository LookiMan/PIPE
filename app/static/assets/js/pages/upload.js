import { GetUpdates } from '../utils.js';
import { FileInput } from '../utils.js';
import { RenderTable } from '../utils.js'; 
import { TABLE_TYPE } from '../utils.js';
import { Watcher } from '../utils.js';


$(document).ready(function () {
    $('#upload-item').closest('li').addClass('active');

    const fileInput = new FileInput('.hidden-file-input');
    fileInput.init();

    const render  = new RenderTable('.table .responsive-body', TABLE_TYPE.Remove);
    const updates = new GetUpdates(render);
    const watcher = new Watcher(() => updates.get(), 1000*10); // 10 seconds
    watcher.trigger();

    $('#upload-button').on('click', function (event) {
        const target = $(event.currentTarget);
        const file = fileInput.file();

        if (!file) {
            swal('Warning', 'Select a file to upload', 'warning');
            return;
        }

        const form = new FormData();
        form.append('file', file);

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
                fileInput.reset();
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
