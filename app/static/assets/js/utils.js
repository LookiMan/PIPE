const PIPE_LUI_HEADER = 'PP-Last-Update-Id'; 

export const TABLE_TYPE = {
    Download: 'Download',
    Remove: 'Remove',
}


function renderItem(fileName, buttonType, actionUrl) {
    const title = buttonType === TABLE_TYPE.Download ? 'download' : 'remove';
    const _class = buttonType === TABLE_TYPE.Download ? 'download-button' : 'remove-button';
    const action = `<a href="${actionUrl}" class="${_class}">${title}</a>`;

    return $(`<li class="table-row">
                <div class="col col-1"><p>${fileName}</p></div>
                <div class="col col-2">
                    ${action}
                </div>
            </li>`);
}


export function renderDownloadButton(data) {
    return renderItem(data.name, TABLE_TYPE.Download, data.action);
}


export function renderRemoveButton(data) {
    return renderItem(data.name, TABLE_TYPE.Remove, data.action);
}


export function renderTable(buttonType) {
    const url = $('#action-url').val();
    $.ajax({
        url: url,
        headers: {
            [PIPE_LUI_HEADER]: $('#hidden-last-update-id').val() || 0,
        },
        success: function (response, status, xhr) {
            const render = buttonType === TABLE_TYPE.Download ? renderDownloadButton : renderRemoveButton;
            const target = $('.table .responsive-body');

            if (!isNeedStartRenderingButtons(xhr)) {
                console.log('skip updating...')
                return;
            }

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
        const fileName = event.target.value.split('\\').pop();

        if (fileName) {
            label.find('span.placeholder').addClass('d-none');
            label.find('span.filename').removeClass('d-none').html(fileName);
        }
    });
}

function isNeedStartRenderingButtons(xhr) {
    const serverLastUpdateId = xhr.getResponseHeader(PIPE_LUI_HEADER);
    const input = $('#hidden-last-update-id');

    if (!input.val()) {
        $('body').append($(`<input id="hidden-last-update-id" type="hidden" value="${serverLastUpdateId}"></input>`));
        return true;
    }

    if (input.val() < serverLastUpdateId) {
        input.val(serverLastUpdateId);
        return true;
    }

    return false;
}


export class Watcher {
    timer = null;
  
    constructor (callback, interval) {
        this.callback = callback;
        this.interval = interval;
    }
  
    start() {
        this.timer = setInterval(this.callback, this.interval);
    }
  
    stop() {
        clearInterval(this.timer);
        this.timer = null;
    }

    trigger() {
        this.callback();
        this.restart();
    }
  
    restart(interval = 0) {
        this.stop();
  
        if (interval) {
            this.interval = interval || this.interval;
        }
  
        this.start();
    }
};
