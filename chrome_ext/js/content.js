chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg === 'get_userdata') {
    	var schedule_json_regex = /var jsonData = ([\s\S]*?);\s*Scheduler\.initialize/mi;
    	var html = document.all[0].outerHTML;
    	var matches = html.match(schedule_json_regex);
        sendResponse(JSON.parse(matches[1]));
    }
});