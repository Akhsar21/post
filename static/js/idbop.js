var dbPromise = idb.open("posts-db", 5, function (upgradeDb) {
  upgradeDb.createObjectStore("posts", { keyPath: "pk" });
});

//collect latest post from server and store in idb
fetch("http://127.0.0.1:8000/getdata")
  .then(function (response) {
    return response.json();
  })
  .then(function (jsondata) {
    dbPromise.then(function (db) {
      var tx = db.transaction("posts", "readwrite");
      var postStore = tx.objectStore("posts");
      for (var key in jsondata) {
        if (jsondata.hasOwnProperty(key)) {
          postStore.put(jsondata[key]);
        }
      }
    });
  });

//retrive data from idb and display on page
var post = "";
dbPromise
  .then(function (db) {
    var tx = db.transaction("posts", "readonly");
    var postStore = tx.objectStore("posts");
    return postStore.openCursor();
  })
  .then(function logItems(cursor) {
    if (!cursor) {
      document.getElementById("offlinedata").innerHTML = post;
      return;
    }
    for (var field in cursor.value) {
      if (field == "fields") {
        postData = cursor.value[field];
        for (var key in postData) {
          if (key == "title") {
            var title = "<h3>" + postData[key] + "</h3>";
          }
          if (key == "author") {
            var author = postData[key];
          }
          if (key == "content") {
            var content = "<p>" + postData[key] + "</p>";
          }
        }
        post = post + "<br>" + title + "<br>" + author + "<br>" + content + "<br>";
      }
    }
    return cursor.continue().then(logItems);
  });
