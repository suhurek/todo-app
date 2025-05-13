<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card>
      <v-card-title>
        {{ isEdit ? "カテゴリの編集" : "新しいカテゴリ" }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="categoryData.name"
          label="カテゴリ名"
          variant="outlined"
          class="mb-4"
        ></v-text-field>
        <v-color-picker
          v-model="categoryData.color"
          hide-inputs
          hide-canvas
          show-swatches
          swatches-max-height="200px"
        ></v-color-picker>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" variant="text" @click="cancel"> キャンセル </v-btn>
        <v-btn
          color="primary"
          variant="text"
          @click="save"
          :disabled="!categoryData.name"
        >
          保存
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "CategoryDialog",
  props: {
    category: {
      type: Object,
      default: () => ({ name: "", color: "#4CAF50" }),
    },
    visible: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      categoryData: { name: "", color: "#4CAF50" },
    };
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible;
      },
      set(value) {
        if (!value) {
          this.$emit("update:visible", false);
        }
      },
    },
  },
  watch: {
    category: {
      handler(newCategory) {
        this.categoryData = { ...newCategory };
      },
      immediate: true,
    },
  },
  methods: {
    save() {
      if (!this.categoryData.name.trim()) return;
      this.$emit("save", this.categoryData);
    },
    cancel() {
      this.$emit("cancel");
    },
  },
};
</script>
