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
