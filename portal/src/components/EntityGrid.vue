<template>
  <div class="entity-grid">
    <entity-modal v-if="showEntityModal" @close="closeEntityModal" :entity="selectedEntity"></entity-modal>

    <table class="table is-bordered is-striped is-narrow">
      <thead>
        <tr>
          <th>Ações</th>
          <th>Código</th>
          <th>Nome</th>
          <th>Salário</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entity in data">
          <td>
            <button @click="showEntity(entity)" class="button is-small is-info">
              <i class="fa fa-search"></i>
            </button>
          </td>
          <td>{{ entity.id }}</td>
          <td>{{ entity.name }}</td>
          <td>R$ {{ entity | lastSalary }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import EntityModal from '@/components/EntityModal'

/* eslint-disable no-unused-vars */
function getCurrenctSalary (entity) {

}

export default {
  filters: {
    lastSalary (entity) {
      const keys = Object.keys(entity.salaries)
      keys.sort()

      return entity.salaries[keys[0]].gross
    }
  },
  props: ['data'],
  components: {
    EntityModal
  },
  data () {
    return {
      showEntityModal: false,
      selectedEntity: null
    }
  },
  methods: {
    showEntity (entity) {
      this.showEntityModal = true
      this.selectedEntity = entity
    },
    closeEntityModal () {
      this.showEntityModal = false
      this.selectedEntity = null
    }
  }
}
</script>

<style scoped>
.entity-grid{
  margin-top: 12px;
}
</style>
