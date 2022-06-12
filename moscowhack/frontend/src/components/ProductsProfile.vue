<template>
  <div>
    <input v-model="text" @keyup.enter="applySearchProducts">
    <button @click="applySearchProducts"> Поиск </button>
    <div v-if="productsProfile.length > 0">
      <div class="product" v-for="product in productsProfile" :key="product">
        <div v-for="(key, value) in product" :key="key">
          <b>{{ value }}</b>: {{ key }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>


export default {
  data() {
    return {
      text: '',
      productsProfile: [],
      productsProfileErrorStatus: null,
    };
  },
  name: "MoscowProduct",
  methods: {
    async getProductsProfile(company_inn) {
      let response = await fetch(
          `http://127.0.0.1:8000/product/get/${company_inn}`,
          {method: 'GET'}
      )
      if (response.ok) {
        this.productsProfile = await response.json()
      }
      else {
        this.productsProfileErrorStatus = response.status
      }
    },
    async applySearchProducts() {
      await this.getProductsProfile(this.text)
    }
  },
};
</script>

<style scoped>
.product {
  margin: 20px;
  padding: 20px;
  border: 2px solid black;
  text-align: left;
}
</style>
