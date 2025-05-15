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

        <!-- 優先度選択 -->
        <div class="mb-4">
          <label class="text-subtitle-1 mb-2 d-block">優先度</label>
          <v-btn-toggle
            v-model="taskData.priority"
            mandatory
            density="comfortable"
            color="primary"
            variant="outlined"
          >
            <v-btn value="high" prepend-icon="mdi-alert-circle" color="error">
              高
            </v-btn>
            <v-btn
              value="medium"
              prepend-icon="mdi-minus-circle"
              color="warning"
            >
              中
            </v-btn>
            <v-btn
              value="low"
              prepend-icon="mdi-chevron-down-circle"
              color="success"
            >
              低
            </v-btn>
          </v-btn-toggle>
        </div>

        <!-- 期日設定 -->
        <div class="mb-4">
          <label class="text-subtitle-1 mb-2 d-block">期日</label>
          <v-menu
            v-model="dateMenu"
            :close-on-content-click="false"
            location="bottom"
          >
            <template v-slot:activator="{ props }">
              <v-text-field
                v-model="formattedDueDate"
                label="期日を選択"
                readonly
                prepend-icon="mdi-calendar"
                v-bind="props"
                variant="outlined"
                clearable
                clear-icon="mdi-close-circle"
                @click:clear="taskData.due_date = null"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="taskData.due_date"
              @update:model-value="dateMenu = false"
            ></v-date-picker>
          </v-menu>
        </div>

        <!-- 繰り返し設定 -->
        <div class="mb-4">
          <label class="text-subtitle-1 mb-2 d-block">繰り返し</label>
          <v-select
            v-model="taskData.repeat_type"
            :items="repeatOptions"
            label="繰り返しの種類"
            variant="outlined"
            hide-details
            item-title="text"
            item-value="value"
          ></v-select>

          <!-- カスタム繰り返し間隔設定 -->
          <div v-if="taskData.repeat_type === 'custom'" class="mt-3">
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model.number="taskData.repeat_interval"
                  label="間隔"
                  type="number"
                  min="1"
                  variant="outlined"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-select
                  :value="'days'"
                  :items="[{ text: '日ごと', value: 'days' }]"
                  variant="outlined"
                  hide-details
                  disabled
                  item-title="text"
                  item-value="value"
                ></v-select>
              </v-col>
            </v-row>
          </div>

          <!-- 繰り返し設定の注意事項 -->
          <v-alert
            v-if="taskData.repeat_type !== 'none' && !taskData.due_date"
            type="warning"
            variant="tonal"
            class="mt-3"
            density="compact"
          >
            繰り返しタスクを作成するには期日の設定が必要です
          </v-alert>
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
import { format } from "date-fns";
import { ja } from "date-fns/locale";

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
      dateMenu: false,
      repeatOptions: [
        { text: "繰り返しなし", value: "none" },
        { text: "毎日", value: "daily" },
        { text: "毎週", value: "weekly" },
        { text: "毎月", value: "monthly" },
        { text: "カスタム", value: "custom" },
      ],
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
    formattedDueDate() {
      if (!this.taskData || !this.taskData.due_date) return "";
      try {
        return format(new Date(this.taskData.due_date), "yyyy年MM月dd日(E)", {
          locale: ja,
        });
      } catch (e) {
        return "";
      }
    },
  },
  watch: {
    task(newTask) {
      if (newTask) {
        // category_idを追加してディープコピーを作成
        const taskCopy = JSON.parse(JSON.stringify(newTask));
        taskCopy.category_id = newTask.category ? newTask.category.id : null;

        // デフォルトの優先度を設定
        if (!taskCopy.priority) {
          taskCopy.priority = "medium";
        }

        // 繰り返し関連の設定
        if (!taskCopy.repeat_type) {
          taskCopy.repeat_type = "none";
        }

        if (!taskCopy.repeat_interval || taskCopy.repeat_interval < 1) {
          taskCopy.repeat_interval = 1;
        }

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

          // デフォルトの優先度を設定
          if (!taskCopy.priority) {
            taskCopy.priority = "medium";
          }

          // 繰り返し関連の設定も初期化
          if (!taskCopy.repeat_type) {
            taskCopy.repeat_type = "none";
          }

          if (!taskCopy.repeat_interval || taskCopy.repeat_interval < 1) {
            taskCopy.repeat_interval = 1;
          }

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
