const Joi = require('joi')

const schema = Joi.object({
    chunkNumber: Joi.number().integer().positive().min(1).max(10).required(),
})

const validate = (req, res, next) => {
    const { error } = schema.validate(req.body)

    if (error) {
        return res
            .status(400)
            .json({ error: `Validation error: ${error.details[0].message}` })
    }

    next()
}

module.exports = validate
