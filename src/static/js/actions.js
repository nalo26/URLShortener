createListeners(".save", "POST");
createListeners(".delete", "DELETE");


function createListeners(selector, method) {
    document.querySelectorAll(selector).forEach((button) => {
        var childs = button.parentElement.parentElement.children;
        var source = childs[0].firstChild.innerHTML;
        var target = childs[2].firstChild.innerHTML;
        button.addEventListener("click", (e) => {
            fetch(source, {
                method: method,
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    target: target,
                })
            }).then(() => {
                window.location.href = '/';
            }).catch((error) => {
                console.log(error);
            });
        });
    });
}