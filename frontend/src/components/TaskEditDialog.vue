<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card v-if="taskData">
      <v-card-title>タスクの編集</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="taskData.title"
          label="タスク名"
          variant="outlined"
          class="mb-4"
        ></v-text-field>

        <v-textarea
          v-model="taskData.description"
          label="詳細説明（任意）"
          variant="outlined"
          rows="4"
          class="mb-4"
        ></v-textarea>

        <!-- カテゴリ選択（カスタム実装） -->
        <div class="mb-4">
          <label class="text-subtitle-1 mb-2 d-block">カテゴリ</label>

          <v-menu v-model="categoryMenuOpen" :close-on-content-click="false">
            <template v-slot:activator="{ props }">
              <v-chip
                variant="outlined"
                v-bind="props"
                label
                class="pa-2"
                size="large"
                prepend-icon="mdi-tag"
              >
                <template v-slot:prepend>
                  <div
                    v-if="selectedCategory"
                    :style="{
                      backgroundColor: selectedCategory.color,
                      width: '16px',
                      height: '16px',
                      display: 'inline-block',
                      borderRadius: '50%',
                      marginRight: '4px',
                    }"
                  ></div>
                </template>
                {{ selectedCategory ? selectedCategory.name : "カテゴリなし" }}
              </v-chip>
            </template>

            <v-card min-width="200">
              <v-list>
                <v-list-item
                  @click="selectCategory(null)"
                  :active="taskData.category_id === null"
                >
                  <template v-slot:prepend>
                    <div class="position-relative d-flex align-center">
                      <div
                        :style="{
                          backgroundColor: 'grey',
                          opacity: 0.3,
                          width: '24px',
                          height: '24px',
                          display: 'inline-block',
                          borderRadius: '50%',
                          marginRight: '8px',
                        }"
                      ></div>
                      <v-icon
                        v-if="taskData.category_id === null"
                        size="x-small"
                        color="white"
                        class="category-check-icon"
                      >
                        mdi-check
                      </v-icon>
                    </div>
                  </template>
                  <v-list-item-title>カテゴリなし</v-list-item-title>
                </v-list-item>

                <v-list-item
                  v-for="category in uniqueCategories"
                  :key="category.id"
                  @click="selectCategory(category)"
                  :active="taskData.category_id === category.id"
                >
                  <template v-slot:prepend>
                    <div class="position-relative d-flex align-center">
                      <div
                        :style="{
                          backgroundColor: category.color,
                          width: '24px',
                          height: '24px',
                          display: 'inline-block',
                          borderRadius: '50%',
                          marginRight: '8px',
                        }"
                      ></div>
                      <v-icon
                        v-if="taskData.category_id === category.id"
                        size="x-small"
                        color="white"
                        class="category-check-icon"
                      >
                        mdi-check
                      </v-icon>
                    </div>
                  </template>
                  <v-list-item-title>{{ category.name }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card>
          </v-menu>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" variant="text" @click="cancel">キャンセル</v-btn>
        <v-btn color="primary" variant="text" @click="save">保存</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import CategoryService from "@/services/CategoryService";

export default {
  name: "TaskEditDialog",
  props: {
    task: {
      type: Object,
      default: null,
    },
    visible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      taskData: null,
      categories: [],
      loadingCategories: false,
      categoryMenuOpen: false,
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
    // 重複のない一意なカテゴリリスト
    uniqueCategories() {
      // IDをキーにしてマップを作成して重複を排除
      const categoryMap = new Map();
      this.categories.forEach((category) => {
        if (!categoryMap.has(category.id)) {
          categoryMap.set(category.id, category);
        }
      });
      // マップから値のみを配列として返す
      return Array.from(categoryMap.values());
    },
    // 選択されているカテゴリ
    selectedCategory() {
      if (!this.taskData || this.taskData.category_id === null) return null;
      return (
        this.uniqueCategories.find((c) => c.id === this.taskData.category_id) ||
        null
      );
    },
  },
  watch: {
    task(newTask) {
      if (newTask) {
        // category_idを追加してディープコピーを作成
        const taskCopy = JSON.parse(JSON.stringify(newTask));
        taskCopy.category_id = newTask.category ? newTask.category.id : null;
        this.taskData = taskCopy;
      } else {
        this.taskData = null;
      }
    },
    visible(newVal) {
      if (newVal) {
        this.fetchCategories();
        if (this.task) {
          const taskCopy = JSON.parse(JSON.stringify(this.task));
          taskCopy.category_id = this.task.category
            ? this.task.category.id
            : null;
          this.taskData = taskCopy;
        }
      }
    },
  },
  methods: {
    // カテゴリ一覧の取得
    fetchCategories() {
      this.loadingCategories = true;
      CategoryService.getCategories()
        .then((response) => {
          this.categories = response.data;
          this.loadingCategories = false;

          // デバッグ用
          console.log("取得したカテゴリ:", this.categories);
          console.log("uniqueCategories:", this.uniqueCategories);
        })
        .catch((error) => {
          console.error("カテゴリの取得中にエラーが発生しました:", error);
          this.loadingCategories = false;
        });
    },

    // カテゴリを選択
    selectCategory(category) {
      if (this.taskData) {
        this.taskData.category_id = category ? category.id : null;
      }
      this.categoryMenuOpen = false;
    },

    save() {
      if (!this.taskData.title.trim()) return;
      this.$emit("save", this.taskData);
    },

    cancel() {
      this.$emit("cancel");
    },
  },
  created() {
    this.fetchCategories();
  },
};
</script>

<style scoped>
.position-relative {
  position: relative;
}

.category-check-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
}
</style>
