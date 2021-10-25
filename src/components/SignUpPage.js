import React, { useState } from 'react';
import LoginPage from './LoginPage.js';
import RandomSongPage from './RandomSongPage.js';


function SignUpPage() {
    const [username, setUsername] = useState('')
    const [switchTologinPage, setSwitchToLoginPage] = useState(false)
    const [switchToRandomSongPage, setSwitchToRandomSongPage] = useState(false)

    function updateUsername(e) {
        setUsername(e.target.value)
    }

    function signUp() {

        console.log(username)

        const headers = {
            method: 'POST',
            body: JSON.stringify({ 'username': username })
        }

        fetch('/signup', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => handleResponse(data), error => console.log(error));
    }

    function handleResponse(data) {
        console.log(data)
        setSwitchToLoginPage(true)
    }

    function switchToLogin() {
        setSwitchToLoginPage(true)
    }

    if (switchTologinPage) {
        return <LoginPage />
    } else if (switchToRandomSongPage)
        return <RandomSongPage />
    else {
        return <>
            <h1>Sign Up Page</h1>
            <input type='text' onChange={updateUsername} />
            <button onClick={signUp}>Sign Up</button>
            <p>Already have an account?
                <button onClick={switchToLogin}>Login</button>
            </p>
        </>
    }
}

export default SignUpPage;