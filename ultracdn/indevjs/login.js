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
function base64Encode(str) {
    // Convert the string to a UTF-8 encoded byte array
    const bytes = new TextEncoder().encode(str);

    // Base64 encode the byte array
    const base64 = btoa(String.fromCharCode(...bytes));

    // Return the Base64 encoded string
    return base64;
}
function sha256(input) {
    const buffer = new TextEncoder().encode(input);
    const digestBuffer = crypto.subtle.digest('SHA-256', buffer);
    const digestArray = Array.from(new Uint8Array(digestBuffer));
    const digestHex = digestArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return digestHex;
}

if (document.cookie != "") {
    cks = document.cookie.split(";")
    function iter(i) {
        if (i.startsWith("cookie"))
        {
            ck = i.split("=")[1]
            ck = ck.replace(" ", "")
            httpGet('/api/verify', { "Authorization": ck })
                .then(text => {
                    console.log(text);
                    if (text != "None") {
                        document.location = "/"
                    } else {
                        document.cookie = "";
                    }
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }
    cks.forEach(iter)
}

function login() {
    user = document.getElementById("Username").value;
    pass = base64Encode(document.getElementById("password").value);
    remb = document.getElementById("rememberMe").value
    if (user.length == 0 || pass.length == 0) {
        return "";
    }
    httpPost('/api/login', {"username":user,"password":pass})
        .then(text => {
            console.log(text);
            if (text != "None") {
                if (!remb) {
                    document.cookie = "cookie=" + text + ";";
                } else {
                    document.cookie = "cookie=" + text + "; expires=Fri, 31 Dec 9999 23:59:59 GMT;";
                }
                document.location = "/"
            } else {
                console.log("Login failed");
                //document.cookie = "";
            }
        })
        .catch(error => {
            console.error(error);
        });
}