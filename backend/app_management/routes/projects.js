const express = require('express')
const router = express.Router()

router.get('/:pid', async (req, res) => {
    res.send("Success").status(200)
})

router.put('/:pid', async (req, res) => {
    res.send(req.params.pid)
})

router.delete('/:pid', async (req, res) => {
    res.send(req.params.pid)
})

router.post('/', async (req, res) => {
    res.send('Post')
})

module.exports = router