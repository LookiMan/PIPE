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
