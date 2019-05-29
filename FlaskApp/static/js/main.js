let access_token;

function getQueryString(params) {
    const esc = encodeURIComponent;
    return Object.keys(params)
        .map(k => `${esc(k)}=${esc(params[k])}`)
        .join('&');
}

function request(params) {
    let method = params.method || 'GET';
    let headers = params.headers || new Headers();
    let qs = '';
    let body;

    if (['GET', 'DELETE'].indexOf(method) > -1) {
        qs = getQueryString(params.data);
    } else {
        body = JSON.stringify(params.data);
    }

    let url = `${params.url}?${qs}`;

    return fetch(url, { method, headers, body });
}

function split_url(url) {
    let parts = url.split('?');
    let data = parts[1].split('&').map(arg => arg.split('='));

    url = parts[0];
    data = Object.assign({}, ...data.map(arg => ({[arg[0]]: arg[1]})))
    return { url, data }
}

async function clickLoadPlaylists(event) {
    event.preventDefault();
    let response = await fetch('http://www.imsignificant.com/access_token?user_id=notbobbobby');
    let result = await response.json();
    let playlists = await(getPlaylists(result.access_token));

    playlists.forEach(playlist => {
        let li = document.createElement('li');
        let textNode = document.createTextNode(playlist);
        li.appendChild(textNode);
        ulPlaylists.appendChild(li);
    });

    btnLoadPlaylists.classList.add('hidden');
    ulPlaylists.classList.remove('hidden');
}

async function getPlaylists(access_token) {
    let response = await request({
        url: 'https://api.spotify.com/v1/me/playlists',
        data: { access_token, limit: 50 }});
    let result = await response.json();
    let playlists = result['items'];

    while (result['next']) {
        let params = split_url(result['next']);
        Object.assign(params.data, { access_token });
        response = await request(params);
        result = await response.json();
        playlists.push(...result['items'])
    }

    return playlists.map(p => p.name);
}

const clickEventType = 'ontouchend' in document ? 'touchstart' : 'click';
const ulPlaylists = document.querySelector('#ul-playlists');
const btnLoadPlaylists = document.querySelector('#btn-playlists');
btnLoadPlaylists.addEventListener(clickEventType, clickLoadPlaylists);