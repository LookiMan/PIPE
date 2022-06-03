
$(document).ready(function () {
    try {
        const url = location.pathname;

        switch (true) { 
            case url.indexOf('/upload/') !== -1:
                $('#upload-item').addClass('active');
                $('#upload-button').on('click', function (event) {
                    const files = $('input[type=file]').prop('files');

                    if (files.length === 0) {
                        swal('Упс!', 'Выберите файл для загрузки', 'warning');
                        return;
                    }

                    const formData = new FormData();
                    formData.append('file', files[0]);

                    $.ajax({
                        url: '/uploader',
                        type: 'POST',
                        contentType: false,
                        enctype: 'multipart/form-data',
                        processData: false,
                        data: formData,
                        success: function (response) {
                            swal('Успех!', response.description, 'success');
                        },
                        error: function (error) {
                            swal('Упс!', JSON.stringify(error), 'error');
                        },
                    });
                });
                break;
            case url.indexOf('/download/') !== -1:
                $('#download-item').addClass('active');
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
                break; 
        }
    } catch (error) {
        console.error(error);
    }
});
