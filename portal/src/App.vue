<template>
  <div id="app" class="container">

    <loader v-if="loading"></loader>

    <div class="buttons">
      <h1 class="title">Selecione um Tipo</h1>

      <button class="button" :class="{ 'is-primary' : (selectedEntity === 1) }"  @click="showData(1)">Vereadores</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 2) }"  @click="showData(2)">Efetivos</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 3) }"  @click="showData(3)">Comissionados</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 4) }"  @click="showData(4)">Inativos</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 5) }"  @click="showData(5)">Ouvidor</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 6) }"  @click="showData(6)">Cedido para a Câmara</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 7) }"  @click="showData(7)">Cedido pela Câmara</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 8) }"  @click="showData(8)">Temporário</button>
      <button class="button" :class="{ 'is-primary' : (selectedEntity === 9) }"  @click="showData(9)">Estagiário</button>

      <entity-grid v-if="this.loaded" :data="data"></entity-grid>

    </div>
  </div>
</template>

<script>
import Loader from './components/Loader'
import EntityGrid from './components/EntityGrid'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    Loader,
    EntityGrid
  },
  data () {
    return {
      loading: false,
      loaded: false,
      selectedEntity: 0,
      data: false
    }
  },
  methods: {
    showData (entityId) {
      const vue = this

      this.selectedEntity = entityId
      this.loading = true
      this.loaded = false

      const url = `/api/entities/${this.selectedEntity}/`
      // const url = `/static/estagiarios.json`

      axios.get(url)
        .then((response) => {
          vue.loading = false
          vue.loaded = true
          vue.data = response.data
        })
        .catch((error) => {
          console.warn(error)
          vue.loading = false
        })
    }
  }
}
</script>

<style lang="scss">
@import 'scss/app.scss';
</style>
