multipleSelectors(".save", "POST");
multipleSelectors(".delete", "DELETE");


function multipleSelectors(selector, method) {
    document.querySelectorAll(selector).forEach((button) => {
        var childs = button.parentElement.parentElement.children;
        var source = childs[0].firstChild.innerHTML;
        var target = childs[2].firstChild.innerHTML;
        button.addEventListener("click", (e) => {
            send_data(method, source, target);
        });
    });
}
function send_data(method, source, target) {
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
}

document.querySelector(".add").addEventListener("click", () => {
    var source = document.querySelector("#source").value;
    var target = document.querySelector("#target").value;
    if (source == "" || target == "") {
        alert("Please fill in all fields");
        return;
    }
    if (source.charAt(0) == "/")
        source = source.substring(1);

    send_data("PUT", source, target);
});
