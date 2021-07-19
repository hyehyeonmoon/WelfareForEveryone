const db = require(`../util/db`); // import db pool

module.exports.register = () => {
  return db.execute(
    'INSERT INTO user (user_id, user_password, user_gender, user_age, user_address, user_life_cycle, user_family, user_income_quintile, user_is_disabled, user_is_veterans) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    [this.user_id, this.user_password, this.user_gender, this.user_age, this.user_address, this.user_life_cycle, this.user_family, this.user_income_quintile, this.user_is_disabled, this.user_is_veterans]
  );
}

module.exports.login = () => {
  return db.execute('SELECT * FROM user WHERE user_id = ? AND user_password = ?', [id, pw]);
}

// module.exports = class User {
//   constructor(id, password, gender, age, address, life_cycle, family, income_quintile, disabled, veterans) {
//     this.user_id = id;
//     this.user_password = password;
//     this.user_gender = gender;
//     this.user_age = age;
//     this.user_address = address;
//     this.user_life_cycle = life_cycle;
//     this.user_family = family;
//     this.user_income_quintile = income_quintile;
//     this.user_is_disabled = disabled;
//     this.user_is_veterans = veterans
//   }

//   register(){
//     return db.execute(
//       'INSERT INTO user (user_id, user_password, user_gender, user_age, user_address, user_life_cycle, user_family, user_income_quintile, user_is_disabled, user_is_veterans) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
//       [this.user_id, this.user_password, this.user_gender, this.user_age, this.user_address, this.user_life_cycle, this.user_family, this.user_income_quintile, this.user_is_disabled, this.user_is_veterans]
//     );
//   }
//   static login(id, pw) {
//     return db.execute('SELECT * FROM user WHERE user_id = ? AND user_password = ?', [id, pw]);
//   }
// };