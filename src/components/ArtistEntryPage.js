import React, { useState } from 'react';

function ArtistIdForm(props) {

    const [artistIds, setArtistIds] = useState([])
    const [newId, setNewId] = useState('hi???')

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
            .then(data => console.log(data), error => console.log(error));
    }

    return <>
        <h1>Artist Id Entry Page</h1>
        {displayArtistIds()}
        <input type="text" onChange={doSomething}></input>
        <button onClick={addId}>Add</button>
        <button onClick={submitIds}>Submit</button>
    </>
}

export default ArtistIdForm;