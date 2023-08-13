import { PIPE_LUID_HEADER }  from '../utils'; 


export class GetUpdates {
    constructor (callback) {
        this.callback = callback;
        this.action_url = $('#action-url').val();
        this.get = this.get.bind(this);
    }

    get() {
        const self = this; 
        $.ajax({
            url: self.action_url,
            headers: {
                [PIPE_LUID_HEADER]: $('#hidden-last-update-id').val() || 0,
            },
            success: function (response, status, xhr) {
                self.callback(response, status, xhr);
            },
            error: function (error) {
                swal('Fail', error.responseText, 'error');
            },
        });
    }
};
