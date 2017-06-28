const fs = require('fs')
const _ = require('lodash')
const marked = require('marked')

const MDTable = require('markdown-table')
const file = process.argv[2]

fs.exists(file, (exists) => {
    if (!exists) {
        throw new Error(`File ${file} not exists!`)
    }

    fs.readFile(file, 'utf8', (err, data) => {
        if (err) throw err

        transform(data)
    })
})

function getItemChildAttribute(attr, item, cb) {
    _.each(item, (piece) => {
        cb(piece[attr])
    })
}

function transform (data) {
    let tableData = []

    itens = JSON.parse(data)

    // Grab header data
    let headers = []
    _.each(_.keys(itens[0]), (key) => {
        const value = itens[0][key]

        if (typeof value === 'object') {
            getItemChildAttribute('name', value, (attr) => {
                headers.push(attr)
            })
        } else {
            headers.push(key)
        }
    })

    tableData.push(headers)

    // Raw Data
    _.each(itens, (item, index) => {
        let dataArray = [];

        _.each(_.keys(itens[0]), (key) => {
            const value = itens[0][key]

            if (typeof value === 'object') {
                getItemChildAttribute('value', value, (attr) => {
                    dataArray.push(attr)
                })
            } else {
                dataArray.push(value)
            }
        })

        tableData.push(dataArray)
    })

    const table = MDTable(tableData)
    const html = marked(table)

    console.log(html)
}

