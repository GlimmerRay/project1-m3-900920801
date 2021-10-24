import React, { useState } from 'react';
import RandomSongPage from './RandomSongPage.js';

function ArtistIdForm(props) {

    const [artistIds, setArtistIds] = useState([])
    const [newId, setNewId] = useState('')
    const [validIds, setValidIds] = useState([])
    const [invalidIds, setInvalidIds] = useState([])

    function displayArtistIds() {
        const idListItems = []
        var key = 0
        for (var id of artistIds) {
            idListItems.push(<li className='id-list-item' key={key}>{id}</li>)
            key = key + 1
        }
        return <>
            <ul>{idListItems}</ul>
        </>
    }

    async function addId() {
        setArtistIds([...artistIds, newId])
    }

    function doSomething(e) {
        setNewId(e.target.value)
    }

    function submitIds() {

        const headers = {
            method: 'POST',
            body: JSON.stringify({
                'artist_ids': artistIds,
                'username': props.username
            })
        }

        fetch('http://172.16.227.59:8081/save', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => setReturnData(data), error => console.log(error));

        setArtistIds([])
        setNewId('')
    }

    function setReturnData(data) {
        setValidIds(data['valid_ids'])
        setInvalidIds(data['invalid_ids'])
    }

    function displayValidIds() {
        var display = []
        for (var id of validIds) {
            display.push(<li>{id}</li>)
        }
        if (display.length > 0) {
            return <p>Saved the following ids: <ol>{display}</ol></p>
        }
    }


    function displayInvalidIds() {
        var display = []
        for (var id of invalidIds) {
            display.push(<li>{id}</li>)
        }
        if (display.length > 0) {
            return <p>These ids were invalid: <ol>{display}</ol></p>
        }
    }

    return <>

        {displayValidIds()}
        {displayInvalidIds()}

        {displayArtistIds()}
        <input type="text" onChange={doSomething} value={newId}></input>
        <button onClick={addId}>Add New Artist</button>
        <button onClick={submitIds}>Submit</button>
        {/* <RandomSongPage></RandomSongPage> */}
    </>
}

export default ArtistIdForm;