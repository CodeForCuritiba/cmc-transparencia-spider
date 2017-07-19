const mongoose = require('mongoose')

const DefaultSchema = require('./default')

module.exports = {
  vereadores         : mongoose.model('Vereador', DefaultSchema, 'vereadores'),
  efetivos           : mongoose.model('Efetivo', DefaultSchema, 'efetivos'),
  comissionados      : mongoose.model('Comissionado', DefaultSchema, 'comissionados'),
  inativos           : mongoose.model('Inativo', DefaultSchema, 'inativos'),
  ouvidores          : mongoose.model('Ouvidor', DefaultSchema, 'ouvidores'),
  cedidos_para_camara: mongoose.model('Cedido_para_camara', DefaultSchema, 'cedidos_para_camara'),
  cedidos_pela_camara: mongoose.model('Cedido_pela_camara', DefaultSchema, 'cedidos_pela_camara'),
  temporarios        : mongoose.model('Temporario', DefaultSchema, 'temporarios'),
  estagiarios        : mongoose.model('Estagiario', DefaultSchema, 'estagiarios')
}
