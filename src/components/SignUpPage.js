import React, { useState } from 'react';
import LoginPage from './LoginPage.js';


function SignUpPage() {
    const [username, setUsername] = useState('');
    const [loginPage, setLoginPage] = useState(false);

    function updateUsername(e) {
        setUsername(e.target.value)
    }

    function signUp() {

        console.log(username)

        const headers = {
            method: 'POST',
            body: JSON.stringify({ 'username': username })
        }

        fetch('http://172.16.227.59:8081/signup', headers)
            .then(response => response.json(), error => console.log(error))
            .then(data => console.log(data), error => console.log(error));
    }

    function switchToLogin() {
        setLoginPage(true)
    }

    if (loginPage) {
        return <LoginPage />
    } else {
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