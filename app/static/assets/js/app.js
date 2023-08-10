
try {
    const url = location.pathname;

    switch (true) { 
        case url.indexOf('/upload/') !== -1:
            import('./pages/upload.js');
            break;
        case url.indexOf('/download/') !== -1:
            import('./pages/download.js');
            break; 
    }
} catch (error) {
    console.error(error);
}
