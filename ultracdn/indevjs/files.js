////<div class="file-list-item">
////    <div class="file-list-item-name">File 1</div>
////    <div class="file-list-item-actions px-5 rightalign">
////        <button class="icon">Rename</button>
////        <button class="icon">Delete</button>
////    </div>
////    <div class="file-list-item-size">1.2 MB</div>
////</div>

//append to id="files"

function showPrompt() {
    var promptBox = document.getElementById("promptBox");
    promptBox.style.display = "flex";
}

function hidePrompt() {
    var promptBox = document.getElementById("promptBox");
    promptBox.style.display = "none";
}
src=""




function httpGet(url, headers) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url);

        // Add headers to the request, if provided
        if (headers) {
            for (const header in headers) {
                xhr.setRequestHeader(header, headers[header]);
            }
        }

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject(new Error(`HTTP error ${xhr.status}: ${xhr.statusText}`));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error'));
        };

        xhr.send();
    });
}
function httpPatch(url, headers = {}) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('PATCH', url);

        // Add headers to the request, if provided
        if (headers) {
            for (const header in headers) {
                xhr.setRequestHeader(header, headers[header]);
            }
        }

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject(new Error(`HTTP error ${xhr.status}: ${xhr.statusText}`));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error'));
        };

        xhr.send();
    });
}
function httpDelete(url, headers = {}) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('DELETE', url);

        // Add headers to the request, if provided
        if (headers) {
            for (const header in headers) {
                xhr.setRequestHeader(header, headers[header]);
            }
        }

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject(new Error(`HTTP error ${xhr.status}: ${xhr.statusText}`));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error'));
        };

        xhr.send();
    });
}
function httpPost(url, data = {}, headers = {}) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);

        // Add headers to the request
        for (const header in headers) {
            xhr.setRequestHeader(header, headers[header]);
        }

        // Convert the data object to a JSON string and set the content type header
        xhr.setRequestHeader('Content-Type', 'application/json');
        const jsonData = JSON.stringify(data);

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.responseText);
            } else {
                reject(new Error(`HTTP error ${xhr.status}: ${xhr.statusText}`));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error'));
        };

        xhr.send(jsonData);
    });
}

function httpPostFetch(url, data, headers) {
    let formData = new FormData();
    console.log(data)
    formData.append("file", data);
    return fetch(url, { method: "POST", body: data, headers: headers });
}

function submitPrompt() {
    var nameInput = document.getElementById("name");
    var error = document.getElementById("error");

    var name = nameInput.value;

    // Validate the name
    if (name.trim() === "") {
        error.textContent = "Name cannot be empty";
        nameInput.classList.add("error"); // Apply error class
        return;
    }

    if (!/\.[^.]+$/.test(name)) {
        error.textContent = "Name must include a file extension";
        nameInput.classList.add("error"); // Apply error class
        return;
    }

    if (/[',\/<>:;"()*&^%$#@!~`_+\-=\{\}\[\]\\\|]/.test(name)) {
        error.textContent = "Name contains invalid characters";
        nameInput.classList.add("error"); // Apply error class
        return;
    }

    // Clear any previous error messages and remove error class
    error.textContent = "";
    nameInput.classList.remove("error");

    // Use the submitted name as needed
    console.log("Submitted name:", name);
    httpPatch(`/api/files?file=${src}&dest=${name}`, { "Authorization": cookie })
        .then(text => {
            console.log(text)
            ref()
        })
        .catch(error => {
            console.error(error);
        });
    hidePrompt();
}
function handleKey(key) {
    if (key.keyCode == 13) {
        submitPrompt();
    }
}
let cookie = ""
if (document.cookie != "") {
    cks = document.cookie.split(";")
    function iter(i) {
        if (i.startsWith("cookie")) {
            ck = i.split("=")[1]
            ck = ck.replace(" ", "")
            cookie=ck
        }
    }
    cks.forEach(iter)
} else {
    document.location = "/login"
}
function hr(number) {
    return Number(number.toFixed(2));
}

function iter2(f) {
    div = document.createElement("div")
    div.setAttribute("class", "file-list-item")
    attr = f.split(",")
    size = attr[1]
    str = ""
    if (size > 1024 * 1024 * 1024) {
        str = `${hr(size / (1024 * 1024 * 1024))}GB`
    } else if (size > 1024 * 1024) {
        str = `${hr(size / (1024 * 1024))}MB`
    } else if (size > 1024) {
        str = `${hr(size / (1024))}KB`
    } else {
        str = `${size}B`
    }
    iht = `<div class="file-list-item-name">${attr[0]}</div>
    <div class="file-list-item-actions px-5 rightalign">
        <button class="icon" onclick="rename_file_trig('${attr[0]}')">Rename</button>
        <button class="icon" onclick="delete_file('${attr[0]}')">Delete</button>
        <button class="icon" onclick="trig_download('${attr[0]}')">Download</button>
    </div>
    <div class="file-list-item-size">${str}</div>`
    div.innerHTML = iht
    document.getElementById("files").appendChild(div)
    ////<div class="file-list-item">

    ////</div>
}
function ref() {
    console.log("Trying to refresh")
    document.getElementById("files").innerHTML = ""
    httpGet('/api/files?file=filelist.index', { "Authorization": cookie })
        .then(text => {
            text.split("\n").forEach(iter2)
        })
        .catch(error => {
            console.error(error);
        });
}
function downloadFileFromServer(fileUrl, filename) {
    const headers = new Headers();

    // Set the authorization header
    if (cookie) {
        headers.append('Authorization', cookie);
    }

    fetch(fileUrl, {
        method: 'GET',
        headers: headers,
    })
        .then(response => response.blob())
        .then(blob => {
            // Extract the filename from the URL
            //const filename = urlParams.get('file');

            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename; // Set the filename
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error downloading file:', error);
        });
}

function trig_download(fn) {
    downloadFileFromServer(`/api/files?file=${fn}`,fn)
}
function delete_file(fn) {
    console.log("Deleting")
    httpDelete(`/api/files?file=${fn}`, { "Authorization": cookie })
        .then(text => {
            console.log(text)
            ref()
        })
        .catch(error => {
            console.error(error);
        });
}
function rename_file_trig(fn) {
    src=fn
    document.getElementById("name").value = fn;
    showPrompt();
}
function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function (event) {
            const fileContent = event.target.result;
            resolve(fileContent);
        };

        reader.onerror = function (event) {
            reject(event.target.error);
        };

        reader.readAsText(file);
    });
}
function uploadFile() {
    const fileInput = document.getElementById('fileinput');
    const file = fileInput.files[0];
    
    if (file) {
        readFileContent(file)
            .then(content => {

                const filePath = fileInput.value;
                const separator = filePath.includes('\\') ? '\\' : '/';
                const parts = filePath.split(separator);
                const filename = parts[parts.length - 1];
                httpPostFetch(`/api/files?file=${filename}`, content, { 'Authorization': cookie }).then(text => {
                    //window.location.reload();
                    fileInput.value = "";
                    ref()
                })
                    .catch(error => {
                        console.error(error);
                    });
                // Process the file content as needed
            })
            .catch(error => {
                console.error('Error reading file:', error);
                // Handle the error if needed
            });
    } else {
        console.log('No file selected');
       
    }

    

    
}
//filelist.index to grab file list
            httpGet('/api/files?file=filelist.index', { "Authorization": cookie })
                .then(text => {
                    text.split("\n").forEach(iter2)
                })
                .catch(error => {
                    console.error(error);
                });

hidePrompt()