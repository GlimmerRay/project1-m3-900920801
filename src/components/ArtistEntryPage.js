import React, { useState } from 'react';

function ArtistIdForm(props) {

    const [artistIds, setArtistIds] = useState([])
    const [newId, setNewId] = useState('')
    const [validIds, setValidIds] = useState([])
    const [invalidIds, setInvalidIds] = useState([])
    const [canSubmit, setCanSubmit] = useState(false)

    function displayArtistIds() {
        const idListItems = []
        var key = 0
        for (var id of artistIds) {
            idListItems.push(<li key={key}>{id}</li>)
            key = key + 1
        }
        return <>
            <ul className='new-id-list'>{idListItems}</ul>
        </>
    }

    async function addId() {
        if (!canSubmit) {
            setCanSubmit(true)
        }
        setArtistIds([...artistIds, newId])
    }

    function updateNewId(e) {
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

        setArtistIds([])
        setNewId('')
        setCanSubmit(false)

        fetch('http://192.168.1.127:8081/save', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => setReturnData(data), error => console.log(error));


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
            return <p>Saved the following ids: <ol className="valid-id-list">{display}</ol></p>
        }
    }


    function displayInvalidIds() {
        var display = []
        for (var id of invalidIds) {
            display.push(<li>{id}</li>)
        }
        if (display.length > 0) {
            return <p>These ids were invalid: <ol className="invalid-id-list">{display}</ol></p>
        }
    }

    return <>
        <div>
            {displayValidIds()}
            {displayInvalidIds()}
            {displayArtistIds()}
            <input type="text" onChange={updateNewId} value={newId}></input>
            <button onClick={addId}>Add New Artist</button>
            <button onClick={submitIds} disabled={!canSubmit}>Submit</button>
        </div>
    </>
}

export default ArtistIdForm;