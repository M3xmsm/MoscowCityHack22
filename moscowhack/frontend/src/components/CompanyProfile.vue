<template>
  <div>
    <input v-model="text" @keyup.enter="applySearchInn">
    <button @click="applySearchInn"> Поиск</button>
    <div class="company">
      <div v-for="(key, value) in companyProfile" :key="key"><b>{{ value }}</b>: {{ key }}</div>
    </div>
  </div>
</template>

<script>


export default {
  data() {
    return {
      text: '',
      companyProfile: null,
      companyProfileErrorStatus: null,
    };
  },
  name: "CompanyProfile",
  methods: {
    async getCompanyProfile(company_inn) {
      let response = await fetch(
          `http://127.0.0.1:8000/company/get/${company_inn}`,
          {method: 'GET'}
      )
      if (response.ok) {
        this.companyProfile = await response.json()
      }
      else {
        this.companyProfileErrorStatus = response.status
      }
    },
    async applySearchInn() {
      await this.getCompanyProfile(this.text)
    }
  },
};
</script>

<style scoped>
.company {
  margin: 20px;
  padding: 20px;
  border: 2px solid black;
  text-align: left;
}
</style>

