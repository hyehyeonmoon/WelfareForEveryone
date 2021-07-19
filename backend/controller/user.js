const express = require('express');
const user_method = require('../model/user');
const User_Router = express.Router();


User_Router.post('/userLogin', (req, res, next) => {
    user_method.login(req.body.id, req.body.pw)
    .then((user)=>{
        if (user[0].length == 0){
            const approve ={'result':'Failed'};
            res.send(approve);
        }
        else{
            const approve ={'result':'Successful'};
            res.send(approve);
        }
    })
});

User_Router.post('/userLogout', (req, res, next) => {
    const approve ={'result':'Successful'};
    res.send(approve);
});
  
User_Router.post('/userRegister', (req, res, next) => {
    user_method.register(req.body.id, req.body.pw, req.body.gender, req.body.age, req.body.adress, req.body.life_cycle, req.body.family, req.body.income_quintile, req.body.disabled, req.body.veteran)
    .then((result)=>{
        console.log(result);
        const approve ={'result':'Successful'};
        res.send(approve);
    });
});

module.exports = User_Router;


// res.setHeader('Content-Type', 'text/html');
// res.write("Logout");
// res.end();
