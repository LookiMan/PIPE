export class FileInput {
    constructor (selector) {
        this.input = $(selector);
        this.init();
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
