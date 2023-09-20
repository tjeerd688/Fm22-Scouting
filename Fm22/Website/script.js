const URL = 'http://127.0.0.1:8000/data'
async function makeAPICall() {
    const result = await fetch(URL)
    result.json().then(data => {
        console.log(data)
    })
}

makeAPICall()