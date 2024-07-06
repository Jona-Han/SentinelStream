const express = require('express')
const app = express()
const config = require('./config/config')

const uploadRouter = require('./routes/upload')

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.use('/ingestion/v0', uploadRouter)

app.listen(config.port, () => {
    console.log(`Api listening at http://localhost:${config.port}`)
})
