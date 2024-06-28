const express = require('express')
const router = express.Router()

const usersRouter = require('./users')

router.use('/app-manager/v0/users', usersRouter)

module.exports = router