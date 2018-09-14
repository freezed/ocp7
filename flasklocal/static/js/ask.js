// AJAX Post with JS fetch
function addSubmit(ev) {
    ev.preventDefault();
    fetch('/ask', {method: 'POST', body: new FormData(this)})
    .then(function(response) { return response.json(); })
    .then(function(json) {
        var chatDiv = document.getElementById('chat');

        const markup = `
                <p>${json.question}</p>
                <p>${json.address}</p>
                <p>
                    ${json.extract}
                    Mais je fatigue : c'est l'heure de la sièste!
                    Va donc voir <a href='https://fr.wikipedia.org/w/index.php?curid=${json.curid}'>sur wikipedia</a>, pendant que je vais faire un somme (-:
                </p>
                <p><a href="${json.map_link}"><img src="${json.map_img_src}"></a></p>
            `
        chatDiv.innerHTML = markup;
   })
};

var form = document.getElementById('form');
form.addEventListener('submit', addSubmit);
