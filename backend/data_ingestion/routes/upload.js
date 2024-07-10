const express = require('express')
const { v4: uuidv4 } = require('uuid')
const startUploadValidator = require('../validators/start_upload')
const chunkValidator = require('../validators/chunk_upload')
const pg_pool = require('../utils/rdb')
const redisClient = require('../utils/redis')
const upload = require('../utils/multer')
const storeChunkWithRetry = require('../services/store_chunk')

const router = express.Router()

router.post('/start-upload', startUploadValidator, async (req, res) => {
    const { fileName, fileSize, totalChunks } = req.body
    const uploadId = uuidv4()
    const metadata = {
        fileName,
        fileSize,
        totalChunks,
        receivedChunks: 0,
        chunks: Array(totalChunks).fill(false), // Track received chunks
    }

    try {
        await redisClient.expire(uploadId, 3600)
        await redisClient.set(uploadId, JSON.stringify(metadata))
        res.status(201).json({ data: uploadId })
    } catch (err) {
        console.error('Error initiating upload session:', err)
        res.status(500).json({ error: 'Could not initiate upload session' })
    }
})

router.post(
    '/upload-whole/:uploadid',
    upload.single('file'),
    async (req, res) => {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' })
        }
        const { uploadId } = req.params
        const { originalname, mimetype, size, filename } = req.file
        console.log(
            `File uploading: ${originalname}, ${filename}, ${mimetype}, ${size} bytes`
        )

        try {
            const metadata = await redisClient.get(uploadId)
            if (!metadata) {
                return res
                    .status(404)
                    .json({ error: 'Upload session expired or not found' })
            }

            const query =
                'INSERT INTO models (uuid, model_data, name, size) VALUES ($1, $2, $3, $4)'
            const values = [uploadId, req.file.buffer, filename, size]

            const res = await pg_pool.query(query, values)

            // Todo: Delete upload data in redis

            res.status(201).json({ data: res })
        } catch (err) {
            res.status(500).json({ error: err.message })
        }
    }
)

router.post(
    '/upload-chunk/:uploadid',
    chunkValidator,
    upload.single('file'),
    async (req, res) => {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' })
        }

        const { uploadId } = req.params
        const { chunkNumber } = req.body
        const chunk = req.file.buffer

        try {
            const chunkKey = `${uploadId}-${chunkNumber}.chunk`
            await storeChunkWithRetry(
                uploadId,
                chunkKey,
                chunk,
                chunkNumber,
                res
            )
        } catch (err) {
            console.error('Error:', err)
            res.status(500).json({ error: err })
        }
    }
)

module.exports = router
