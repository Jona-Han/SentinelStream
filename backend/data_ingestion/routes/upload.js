const express = require('express')
const redis = require('redis')
const multer = require('multer')
const { v4: uuidv4 } = require('uuid')
const startUploadValidator = require('../validators/start_upload')
const chunkValidator = require('../validators/chunk_upload')

const fileFilter = (_, file, cb) => {
    // Reject files with a mimetype other than csv
    if (file.mimetype === 'text/csv') {
        cb(null, true)
    } else {
        cb(new Error('Only csv files are allowed'), false)
    }
}

const storage = multer.memoryStorage()
const upload = multer({
    storage,
    fileFilter,
    limits: {
        files: 1, // Maximum of 1 files per request
    },
})

const router = express.Router()
const redisClient = redis.createClient()

redisClient.on('error', (err) => {
    console.error('Redis error:', err)
})

redisClient.connect().then(() => {
    console.log('Connected to Redis')
})

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
        await redisClient.set(uploadId, JSON.stringify(metadata))
        res.json({ uploadId })
    } catch (err) {
        console.error('Error initiating upload session:', err)
        res.status(500).json({ error: 'Could not initiate upload session' })
    }
})

router.post('/upload-all/:uploadid', async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' })
    }
    const { uploadId } = req.params
    const { originalname, mimetype, size, filename } = req.file
    console.log(`File uploaded: ${originalname}, ${filename}, ${mimetype}, ${size} bytes`)
})

router.post('/upload-chunk/:uploadid', chunkValidator, async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' })
    }

    const { uploadId } = req.params
    const { chunkNumber } = req.body
    const chunk = req.file.buffer

    try {
        const chunkKey = `${uploadId}-${chunkNumber}.chunk`
        await storeChunkWithRetry(uploadId, chunkKey, chunk, chunkNumber, res)
    } catch (err) {
        console.error('Error:', err)
        res.status(500).json({ error: 'Internal server error' })
    }
})

async function storeChunkWithRetry(
    uploadId,
    chunkKey,
    chunk,
    chunkNumber,
    res,
    retries = 5
) {
    let attempt = 0
    let success = false

    while (attempt < retries && !success) {
        try {
            attempt++
            await redisClient.watch(uploadId)

            const metadata = await redisClient.get(uploadId)
            if (!metadata) {
                return res
                    .status(404)
                    .json({ error: 'Upload session not found' })
            }

            const parsedMetadata = JSON.parse(metadata)
            if (parsedMetadata.chunks[chunkNumber - 1] === false) {
                const transaction = redisClient.multi()
                transaction.set(chunkKey, chunk)
                parsedMetadata.chunks[chunkNumber - 1] = true
                parsedMetadata.receivedChunks++
                transaction.set(uploadId, JSON.stringify(parsedMetadata))

                const results = await transaction.exec()

                if (results === null) {
                    console.log(
                        `Transaction failed due to a change in the watched keys. Retry attempt ${attempt}/${retries}.`
                    )
                } else {
                    console.log('Transaction succeeded:', results)
                    success = true
                }
            } else {
                return res.status(400).json({ error: 'Chunk already uploaded' })
            }
        } catch (err) {
            console.error('Error performing transaction:', err)
        } finally {
            await redisClient.unwatch()
        }
    }

    if (!success) {
        return res
            .status(500)
            .json({ error: 'Transaction failed after maximum retry attempts' })
    } else {
        return res.status(200).json({ message: 'Chunk uploaded successfully' })
    }
}

module.exports = router
