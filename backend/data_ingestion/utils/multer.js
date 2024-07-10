const multer = require('multer')

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

module.exports = upload
