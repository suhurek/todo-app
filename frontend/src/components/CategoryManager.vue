<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center">
        <span>カテゴリ管理</span>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-plus"
          @click="addCategory"
        >
          新規カテゴリ
        </v-btn>
      </v-card-title>
      <v-card-text>
        <div v-if="loading" class="text-center my-3">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>
        <v-alert v-else-if="categories.length === 0" type="info" class="my-3">
          カテゴリがありません。新しいカテゴリを追加してください。
        </v-alert>
        <v-chip-group v-else class="mb-4">
          <v-chip
            v-for="category in categories"
            :key="category.id"
            :color="category.color"
            label
            filter
            filter-icon="mdi-check"
            class="mr-2 mb-2"
          >
            {{ category.name }}
            <template v-slot:append>
              <v-icon size="small" @click.stop="editCategory(category)">
                mdi-pencil
              </v-icon>
              <v-icon
                size="small"
                @click.stop="confirmDeleteCategory(category)"
              >
                mdi-delete
              </v-icon>
            </template>
          </v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>

    <!-- カテゴリ編集ダイアログ -->
    <category-dialog
      :category="editedCategory"
      :visible="categoryDialogVisible"
      :is-edit="isEditMode"
      @update:visible="categoryDialogVisible = $event"
      @save="saveCategory"
      @cancel="cancelCategoryEdit"
    ></category-dialog>

    <!-- 確認ダイアログ -->
    <v-dialog v-model="confirmDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">確認</v-card-title>
        <v-card-text>
          このカテゴリを削除しますか？このカテゴリに関連付けられたタスクは、カテゴリなしになります。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="confirmDialog = false"
          >
            キャンセル
          </v-btn>
          <v-btn color="error" variant="text" @click="deleteCategory">
            削除
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import CategoryService from "@/services/CategoryService";
import CategoryDialog from "@/components/CategoryDialog.vue";

export default {
  name: "CategoryManager",
  components: {
    CategoryDialog,
  },
  data() {
    return {
      categories: [],
      loading: true,
      categoryDialogVisible: false,
      editedCategory: null,
      isEditMode: false,
      confirmDialog: false,
      categoryToDelete: null,
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    // カテゴリ一覧の取得
    fetchCategories() {
      this.loading = true;
      CategoryService.getCategories()
        .then((response) => {
          this.categories = response.data;
          this.loading = false;
        })
        .catch((error) => {
          console.error("カテゴリの取得中にエラーが発生しました:", error);
          this.loading = false;
        });
    },

    // 新規カテゴリの追加モード
    addCategory() {
      this.editedCategory = { name: "", color: "#4CAF50" };
      this.isEditMode = false;
      this.categoryDialogVisible = true;
    },

    // カテゴリの編集モード
    editCategory(category) {
      this.editedCategory = { ...category };
      this.isEditMode = true;
      this.categoryDialogVisible = true;
    },

    // カテゴリの保存（作成/更新）
    saveCategory(category) {
      if (this.isEditMode) {
        // 既存カテゴリの更新
        CategoryService.updateCategory(this.editedCategory.id, category)
          .then((response) => {
            const index = this.categories.findIndex(
              (c) => c.id === this.editedCategory.id
            );
            if (index !== -1) {
              this.categories.splice(index, 1, response.data);
            }
            this.categoryDialogVisible = false;
          })
          .catch((error) => {
            console.error("カテゴリの更新中にエラーが発生しました:", error);
          });
      } else {
        // 新規カテゴリの作成
        CategoryService.createCategory(category)
          .then((response) => {
            this.categories.push(response.data);
            this.categoryDialogVisible = false;
          })
          .catch((error) => {
            console.error("カテゴリの作成中にエラーが発生しました:", error);
          });
      }
    },

    // カテゴリ編集のキャンセル
    cancelCategoryEdit() {
      this.categoryDialogVisible = false;
    },

    // カテゴリ削除の確認
    confirmDeleteCategory(category) {
      this.categoryToDelete = category;
      this.confirmDialog = true;
    },

    // カテゴリの削除
    deleteCategory() {
      if (!this.categoryToDelete) return;

      CategoryService.deleteCategory(this.categoryToDelete.id)
        .then(() => {
          this.categories = this.categories.filter(
            (c) => c.id !== this.categoryToDelete.id
          );
          this.confirmDialog = false;
          this.categoryToDelete = null;
        })
        .catch((error) => {
          console.error("カテゴリの削除中にエラーが発生しました:", error);
        });
    },
  },
};
</script>
