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
    port: process.env.PORT,
    db: {
        user: process.env.DB_USER,
        host: process.env.DB_HOST,
        database: process.env.DB_NAME,
        password: process.env.DB_PASS,
        port: process.env.DB_PORT,
        max: 10, // maximum number of clients in the pool
        idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
      },
}

module.exports = config
