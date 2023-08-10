

export function renderItem(data) {
    return $(`<li class="table-row">
                <div class="col col-1" data-label="Name"><p>${data.file.name}</p></div>
                <div class="col col-2" data-label="Action">
                    <a href="#" class="download-button">Download</a>
                </div>
            </li>`);
}
