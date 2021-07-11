const db = require(`./util/db`); // import db pool

module.exports = class User {
  constructor(id, password, gender, age, address, life_cycle, family, income_quintile, disabled, veterans) {
    this.id = id;
    this.password = password;
    this.gender = gender;
    this.age = age;
    this.address = address;
    this.life_cycle = life_cycle;
    this.family = family;
    this.income_quintile = income_quintile;
    this.disabled = disabled;
    this.veterans = veterans
  }

  log_in() {
  }

  log_out(){

  }

};