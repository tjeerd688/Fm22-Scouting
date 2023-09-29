fetch("http://127.0.0.1:8000/data").then((Response) => {
    return Response.json()
}).then((data) => {
    console.log(data);
})











//fetch('http://localhost:8000', {
//    mode: "cors",
//    credentials: "include",
//   headers: {
//        "Content-Type": "application/json"
//    }
//}).then((res) => {
//    res.json().then((data) => {
//        console.log("Data ", data)
//    })
//})
// const response = await fetch('http://127.0.0.1:8000/data');
// const detail = await response.json();
// var test = await fetch('http://127.0.0.1:8000/data')
// console.log(detail)

