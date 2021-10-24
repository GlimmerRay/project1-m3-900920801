import React, { useState, useEffect } from 'react';
import ArtistIdEntryPage from './ArtistIdEntryPage.js';

function RandomSongPage(props) {

    const [artistPage, setArtistPage] = useState(false)
    const [previewUrl, setPreviewUrl] = useState('')
    const [imgUrl, setImgUrl] = useState('')
    const [artistName, setArtistName] = useState('')
    const [trackName, setTrackName] = useState('')

    const headers = {
        method: 'POST',
        body: JSON.stringify({
            'username': props.username
        })
    }

    useEffect(() => { fetchRandomSong() }, [])

    function fetchRandomSong() {
        fetch('http://172.16.227.59:8081/random-song', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => setArtistData(data), error => console.log(error));
    }

    function setArtistData(data) {
        setPreviewUrl(data['preview_url'])
        setTrackName(data['track_name'])
        setArtistName(data['artist_name'])
        setImgUrl(data['img_url'])

    }

    function switchToArtistPage() {
        setArtistPage(true);
    }



    if (artistPage) {
        return <ArtistIdEntryPage username={props.username} />
    } else {
        return <>
            <p>Logged in as: {props.username}</p>
            <img src={imgUrl} width="400px"></img>
            <p>Artist name: {artistName}</p>
            <p>Track name: {trackName}</p>
            <p><a href={previewUrl}></a></p>
            <h1>RandomSongPage</h1>
            <p><button onClick={fetchRandomSong}>NewSong</button></p>
            <p><button onClick={switchToArtistPage}>Enter favorite artists</button></p>
        </>
    }

}

export default RandomSongPage;