const fs = require('fs')
const path = require('path')
const dotenv = require('dotenv')

const env = process.env.NODE_ENV || 'development'
const envFile = `.env.${env}`

if (fs.existsSync(path.join(__dirname, envFile))) {
    dotenv.config({ path: path.join(__dirname, envFile) })
} else {
    dotenv.config()
}

const config = {
    port: process.env.PORT || 4001,
    redis_url: process.env.REDIS_URL || 'localhost:6379',
}

module.exports = config
