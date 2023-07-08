document.querySelector('#logout').addEventListener('click', () => {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            method: 'logout'
        })
    }).then(() => {
        window.location.href = '/';
    }).catch((error) => {
        console.log(error);
    });
});