function getUpdate() {
    //create a new HTTP request
    var request = new XMLHttpRequest()
    //get value from text input in HTML
    var fname = document.getElementById("fname").value;
    //Open and send request with URL based on input value
    request.open('GET', 'https://api.agify.io?name='+fname, false)
    request.send()

    //parse the response from JSON to JS Object
    var obj = JSON.parse(request.response);

    //update paragraph objects text to the respones age value
    document.getElementById("display").innerHTML = obj.age;

    //deprecated learning attempts
    
    //const response = await fetch('https://api.agify.io?name=michael')
    //const data = await response.json()
    //var data = JSON.parse(this.response)
    //var xmlHttp = new XMLHttpRequest();
    //xmlHttp.open( "GET", 'https://api.agify.io?name=michael', true);
    //xmlHttp.send( null );
}