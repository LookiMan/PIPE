import { GetUpdates }  from '../components/get-updates';
import { TableRender } from '../components/table-render';
import { Watcher }     from '../components/watcher';
import { TABLE_TYPE }  from '../utils'; 


$(document).ready(function () {
    $('#download-item').closest('li').addClass('active');

    const render  = new TableRender('.table .responsive-body', TABLE_TYPE.Download);
    const updates = new GetUpdates(render.update);
    const watcher = new Watcher(updates.get, 1000*10); // 10 seconds
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
