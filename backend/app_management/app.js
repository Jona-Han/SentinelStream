const express = require('express')
const app = express()
const config = require('./config/config')
const indexRouter = require('./routes/index')

app.use('/', indexRouter)

app.listen(config.port, () => {
  console.log(`Api listening at http://localhost:${config.port}`)
})
