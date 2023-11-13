document.addEventListener('click', function(event) {
    var element = event.target;
    while (element != null && element.tagName != 'A') {
        element = element.parentElement;
    }
    if (element != null && element.tagName === 'A') {
        event.preventDefault();
        jshelper.openUrl(element.href);
    }
}, true);