
$(document).ready(function () {

    $('#download-button').on('click', function (event) {
        event.preventDefault();
        
        const code = $('input[name="code-input"]').val().trim();

        if (!code) {
            swal('Упс!', 'Введите код для скачивания', 'warning');
            return;
        }

        const url = $(this).data('url').replace('/0', '/' + code);

        $.ajax({
            url,
            type: 'HEAD',
            complete: function (response) {
                console.log(response);
                if (response.getResponseHeader('Content-Type') === 'application/json') {
                    swal('Упс!', 'По данному коду файл не обнаружен', 'error');
                } else {
                    const link = $('<a>');
                    link.attr('href', url);
                    link.attr('download', 'download');
                    link[0].click();
                }
            }
        });
    });

    $('#code-input').keydown(function(event){ 
        const keyId = event.keyCode || event.which || event.key || 0;

        if (keyId === 13) {
            $('#download-button').click();
        }
    });

    $('#download-item').addClass('active');
});
