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
const dialogFormVisible = ref(false)
const dialogForm2Visible = ref(false)
const tableData = ref<Whisky[]>([])
const database = ref<Whisky[]>([])
const form = reactive({
  name: '',
  price: '',
  purchased: '',
  store: '',
  score: 0
})
const form2 = reactive({
  name: '',
  apikey: '',
  hits: 0,
  max: 0,
  min: 0,
  shops: []
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

const handleAppend = () => {
  dialogFormVisible.value = true
}
const handleCheck = (index: number, row: Whisky) => {
  console.log(index)
  dialogForm2Visible.value = true
  form2.name = row.name
  form2.max = 0
  form2.min = 0
  form2.shops = []
}
const handleDelete = (index: number, row: Whisky) => {
  console.log(index)
  tableData.value.splice(index)
  updateWishlist()
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
const handleCancel2 = () => {
  dialogForm2Visible.value = false
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
  updateWishlist()
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
const handleSearch = () => {
  axios.get(`https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&keyword=${encodeURIComponent(form2.name)}&applicationId=${form2.apikey}`)
    .then((response) => {
      console.log(response.data)
      form2.hits = response.data.hits
      if (response.data.Items.length > 0) {
        form2.max = Math.max(...response.data.Items.map((x: any) => x.Item.itemPrice))
        form2.min = Math.min(...response.data.Items.map((x: any) => x.Item.itemPrice))
        form2.shops = response.data.Items.map((x: any) => x.Item.shopName)
        form2.shops = form2.shops.filter((element: never, index: number) => {
          return form2.shops.indexOf(element) == index
        })
      }
    })
    .catch((error) => {
      console.log(error);
    })
}
const updateWishlist = () => {
  axios.put(`${endpoint}/wishlist`, tableData.value)
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
  axios.get(`${endpoint}/wishlist`)
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
      <el-table-column label="Name" prop="name" />
      <el-table-column label="Price" prop="price">
        <template #default="scope">
          <span>{{ scope.row.price }}</span>
        </template>
      </el-table-column>
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
      <el-table-column align="right">
        <template #header>
          <el-button size="default" @click="handleAppend()">Append</el-button>
        </template>
        <template #default="scope">
          <el-button
            size="small"
            @click="handleCheck(scope.$index, scope.row)"
          >
            Check
          </el-button>
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
  <el-dialog v-model="dialogForm2Visible" title="Check whisky in store" width="500">
    <el-form :model="form2">
      <el-form-item label="Name">
        <el-input v-model="form2.name" disabled />
      </el-form-item>
      <el-form-item label="Rakuten Application ID">
        <el-input v-model="form2.apikey" />
      </el-form-item>
    </el-form>
    <div style="display: flex;">
      <el-statistic title="Hits" :value="form2.hits" />
      <el-statistic title="Max Price" :value="form2.max" style="margin-left: 2em;" />
      <el-statistic title="Min Price" :value="form2.min" style="margin-left: 2em;" />
    </div>
    <div>
      <el-tag v-for="shop in form2.shops">{{ shop }}</el-tag>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel2">Cancel</el-button>
        <el-button type="primary" @click="handleSearch" :disabled="form2.apikey == ''">
          Search
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
