const url = "http://127.0.0.1:5000/"

function loadAdmin() {
  // Redirects page to admin page
  window.location.href = url+"admin"
}

function register(){
  window.location.href = url+"register"
}

function newUser(){
  username2 = document.getElementById("username2").value
  password2 = document.getElementById("Password2").value
  fullname = document.getElementById("full_name").value


  fetch(url+"newUser", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({username2,password2,fullname})
  })
  .then(response => window.location.href=response.url)


}

function login() {
  // Checks credentials and loads the respective page for user.
  username = document.getElementById("username").value
  password = document.getElementById("password").value

  fetch(url+"login", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => window.location.href=response.url)
}

function logout() {
  // Sends user back to login page.
  fetch(url+"logout", {
    method: "GET"
  })
  .then(response => window.location.href=response.url)
}

function loadPostPage() {
  //Redirect to Post Page

  fetch(url+"loadPostPage", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => window.location.href=response.url)
}

function loadUser() {
  //Redirect to Post Page

  fetch(url+"loadUser", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => window.location.href=response.url)
}

function loadFollowPost(){
  fetch(url+"followpost", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(data => displayPost2(data))
}

function loadUserPost() {
  //Redirect to Post Page

  fetch(url+"myPost", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(data => displayPost(data))
}

function loadAllPosts(){
  fetch(url+"getallpost", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(data => displayPost2(data))
}

function CreatePost(){
  pic = document.getElementById("picture").value
  desc = document.getElementById("desc").value

  if(pic =="" && desc ==""){
    return alert("Please have a picture URL or description")
  }
  
  fetch(url+"createPost", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({pic,desc})
  })
  .then(response => response.json())
  .then(data => alert(data))
  
}

async function deleteUserPost(element) {
  id = element.value
  console.log(id)

  fetch(url+"deletepost", {
    method: "DELETE", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({id})
  })
  .then(response => response.json())
  .then(data => alert(data))
}

function sharePost(element){
  id = element.value
  console.log(id)

  fetch(url+"sharepost", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({id})
  })
  .then(response => response.json())
  .then(data => alert(data))
}

function getshared(){
  fetch(url+"getshared", {
    method: "GET", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
   
  })
  .then(response => response.json())
  .then(data => displayPost3(data))
}

function addfollow(element){
  name = element.value
  console.log(name)
  

  fetch(url+"follow", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name})
  })
  .then(response => response.json())
  .then(data => alert(data))
}

function likePost(element){
  Id = element.value
  console.log(Id)

  fetch(url+"like", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({Id})
  })
  .then(response => response.json())
  .then(data => alert(data))

}

function dislikePost(element){
  Id = element.value
  console.log(Id)

  fetch(url+"dislike", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({Id})
  })
  .then(response => response.json())
  .then(data => alert(data))
}

function addComment(element){
  Id = element.value
  console.log(Id)
  get = "comment" + Id
  comment = document.getElementById(get).value
  console.log(comment)

  fetch(url+"addComment", {
    method: "POST", 
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({Id,comment})
  })
  .then(response => response.json())
  .then(data => alert(data))
}




async function displayPost(data){
  console.log(data)
  display = document.getElementById("display")
  while (display.firstChild) {
    display.removeChild(display.firstChild);
  }

  var entry ="<br><br>"
  for (item in data){
    entry += "<tr>"
    entry += "<p> You posted on: " + String(data[item].Date) +"</p>"
    entry += "<button value = " + String(data[item].Id) + " onclick = sharePost(this)>Share Post</button>"
    entry += "<button value = " + String(data[item].Id) + " onclick = deleteUserPost(this)>Delete Post</button><br>"
    if (String(data[item].Picture) != 0){
      entry += "<img src=" + String(data[item].Picture) + " width = '300' height = '300'><br>"
    }
    entry += "<p>" + String(data[item].Description) + "</p></tr>"
    entry += "<tr><br><br>"
    entry += "<h style = 'font-size: 30px' >Comments</h>"
    
   
    console.log("continue for comments")
    list = data[item].Comments
    console.log(list)
    
    for(item in list){
      console.log("inside comment list")
      entry += "<br>"
      entry += "<p>" + String(list[item].Commenter)+ " posted on: " + String(list[item].Date) +"</p><br>"
      entry += "<p>" + String(list[item].Comment) + "</p><br>"
    }
    entry += "</tr>"
    entry += "<h4></h4>"

  }
  console.log(entry)
  document.getElementById("display").innerHTML = entry;
}


