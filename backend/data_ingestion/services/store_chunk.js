const redisClient = require('../utils/redis')

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

module.exports = storeChunkWithRetry
