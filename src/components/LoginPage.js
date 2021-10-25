import React, { useState, useEffect } from 'react';
import SignUpPage from './SignUpPage.js';
import RandomSongPage from './RandomSongPage.js';


function LoginPage() {
    const [username, setUsername] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const [signUpPage, setSignUpPage] = useState(false);

    function updateUsername(e) {
        if (!loggedIn) {
            setUsername(e.target.value)
        }
    }

    function login() {

        console.log('HI????')

        const headers = {
            method: 'POST',
            body: JSON.stringify({ 'username': username })
        }

        fetch('/login', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => setLoggedIn(data['login_successful']),
                error => console.log(error));
    }

    function switchToSignUp() {
        setSignUpPage(true)
    }

    if (loggedIn) {
        return <RandomSongPage username={username} />
    } else if (signUpPage) {
        return <SignUpPage />
    } else {
        return <>
            <h1>Login Page</h1>
            <input type='text' onChange={updateUsername} />
            <button onClick={login}>Login</button>
            <p>Need an account?
                <button onClick={switchToSignUp}>Sign Up</button>
            </p>
        </>
    }

}

export default LoginPage;