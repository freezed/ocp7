// AJAX Post with JS fetch
function addSubmit(ev) {
    ev.preventDefault();
    var chatDiv = document.getElementById('chat');
    fetch('/ask', {method: 'POST', body: new FormData(this)})
    .then(function(response) { return response.json(); })
    .then(function(json) {

        const markup = `
        <ul>
            <li>name : ${json.name}</li>
            <li>url : ${json.url}</li>
        </ul>
    `
        chatDiv.innerHTML = markup;
   })
};

var form = document.getElementById('form');
form.addEventListener('submit', addSubmit);
