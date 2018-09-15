// AJAX Post with JS fetch
function addSubmit(ev) {
    ev.preventDefault();
    fetch('/ask', {method: 'POST', body: new FormData(this)})
    .then(function(response) { return response.json(); })
    .then(function(json) {
        const chatElt = document.getElementById('chat');
        answerElt = document.createElement('div');
        const markup = `
                <p>${json.question}</p>
                <p>${json.address}</p>
                <p>
                    ${json.extract}
                    Mais je fatigue : c'est l'heure de la sièste!
                    Va donc voir <a href='https://fr.wikipedia.org/w/index.php?curid=${json.curid}'>sur wikipedia</a>.
                </p>
                <p><a href="${json.map_link}"><img src="${json.map_img_src}"></a></p>
            `
        answerElt.innerHTML = markup;
        chatElt.appendChild(answerElt)
        chatElt.innerHTML += '\n            '
   })
};

const form = document.getElementById('form');
form.addEventListener('submit', addSubmit);
