export const ButtonType = {
    Download: 'Download',
    Remove: 'Remove',
}


function renderItem(fileName, buttonType, actionUrl) {
    const title = buttonType === ButtonType.Download ? 'download' : 'remove';
    const _class = buttonType === ButtonType.Download ? 'download-button' : 'remove-button';
    const action = `<a href="${actionUrl}" class="${_class}">${title}</a>`;

    return $(`<li class="table-row">
                <div class="col col-1" data-label="Name"><p>${fileName}</p></div>
                <div class="col col-2" data-label="Action">
                    ${action}
                </div>
            </li>`);
}


export function renderDownloadButton(data) {
    return renderItem(data.name, ButtonType.Download, data.action);
}


export function renderRemoveButton(data) {
    return renderItem(data.name, ButtonType.Remove, data.action);
}


export function watcher(buttonType) {
    const url = $('#action-url').val();
    $.ajax({
        url: url,
        success: function (response) {
            const render = buttonType === ButtonType.Download ? renderDownloadButton : renderRemoveButton;
            const target = $('.table .responsive-body');

            target.find('.table-row').remove();

            for (const item of response) {
                target.append(render(item));
            }
        },
        error: function (error) {
            swal('Fail', error.responseText, 'error');
        },
    });
}


export function init_file_input(input) {
    const label = input.next();

    input.change((event) => {
        fileName = event.target.value.split('\\').pop();

        if (fileName) {
            label.find('span.placeholder').addClass('d-none');
            label.find('span.filename').removeClass('d-none').html(fileName);
        }
    });
}
