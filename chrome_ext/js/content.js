chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.msg === 'get_userdata') {
        var schedule_json_regex = /var jsonData = ([\s\S]*?);\s*Scheduler\.initialize/mi;
        var html = document.all[0].outerHTML;
        var matches = html.match(schedule_json_regex);
        sendResponse(JSON.parse(matches[1]));
    } else if (msg.msg == 'warn_user') {
        var actualCode = `toastr.${ msg.toast_type }(\"${ msg.toast_msg }\");`;
        var s = document.createElement('script');
        s.textContent = actualCode;
        s.onload = function() { s.parentNode.removeChild(s); }; // Somehow this doesn't work
        (document.head||document.documentElement).appendChild(s);
    }
});

function injectScript(scriptUrl) {
    var s = document.createElement("script");
    (document.head || document.documentElement).appendChild(s);
    s.onload = function() { s.parentNode.removeChild(s); }
    s.src = chrome.extension.getURL(scriptUrl);
};

function injectCSS(cssUrl) {
    var s = document.createElement("link");
    s.rel = "stylesheet";
    s.type = "text/css";
    s.href = chrome.extension.getURL(cssUrl);
    (document.head || document.documentElement).appendChild(s);
};

injectScript("toastr/toastr.min.js");
injectCSS("toastr/toastr.min.css");
