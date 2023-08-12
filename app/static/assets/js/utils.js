const PIPE_LUID_HEADER = 'PP-Last-Update-Id'; 


export const TABLE_TYPE = {
    Download: 'Download',
    Remove: 'Remove',
}


export class RenderTable {
    constructor (selector, tableType) {
        this.tableType = tableType;
        this.table = $(selector);
    }

    renderItem(fileName, tableType, actionUrl) {
        const title = tableType === TABLE_TYPE.Download ? 'Download' : 'Remove';
        const _class = tableType === TABLE_TYPE.Download ? 'download-button' : 'remove-button';
        const action = `<a href="${actionUrl}" class="${_class}">${title}</a>`;
    
        return $(`<li class="table-row">
                    <div class="col col-1"><p>${fileName}</p></div>
                    <div class="col col-2">
                        ${action}
                    </div>
                </li>`);
    }

    update(response, status, xhr) {
        if (this.isNeedRenderingTable(xhr)) {
            this.table.find('.table-row').remove();
            for (const item of response) {
                this.table.append(this.renderItem(item.name, this.tableType, item.action));
            };
        };
    }

    isNeedRenderingTable(xhr) {
        const serverLastUpdateId = xhr.getResponseHeader(PIPE_LUID_HEADER);
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
};


export class GetUpdates {
    constructor (callback) {
        this.callback = callback;
        this.action_url = $('#action-url').val();
    }

    get() {
        const self = this; 
        $.ajax({
            url: self.action_url,
            headers: {
                [PIPE_LUID_HEADER]: $('#hidden-last-update-id').val() || 0,
            },
            success: function (response, status, xhr) {
                self.callback.update(response, status, xhr);
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    }
};


export class FileInput {
    constructor (selector) {
        this.input = $(selector);
    }

    init() {
        const label = this.input.next();

        this.input.change((event) => {
            const fileName = event.target.value.split('\\').pop();
    
            if (fileName) {
                label.find('span.placeholder').addClass('d-none');
                label.find('span.filename').removeClass('d-none').html(fileName);
            }
        });
    }

    reset() {
        this.input.val('');
        this.input.next().find('span.placeholder').removeClass('d-none');
        this.input.next().find('span.filename').addClass('d-none').html('');
    }

    file() {
        const files = this.input.prop('files');
        return files.length === 0 ? null : files[0];
    }
};


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
