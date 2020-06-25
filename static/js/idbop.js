var dbPromise = idb.open("post-db", 5, function (upgradeDb) {
  upgradeDb.createObjectStore("post", { keyPath: "pk" });
});

//collect latest post from server and store in idb
fetch("http://127.0.0.1:8000/getdata")
  .then(function (response) {
    return response.json();
  })
  .then(function (jsondata) {
    dbPromise.then(function (db) {
      var tx = db.transaction("post", "readwrite");
      var postStore = tx.objectStore("post");
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
    var tx = db.transaction("post", "readonly");
    var postStore = tx.objectStore("post");
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
          if (key == "body") {
            var body = "<p>" + postData[key] + "</p>";
          }
        }
        post = post + "<br>" + title + "<br>" + author + "<br>" + body + "<br>";
      }
    }
    return cursor.continue().then(logItems);
  });