function displayPost2(data){
  console.log(data)
  display = document.getElementById("display")
  while (display.firstChild) {
    display.removeChild(display.firstChild);
  }

  var entry =""
  for (item in data){
    entry += "<tr>"
    entry += "<p>" + String(data[item].Poster)+ " posted on: " + String(data[item].Date) +"</p>"
    entry += "<button value = " + String(data[item].Id) + " onclick = sharePost(this)>Share Post</button>"
    entry += "<button value = " + String(data[item].Poster) + " onclick = addfollow(this)>Follow/Unfollow this Person</button><br>" 
    if (String(data[item].Picture) != 0){
      entry += "<img src=" + String(data[item].Picture) + " width = '300' height = '300'><br>"
    }
    entry += "<p>Likes:" + String(data[item].Likes) +"     Dislikes:" + String(data[item].Dislikes) + "</p>"
    entry += "<button value = " + String(data[item].Id)  + " onclick = likePost(this)>Like Post</button>"
    entry += "<button value = " + String(data[item].Id)  + " onclick = dislikePost(this)>Dislike Post</button><br>"
    entry += "<p>" + String(data[item].Description) + "</p></tr>"
    entry += "<tr><input id ='comment"+ String(data[item].Id)+ "' type='text' placeholder = 'Add Comment'/><button value = " + String(data[item].Id) + " onclick = addComment(this)>Add Comment</button></tr>"
    entry += "<tr><br><br>"
    entry += "<p style = 'font-size: 30px' >Comments</p>"

    
    console.log("continue for comments")
    list = data[item].Comments
    console.log(list)
    
    for(item in list){
      console.log("inside comment list")
      entry += "<br>"
      entry += "<p>" + String(list[item].Commenter)+ " posted on: " + String(list[item].Date) +"</p><br>"
      entry += "<p>" + String(list[item].Comment) + "</p><br>"
    }
    entry += "</tr>"
    entry += "<h4></h4>"

  }

  document.getElementById("display").innerHTML = entry;
}

function displayPost3(data){
  console.log(data)
  display = document.getElementById("display")
  while (display.firstChild) {
    display.removeChild(display.firstChild);
  }

  var entry =""
  for (item in data){
    entry += "<tr>"
    entry += "<p>"+ String(data[item].SharingPerson) + " shared this post!:</p><br>"
    entry += "<p>" + String(data[item].Poster)+ " posted on: " + String(data[item].Date) +"</p>"
    entry += "<button value = " + String(data[item].Id) + " onclick = sharePost(this)>Share Post</button>"
    entry += "<button value = " + String(data[item].Poster) + " onclick = addfollow(this)>Follow/Unfollow this Person</button><br>" 
    if (String(data[item].Picture) != 0){
      entry += "<img src=" + String(data[item].Picture) + " width = '300' height = '300'><br>"
    }
    entry += "<p>Likes:" + String(data[item].Likes) +"     Dislikes:" + String(data[item].Dislikes) + "</p>"
    entry += "<button value = " + String(data[item].Id)  + " onclick = likePost(this)>Like Post</button>"
    entry += "<button value = " + String(data[item].Id)  + " onclick = dislikePost(this)>Dislike Post</button><br>"
    entry += "<p>" + String(data[item].Description) + "</p></tr>"
    entry += "<tr><input id ='comment"+ String(data[item].Id)+ "' type='text' placeholder = 'Add Comment'/><button value = " + String(data[item].Id) + " onclick = addComment(this)>Add Comment</button></tr>"
    entry += "<tr><br><br>"
    entry += "<h style = 'font-size: 30px' >Comments</h>"

    
    console.log("continue for comments")
    list = data[item].Comments
    console.log(list)
    
    for(item in list){
      console.log("inside comment list")
      entry += "<br>"
      entry += "<p>" + String(list[item].Commenter)+ " posted on: " + String(list[item].Date) +"</p><br>"
      entry += "<p>" + String(list[item].Comment) + "</p><br>"
    }
    entry += "</tr>"
    entry += "<p>---------------------------------------------------</p>"
    

  }

  document.getElementById("display2").innerHTML = entry;
}