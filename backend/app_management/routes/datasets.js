const express = require('express')
const router = express.Router({ mergeParams: true })

router.get('/:did', async (req, res) => {
    res.send("Success").status(200)
})

router.put('/:did', async (req, res) => {
    res.send(req.params.did)
})

router.delete('/:did', async (req, res) => {
    res.send(req.params.did)
})

router.post('/', async (req, res) => {
    res.send('Post')
})

module.exports = router