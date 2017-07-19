const mongoose = require('mongoose')
const Schema = mongoose.Schema
const ObjectId = Schema.ObjectId

module.exports = new Schema({
  _id: ObjectId,
  name: String
})
