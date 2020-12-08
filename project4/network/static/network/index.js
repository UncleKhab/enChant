//---Global Variables
let status = 0;

//----Event Listeners
    document.getElementById("tweet-create-form").addEventListener("submit", postTweet)
//----API CALLS

function getRequestToApi(list){
    fetch(`list/${list}`)
    .then(response => response.json())
    .then(response => {
        console.log(response)
    })
}

function postTweet(e){
    e.preventDefault()
    const myForm = e.target
    const content = myForm.content.value

    fetch('create/', {
        method: 'POST',
        body: JSON.stringify({content: content}),
        
    })
    .then(response => {
        status = response.status
        return response.json()
    })
    .then(response => {
        if (status !== 201){
            alert(response.error)
        }else{
            alert(response.message)
        }
    })
    
}

getRequestToApi("all");
getRequestToApi("following");