/*jslint devel: true */ 
/* eslint-disable no-console */ 
/*eslint no-undef: "error"*/ 
/*eslint-env node*/

const express = require('express');
//const db = require(`./util/db`); // import db pool
const http = require('http');
const bodyParser= require('body-parser');
const app = express();

app.set('port',process.env.PORT || 3000);
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());



app.use((req, res, next) => {
    console.log('첫 번째 미들웨어 호출 됨');
    console.log(req.header);
});

const server = http.createServer(app).listen(app.get('port'),function(){
    console.log("익스프레스로 웹 서버를 실행함 : "+ app.get('port')); 

    // db test code 
    // db.execute(`SELECT * FROM welfare_detail`)
    // .then((result)=>{
    //     console.log(result);
    // })
 });



// DB Test Code
// db.execute(`SELECT * FROM welfare_detail`)
// .then((result)=>{
//     console.log(result);
// })
// .catch((err)=>{
//     console.log(err);
// });
