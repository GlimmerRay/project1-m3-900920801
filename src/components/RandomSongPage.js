import React, { useState, useEffect } from 'react';
import ArtistIdEntryPage from './ArtistIdEntryPage.js';

function RandomSongPage(props) {

    const [previewUrl, setPreviewUrl] = useState('')
    const [imgUrl, setImgUrl] = useState('')
    const [artistName, setArtistName] = useState('')
    const [trackName, setTrackName] = useState('')
    const [lyricsUrl, setLyricsUrl] = useState('')

    const headers = {
        method: 'POST',
        body: JSON.stringify({
            'username': props.username
        })
    }

    useEffect(() => { fetchRandomSong() }, [])

    function fetchRandomSong() {
        fetch('http://192.168.1.127:8081/random-song', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => setArtistData(data), error => console.log(error));
    }

    function setArtistData(data) {
        setPreviewUrl(data['preview_url'])
        setTrackName(data['track_name'])
        setArtistName(data['artist_name'])
        setImgUrl(data['img_url'])
        setLyricsUrl(data['lyrics_url'])
    }

    return <>
        <p>Logged in as: <span className="username">{props.username}</span></p>
        <ArtistIdEntryPage username={props.username} />
        <img src={imgUrl} width="400px"></img>
        <p>Artist name: {artistName}</p>
        <p>Track name: {trackName}</p>
        <p><a href={previewUrl}>preview</a></p>
        <p><a href={lyricsUrl}>lyrics</a></p>
        <p><button onClick={fetchRandomSong}>Load New Song</button></p>
    </>

}

export default RandomSongPage;