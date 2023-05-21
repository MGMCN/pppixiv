const searchBtn = document.getElementById("search");
const downloadBtn = document.getElementById("download");
const input = document.getElementById("input-field");
const select = document.getElementById("select-field");
const listElement = document.getElementById("list-group");
const masonryContainer = document.getElementById("masonry-container");
const masonryItemsContainer = document.getElementById("masonry-items-container");
const previewButton = document.getElementById("toggle-button");
const preogressBarContainer = document.getElementById("pb-container");
const progressBar = document.getElementById("pb");
const progressText = document.getElementById("progress-text");

let global_list = [];
const regex = /Get success! (.*)/;
let global_downloaded_list = [];
let toggleFlag = false;

searchBtn.addEventListener('click', function () {
    preogressBarContainer.style.display = 'none';
    progressBar.style.width = '0%';
    masonryItemsContainer.innerHTML = ``;
    listElement.innerHTML = ``;
    global_list = [];
    global_downloaded_list = [];

    let xhr = new XMLHttpRequest();
    let type = select.options[select.selectedIndex].value;
    let formData = new FormData();
    formData.append(type, input.value)
    switch (type) {
        case 'uid':
            xhr.open('POST', '/getIllustListByUid', true);
            break;
        case 'illust_id':
            xhr.open('POST', '/getIllustDownloadUrl', true);
            break;
        case 'mode':
            xhr.open('POST', '/getIllustRanking', true);
            break;
        default:
            break;
    }
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (this.status === 200) {
            let data = JSON.parse(this.responseText);
            let status = data.status;
            let message = data.message;
            if (status === 1) {
                let render_html = "";
                global_list = data.list;
                global_list.forEach(function (item) {
                    let title = item.title;
                    let url = item.url;
                    render_html += `<li class="list-group-item"><a href="${url}">${title}</a><span class="status-circle"></span></li>`;
                });
                listElement.innerHTML = render_html;
                Swal.fire({
                    title: 'Search success',
                    text: `Search complete! Found: ${global_list.length} items`,
                    icon: 'success',
                    confirmButtonText: 'confirm'
                });
            } else {
                Swal.fire({
                    title: 'Search failed',
                    text: message,
                    icon: 'warning',
                    confirmButtonText: 'confirm'
                });
            }
        } else {
            Swal.fire({
                title: 'Request failed',
                text: 'Check your server status!',
                icon: 'error',
                confirmButtonText: 'confirm'
            });
        }
    };
    xhr.send(new URLSearchParams(formData).toString());
});

function renderPreviewingView() {
    let images = '';
    global_downloaded_list.forEach(function (image) {
        images += `<div class="item"><img class="item-img" src="/Illusts/${image}"></div>`;
    });
    masonryItemsContainer.innerHTML = images;
}

function toPercent(floatNum) {
    let str = Number(floatNum * 100).toFixed(1);
    str += "%";
    return str;
}

downloadBtn.addEventListener('click', function () {
    // ?
    if (global_list.length === 0) {
        Swal.fire({
            title: 'Info',
            text: "Download list is empty!",
            icon: 'info',
            confirmButtonText: 'confirm'
        });
    } else {
        if (global_downloaded_list != 0) {
            Swal.fire({
                title: 'Info',
                text: "Already downloaded!",
                icon: 'info',
                confirmButtonText: 'confirm'
            });
            return;
        }
        progressBar.style.width = '0%';
        preogressBarContainer.style.display = 'block';
        let count_success = 0;
        let count_failed = 0;
        global_list.forEach(function (item, index) {
            let title = item.title;
            let url = item.download_url;
            let iid = item.id;
            let xhr = new XMLHttpRequest();
            let formData = new FormData();
            formData.append("id", iid);
            formData.append("title", title);
            formData.append("download_url", url);
            xhr.open('POST', '/download', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                if (this.status === 200) {
                    let data = JSON.parse(this.responseText);
                    let status = data.status;
                    let message = data.message;
                    if (status === 1) {
                        count_success += 1;
                        global_downloaded_list.push(message.match(regex)[1]);
                        listElement.getElementsByTagName("li")[this.idx].getElementsByTagName("span")[0].className = "status-circle-complete";
                    } else {
                        count_failed += 1;
                        listElement.getElementsByTagName("li")[this.idx].getElementsByTagName("span")[0].className = "status-circle-failed";
                        Swal.fire({
                            title: 'Download failed',
                            text: message,
                            icon: 'warning',
                            confirmButtonText: 'confirm'
                        });
                    }
                } else {
                    Swal.fire({
                        title: 'Request failed',
                        text: 'Check your server status!',
                        icon: 'error',
                        confirmButtonText: 'confirm'
                    });
                }
                if (count_success + count_failed === global_list.length) {
                    renderPreviewingView();
                    Swal.fire({
                        title: 'Download complete',
                        text: `Success: ${count_success}, Failed: ${count_failed}`,
                        icon: 'success',
                        confirmButtonText: 'confirm'
                    });
                }
                let percentage = toPercent((count_success + count_failed) / global_list.length * 1.0);
                progressBar.style.width = percentage;
                progressText.innerText = percentage;
            };
            xhr.idx = index;
            xhr.send(new URLSearchParams(formData).toString());
        });
    }
});

previewButton.addEventListener('click', function () {
    toggleFlag = !toggleFlag;
    if (toggleFlag == true) {
        listElement.style.display = "none";
        masonryContainer.style.display = "block";
    } else {
        masonryContainer.style.display = "none";
        listElement.style.display = "block";
    }
});
