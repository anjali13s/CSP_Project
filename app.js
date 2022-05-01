const express = require("express");
//const {spawn} = require('child_process');
const bodyParser = require("body-parser");
const request = require("request");

const app = express();

app.set('view engine', 'ejs');

app.use(express.static("public"));


//Trial 3
let runPy = function(fileName) {
  return new Promise(function(success, nosuccess) {

      const { spawn } = require('child_process');
      const pyprog = spawn('python', [fileName]);
      pyprog.stdout.on('data', function(data) {
          success(data);
      });
      pyprog.stderr.on('data', (data) => {
          nosuccess(data);
      });
  }).catch((err) => console.log("here is the error: " + err));
}



app.get("/", function(req, res){
  res.render("index");


});

app.get("/diagram", function(req,res){
  res.render("diagram");
});



app.get("/flip", function(req,res){

  runPy("server_Alice_new.py").then(function(fromRunpy) {
        console.log("server output: ");
        console.log(fromRunpy);
        //console.log(fromRunpy.toString());
        //res.end(fromRunpy);
    });
  runPy("client_Bob_new.py").then(function(fromRunpy) {
        console.log("client output: ");
        //console.log(fromRunpy);
        fromRunpy = fromRunpy.toString().split("\n");
        const str = fromRunpy[1];
        const p = fromRunpy[2];
        const q = fromRunpy[3];
        const n = fromRunpy[4];
        const x = fromRunpy[5];
        const a = fromRunpy[6];
        const guess = fromRunpy[7];
        console.log(str);

        res.render("flip", {str:str, p:p, q:q, n:n, x:x, a:a, guess:guess});

        //res.end(fromRunpy);
    }).catch((error) => {
    console.error(error);
  });


});









app.listen(3000, function(){
  console.log("Server is running on port 3000");
});
