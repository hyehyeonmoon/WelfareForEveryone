const mysql = require(`mysql2`); // import mysql module

// Create one connection -> have to run every queries (each query has one connection)
// So we create pool -> can handle many queries
const pool = mysql.createPool({
    host : `34.64.116.88`,
    user : `root`,
    database : `welfare-for-everyone`,
    password : `1357`
}); // need object about db

module.exports = pool.promise();
