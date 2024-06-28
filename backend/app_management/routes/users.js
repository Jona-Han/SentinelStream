const express = require('express')
const router = express.Router()

const userService = require('../services/user_service')

router.get('/:userid', async (req, res) => {
    const user = await userService.getUserById(req.params.userid)
    console.log(user)
    res.send("Success").status(200)
})

router.put('/:userid', async (req, res) => {
    res.send(req.params.userid)
})

router.delete('/:userid', async (req, res) => {
    res.send(req.params.userid)
})

router.post('/', async (req, res) => {
    res.send('Post')
})

module.exports = router