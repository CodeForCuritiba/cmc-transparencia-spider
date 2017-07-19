<template>
  <div class="modal is-active">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ entity.name }}</p>
        <button @click="$emit('close')" class="delete"></button>
      </header>
      <section class="modal-card-body">
        <salary-chart :labels="labels" :data="data" :height="200"></salary-chart>
      </section>
    </div>
  </div>
</template>

<script>
import SalaryChart from './charts/SalaryChart'

export default {
  props: ['entity'],
  components: {
    SalaryChart
  },
  mounted () {

  },
  computed: {
    labels () {
      const meses = Object.keys(this.entity.salaries)
      meses.sort()

      return meses
    },
    data () {
      const data = []

      Object.keys(this.entity.salaries).forEach((key) => {
        data.push(this.entity.salaries[key].gross)
      })

      return data
    }
  }
}
</script>

<style scoped>
</style>
