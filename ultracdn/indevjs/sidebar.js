sb = document.getElementsByClassName("sidebar")[0]
loc = document.location.pathname

pages = [
    ["/", "Home"],
    ["/files", "Files"],
    ["/developer", "Developer"],
    ["/tos", "TOS"]
]

function iter(i) {
    btn = document.createElement("button")
    btn.setAttribute("onclick", "location.href='" + i[0] + "'")
    btn.innerHTML = i[1]
    if (i[0] == loc) {
        btn.style = "background-color:rgba(67,67,67,255);"
    }
    sb.appendChild(btn)
}
pages.forEach(iter)