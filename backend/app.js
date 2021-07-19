const express = require('express');
const bodyParser= require('body-parser');
const user_router = require('./controller/user');

const app = express();

app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

app.use(user_router);

app.listen(3000);

