<script setup lang="ts">
import { computed, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useExchangeStore } from '@/stores/exchange'

interface Whisky {
  purchased: string
  name: string
  price: string
  store: string
  category?: string
  country?: string
  flavor?: string
  critic?: string
  score: number
  cost?: string
  reviewers?: string,
  cluster?: string,
  type?: string,
  stdev?: string
}

const endpoint: string = import.meta.env.VITE_API_ENDPOINT;

const search = ref('')
const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900'])
const dialogFormVisible = ref(false)
const tableData = ref<Whisky[]>([])
const database = ref<Whisky[]>([])
const form = reactive({
  name: '',
  price: '',
  purchased: '',
  store: '',
  score: 0
})
const selected = ref<null | Whisky>(null)
const storeExchange = useExchangeStore()

const filterTableData = computed(() =>
  tableData.value.filter(
    (data) =>
      !search.value ||
      data.name.toLowerCase().includes(search.value.toLowerCase())
  )
)
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? database.value.filter(createFilter(queryString))
    : database.value
  cb(results)
}
const createFilter = (queryString: string) => {
  return (whisky: Whisky) => {
    return (
      whisky.name.toLowerCase().indexOf(queryString.toLowerCase()) !== -1
    )
  }
}
const isBargain = computed(() => (price: string, cost: string) => {
  const p = parseInt(price)
  if (cost == "$$" && p / storeExchange.cad_jpy < 30) {
    return true
  } else if (cost == "$$$" && p / storeExchange.cad_jpy < 50) {
    return true
  } else if (cost == "$$$$" && p / storeExchange.cad_jpy < 70) {
    return true
  } else if (cost == "$$$$$" && p / storeExchange.cad_jpy < 125) {
    return true
  } else if (cost == "$$$$$+" && p / storeExchange.cad_jpy < 300) {
    return true
  }
  return false
})
const isExpensive = computed(() => (price: string, cost: string) => {
  const p = parseInt(price)
  if (cost == "$" && p / storeExchange.cad_jpy > 30) {
    return true
  } else if (cost == "$$" && p / storeExchange.cad_jpy > 50) {
    return true
  } else if (cost == "$$$" && p / storeExchange.cad_jpy > 70) {
    return true
  } else if (cost == "$$$$" && p / storeExchange.cad_jpy > 125) {
    return true
  } else if (cost == "$$$$$" && p / storeExchange.cad_jpy > 300) {
    return true
  }
  return false
})

const handleAppend = () => {
  dialogFormVisible.value = true
}
const handleDelete = (index: number, row: Whisky) => {
  console.log(index)
  tableData.value.splice(index)
  updateStorage()
}
const handleCancel = () => {
  dialogFormVisible.value = false
  selected.value = null
  form.name = ""
  form.price = ""
  form.purchased = ""
  form.store = ""
  form.score = 0
}
const handleConfirm = () => {
  tableData.value.push({
    purchased: form.purchased,
    name: form.name,
    price: form.price,
    store: form.store,
    score: form.score,
    ...selected.value
  })
  form.name = ""
  form.price = ""
  form.purchased = ""
  form.store = ""
  form.score = 0
  dialogFormVisible.value = false
  updateStorage()
}
const handleSelect = (item: Whisky) => {
  selected.value = item
  if (form.price == "") {
    if (item.cost == "$") {
      form.price = String(Math.floor(20 * storeExchange.cad_jpy))
    } else if (item.cost == "$$") {
      form.price = String(Math.floor(40 * storeExchange.cad_jpy))
    } else if (item.cost == "$$$") {
      form.price = String(Math.floor(60 * storeExchange.cad_jpy))
    } else if (item.cost == "$$$$") {
      form.price = String(Math.floor(100 * storeExchange.cad_jpy))
    } else if (item.cost == "$$$$$") {
      form.price = String(Math.floor(200 * storeExchange.cad_jpy))
    } else if (item.cost == "$$$$$+") {
      form.price = String(Math.floor(300 * storeExchange.cad_jpy))
    }
  }
  console.log(item)
}
const updateStorage = () => {
  axios.put(`${endpoint}/storage`, tableData.value)
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error);
    })
  console.log(tableData.value)
}

