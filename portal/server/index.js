const express = require('express')
const mongoose = require('mongoose')
const Schemas = require('./schemas')
const config = require('./config')

const mongodbUri = process.env.MONGODB_URI || 'mongodb://localhost/camara'

// Database
mongoose.connect(mongodbUri)

const app = express()

// Static vue portal
app.use(express.static('dist'))


// routes
app.get('/api/entities/:entityId', (req, res) => {
  const entityId = req.params.entityId
  const entityName = config.entities_types[entityId]

  const entity = Schemas[entityName]

  entity.find({}, (err, docs) => {
      if (err)
        return res.send(err)

      return res.send(docs)
  })
})

// Start
const PORT = process.env.APP_PORT || 3000

app.listen(PORT, () => {
  console.log('Server started at port:', PORT)
})
