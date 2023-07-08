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

document.querySelectorAll(".delete").forEach((button) => {
    var childs = button.parentElement.parentElement.children;
    var source = childs[0].firstElementChild.innerHTML;
    var target = childs[2].firstElementChild.innerHTML;
    button.addEventListener("click", () => {
        send_data("DELETE", source, target);
    });
});

document.querySelectorAll(".edit").forEach((button) => {
    button.addEventListener("click", () => {
        var childs = button.parentElement.parentElement.children;
        var source = childs[0];
        var target = childs[2];
        var source_text = source.firstElementChild.innerHTML.substring(1);
        var target_text = target.firstElementChild.href;
        var source_input = document.createElement("input");
        var target_input = document.createElement("input");
        source_input.setAttribute("type", "text");
        target_input.setAttribute("type", "text");
        source_input.setAttribute("value", source_text);
        target_input.setAttribute("value", target_text);
        source_input.classList.add("w-full", "px-3", "py-2", "border", "rounded-lg", "focus:outline-none", "focus:ring-1", "focus:ring-purple-600");
        target_input.classList.add("w-full", "px-3", "py-2", "border", "rounded-lg", "focus:outline-none", "focus:ring-1", "focus:ring-purple-600");
        source.classList.remove("px-6", "py-4");
        target.classList.remove("px-6", "py-4");
        source.classList.add("px-3", "py-2");
        target.classList.add("px-3", "py-2");
        source.removeChild(source.firstElementChild);
        target.removeChild(target.firstElementChild);
        source.appendChild(source_input);
        target.appendChild(target_input);

        var parent = button.parentElement;
        parent.innerHTML = "";
        var save_button = document.createElement("span");
        save_button.classList.add("save", "text-blue-700", "cursor-pointer", "fa-solid", "fa-floppy-disk");
        save_button.setAttribute("title", "Save");
        save_button.addEventListener("click", () => {
            send_data("POST", source_input.value, target_input.value);
        });
        parent.appendChild(save_button);
    });
});

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