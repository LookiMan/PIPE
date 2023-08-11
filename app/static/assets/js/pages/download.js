
$(document).ready(function () {

    $('.download-button').on('click', function (event) {
        const url = $(this).data('url');
        $.ajax({
            url,
            type: 'GET',
            complete: function (response) {
                const link = $('<a>');
                link.attr('href', url);
                link.attr('download', 'download');
                link.click();
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    });

    $('#download-item').closest('li').addClass('active');
});
