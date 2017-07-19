import { Bar } from 'vue-chartjs'

export default Bar.extend({
  props: ['labels', 'data'],
  mounted () {
    const vue = this

    this.renderChart({
      labels: vue.labels,
      datasets: [
        {
          label: 'Salário',
          backgroundColor: '#f87979',
          data: vue.data
        }
      ]
    })
  }
})
