const logo = document.querySelector('#logo');

const clickEventType = 'ontouchend' in document ? 'touchstart' : 'click';
const ulPlaylists = document.querySelector('#ul-playlists');
const btnLoadPlaylists = document.querySelector('#btn-playlists');

const historyButton = document.querySelector('#btn_recently_played');
const historyContainer = document.querySelector('#container');
const historySlider = document.querySelector('#slider');
const historyList = document.querySelector('#table');
let recentlyPlayed = [];
let recentlyPlayedFiltered = [];


function split_url(url) {
    let parts = url.split('?');
    let data = parts[1].split('&').map(arg => arg.split('='));

    url = parts[0];
    data = Object.assign({}, ...data.map(arg => ({[arg[0]]: arg[1]})))
    return { url, data }
}


function getQueryString(params) {

    const esc = encodeURIComponent;
    return Object.keys(params)
        .map(k => `${esc(k)}=${esc(params[k])}`)
        .join('&');
}


function request(params) {

    let method = params.method || 'GET';
    let headers = params.headers || {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'};
    let qs = '';
    let body;

    if (['GET', 'DELETE'].indexOf(method) > -1) {
        qs = '?' + getQueryString(params.data);
    } else {
        body = JSON.stringify(params.data);
    }

    let url = `${params.url}${qs}`;

    return fetch(url, { method, headers, body });
}


function formatTimestamp(ts) {

    let date = new Date(ts);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2);
    let day = ('0' + date.getDate()).slice(-2);

    return `${year}-${month}-${day}`;
}


async function fetchRecentlyPlayed(userId) {

    params = {
        method: 'POST',
        url: `http://${window.location.host}/history`,
        data: { user_id: userId }
    };
    
    let response = await request(params);
    let result = await response.json();

    recentlyPlayed = result.map(rp => {
        return {...rp, played_at: new Date(rp.played_at)};
    }).sort().reverse();
    recentlyPlayedFiltered = recentlyPlayed;
}


function createRecentlyPlayedSlider() {

    if (!(recentlyPlayedFiltered.length > 0)) return;

    const DAY_MS = 1000 * 60 * 60 * 24;

    let startTime = recentlyPlayed[0].played_at.getTime();
    let startTimeInt = startTime - (startTime % DAY_MS);

    let endTime = recentlyPlayed[recentlyPlayed.length - 1].played_at.getTime();
    let endTimeInt = endTime + (DAY_MS - (endTime % DAY_MS));
    
    const formatter = {
        to: (value) => formatTimestamp(value),
        from: (value) => formatTimestamp(value)
    };

    noUiSlider.create(slider, {
        start: [startTimeInt, endTimeInt],
        step: DAY_MS / 8,
        margin: DAY_MS,
        connect: true,
        range: {
            'min': startTimeInt,
            'max': endTimeInt
        },
        tooltips: [formatter, formatter]
    });

    slider.noUiSlider.on('update', (values, handle) => {
        let startTime = new Date(+values[0]);
        let endTime = new Date(+values[1]);
        recentlyPlayedFiltered = recentlyPlayed.filter(rp => {
            return rp.played_at >= startTime && rp.played_at <= endTime;
        });

        let rows = recentlyPlayedFiltered.map(rp => {
            let date = rp.played_at;
            let year = date.getFullYear();
            let month = ('0' + (date.getMonth() + 1)).slice(-2);
            let day = ('0' + date.getDate()).slice(-2);
            let hours = ('0' + date.getHours()).slice(-2);
            let minutes = ('0' + date.getMinutes()).slice(-2);
            let seconds = ('0' + date.getSeconds()).slice(-2);

            date = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
            return `
                <tr>
                    <td>${date}</td>
                    <td>${rp.track.name}</td>
                    <td>${rp.track.artists.map(a => a.name).join()}</td>
                    <td>${rp.track.album.name}</td>
                </tr>`
        }).reverse().join('');

        historyList.innerHTML = `
            <thead>
                <tr>
                    <th>Played at</th>
                    <th>Track</th>
                    <th>Artists</th>
                    <th>Album</th>
                </tr>
            </thead>
            ${rows}`;
    });
}


function loadRecentlyPlayed(event) {

    event.preventDefault();

    let user_id = logo.innerHTML;
    fetchRecentlyPlayed(user_id);
    createRecentlyPlayedSlider();

    historyButton.classList.toggle('invisible');
    historyContainer.classList.toggle('invisible');
}
historyButton.addEventListener(clickEventType, loadRecentlyPlayed);


function toggleActive(event) {
    
    event.preventDefault();

    const user_id = document.querySelector('#logo').innerHTML;
    if (event.target.innerHTML == 'on') {
        event.target.classList.remove('switch-on')
        event.target.classList.add('switch-off')
        event.target.innerHTML = 'off'
    } else {
        event.target.classList.remove('switch-off')
        event.target.classList.add('switch-on')
        event.target.innerHTML = 'on'
    }
}
document.querySelector('#recently_played').addEventListener(clickEventType, toggleActive);
document.querySelector('#playlist_monitor').addEventListener(clickEventType, toggleActive);