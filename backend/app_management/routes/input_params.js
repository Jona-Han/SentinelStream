const express = require('express')
const router = express.Router()

router.get('/:inputid', async (req, res) => {
    res.send("Success").status(200)
})

router.put('/:inputid', async (req, res) => {
    res.send(req.params.inputid)
})

router.delete('/:inputid', async (req, res) => {
    res.send(req.params.inputid)
})

router.post('/', async (req, res) => {
    res.send('Post')
})

module.exports = router