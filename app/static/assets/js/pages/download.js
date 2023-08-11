import { watcher } from '../utils.js'; 
import { ButtonType } from '../utils.js'; 


$(document).ready(function () {
    $('#download-item').closest('li').addClass('active');

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

    setInterval(() => {
        watcher(ButtonType.Download);
    }, 10*1000)

    watcher(ButtonType.Download);
});
