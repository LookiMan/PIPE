import { PIPE_LUID_HEADER }  from '../utils'; 
import { TABLE_TYPE }  from '../utils';


export class TableRender {
    constructor (selector, tableType) {
        this.tableType = tableType;
        this.table = $(selector);
        this.update = this.update.bind(this);
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