onMounted(() => {
  axios.get(`${endpoint}/database`)
    .then((response) => {
      database.value = response.data
    })
    .catch((error) => {
      console.log(error);
    })
  axios.get(`${endpoint}/storage`)
    .then((response) => {
      tableData.value = response.data
    })
    .catch((error) => {
      console.log(error);
    })
})
</script>

<template>
  <main>
    Search: <el-input v-model="search" size="small" placeholder="Type to search" style="width: 20em;" />
    <el-table :data="filterTableData" style="width: 100%">
      <el-table-column label="Date of Purchase" prop="purchased" />
      <el-table-column label="Name" prop="name" />
      <el-table-column label="Price" prop="price">
        <template #default="scope">
          <span>{{ scope.row.price }}</span>
          <span>{{ isBargain(scope.row.price, scope.row.cost) ? " (Bargain)" : "" }}</span>
          <span>{{ isExpensive(scope.row.price, scope.row.cost) ? " (Expensive)" : "" }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Liquor Store" prop="store" />
      <el-table-column label="Class" prop="category" />
      <el-table-column label="Country" prop="country" />
      <el-table-column label="Flavor" prop="flavor">
        <template #default="scope">
          <span v-if="scope.row.flavor == 'A'">Full-bodied, sweet, pronounced sherry</span>
          <span v-if="scope.row.flavor == 'B'">Full-bodied, sweet, pronounced sherry</span>
          <span v-if="scope.row.flavor == 'C'">Full-bodied, sweet, pronounced sherry</span>
          <span v-if="scope.row.flavor == 'E'">Medium-bodied, medium-sweet</span>
          <span v-if="scope.row.flavor == 'F'">Full-bodied, sweet and malty</span>
          <span v-if="scope.row.flavor == 'G'">Light-bodied, sweet, apéritif-style</span>
          <span v-if="scope.row.flavor == 'H'">Very light-bodied, sweet, apéritif-style</span>
          <span v-if="scope.row.flavor == 'I'">Medium-bodied, medium-sweet, quite smoky</span>
          <span v-if="scope.row.flavor == 'J'">Full-bodied, dry, very smoky, pungent</span>
        </template>
      </el-table-column>
      <el-table-column label="Meta Critic" prop="critic" />
      <el-table-column label="Your Score" prop="score">
        <template #default="scope"><el-rate v-model="scope.row.score" :colors="colors" @click="updateStorage" /></template>
      </el-table-column>
      <el-table-column align="right">
        <template #header>
          <el-button size="default" @click="handleAppend()">Append</el-button>
        </template>
        <template #default="scope">
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </main>
  <el-dialog v-model="dialogFormVisible" title="Append new whisky" width="500">
    <el-form :model="form">
      <el-form-item label="Name">
        <el-autocomplete
          v-model="form.name"
          :fetch-suggestions="querySearch"
          value-key="name"
          clearable
          class="inline-input w-50"
          placeholder="Please Input"
          @select="handleSelect"
        />
      </el-form-item>
      <el-form-item label="Price (JPY)">
        <el-input v-model="form.price">
          <template #prepend>¥</template>
        </el-input>
      </el-form-item>
      <el-form-item label="Date of Purchase">
        <el-date-picker
          v-model="form.purchased"
          type="date"
          placeholder="Pick a day"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="Liquor Store">
        <el-input v-model="form.store" />
      </el-form-item>
      <el-form-item label="Your Score">
        <el-rate v-model="form.score" :colors="colors" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">Cancel</el-button>
        <el-button type="primary" @click="handleConfirm" :disabled="!selected">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
