
console.log("test")
console.log(fetch('http://127.0.0.1:8000/data'))
    .then(res => res.json())
    .then(data => console.log(data))

