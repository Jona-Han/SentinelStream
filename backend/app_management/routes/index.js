const express = require('express')
const router = express.Router()

const usersRouter = require('./users')
const projectsRouter = require('./projects')
const datasetsRouter = require('./datasets')
const modelsRouter = require('./models')
const inputParamsRouter = require('./input_params')
const deployablesRouter = require('./deployables')

router.use('/app-manager/v0/users', usersRouter)
router.use('/app-manager/v0/projects', projectsRouter)
router.use('/app-manager/v0/projects/:pid/datasets', datasetsRouter)
router.use('/app-manager/v0/projects/:pid/models', modelsRouter)
router.use('/app-manager/v0/projects/:pid/input_paramas', inputParamsRouter)
router.use('/app-manager/v0/projects/:pid/deployables', deployablesRouter)

module.exports = router