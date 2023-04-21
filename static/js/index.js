const searchBtn = document.getElementById("search");
const downloadBtn = document.getElementById("download");
const input = document.getElementById("input-field");
const select = document.getElementById("select-field");
const listElement = document.getElementById("list-group");
// debug
// console.log(searchBtn);
// console.log(downloadBtn);
// console.log(input.value);
// console.log(select.options[select.selectedIndex].value);
// console.log(listElement);

var global_list = [];

searchBtn.addEventListener('click', function () {
    var xhr = new XMLHttpRequest();
    var type = select.options[select.selectedIndex].value;
    var formData = new FormData();
    formData.append(type, input.value)
    if (type === 'uid') {
        xhr.open('POST', '/getIllustListByUid', true);
    } else {
        xhr.open('POST', '/getIllustDownloadUrl', true);
    }
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (this.status === 200) {
            var data = JSON.parse(this.responseText);
            global_list = data.list;
            var status = data.status;
            var message = data.message;
            if (status === 1) {
                var render_html = "";
                global_list.forEach(function (item) {
                    var title = item.title;
                    var url = item.url
                    render_html += `<li class="list-group-item"><a href="${url}">${title}</a><span class="status-circle"></span></li>`;
                });
                listElement.innerHTML = render_html;
            } else {
                alert(message);
            }
        } else {
            alert("Request error!");
        }
    };
    xhr.send(new URLSearchParams(formData).toString());
});


downloadBtn.addEventListener('click', function () {
    // ?
    if (global_list.length === 0) {
        alert("Download list is empty!");
    } else {
        global_list.forEach(function (item, index) {
            var title = item.title;
            var url = item.download_url;
            var xhr = new XMLHttpRequest();
            var formData = new FormData();
            formData.append("title", title);
            formData.append("download_url", url);
            xhr.open('POST', '/download', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                if (this.status === 200) {
                    var data = JSON.parse(this.responseText);
                    var status = data.status
                    var message = data.message;
                    if (status === 1) {
                        listElement.getElementsByTagName("li")[this.idx].getElementsByTagName("span")[0].className = "status-circle-complete";
                    } else {
                        listElement.getElementsByTagName("li")[this.idx].getElementsByTagName("span")[0].className = "status-circle-failed";
                        alert(message);
                    }
                } else {
                    alert("Request error!");
                }
            };
            xhr.idx = index;
            xhr.send(new URLSearchParams(formData).toString());
        });
    }
});
