import { GetUpdates } from '../utils.js';
import { RenderTable } from '../utils.js'; 
import { TABLE_TYPE } from '../utils.js'; 
import { Watcher } from '../utils.js';


$(document).ready(function () {
    $('#download-item').closest('li').addClass('active');

    const render  = new RenderTable('.table .responsive-body', TABLE_TYPE.Download);
    const updates = new GetUpdates(render);
    const watcher = new Watcher(() => updates.get(), 1000*10); // 10 seconds
    watcher.trigger();

    $('body').on('click', '.download-button', function (event) {
        event.preventDefault();

        const url = $(event.currentTarget).attr('href');

        $.ajax({
            url,
            type: 'GET',
            complete: function (response) {
                const link = $('<a>');
                link.attr('href', url);
                link.attr('download', 'download');
                link[0].click();
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });
});
