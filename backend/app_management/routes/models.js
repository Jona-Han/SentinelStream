const express = require('express')
const router = express.Router()

router.get('/:mid', async (req, res) => {
    res.send("Success").status(200)
})

router.put('/:mid', async (req, res) => {
    res.send(req.params.mid)
})

router.delete('/:mid', async (req, res) => {
    res.send(req.params.mid)
})

router.post('/', async (req, res) => {
    res.send('Post')
})

module.exports = router