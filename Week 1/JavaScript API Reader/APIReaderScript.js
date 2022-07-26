function getUpdate() {
    var request = new XMLHttpRequest()
    var fname = document.getElementById("fname").value;
    request.open('GET', 'https://api.agify.io?name='+fname, false)
    //const response = await fetch('https://api.agify.io?name=michael')
    //const data = await response.json()
    //var data = JSON.parse(this.response)
    //var xmlHttp = new XMLHttpRequest();
    //xmlHttp.open( "GET", 'https://api.agify.io?name=michael', true);
    //xmlHttp.send( null );
    request.send()

    var obj = JSON.parse(request.response);

    document.getElementById("display").innerHTML = obj.age;
}