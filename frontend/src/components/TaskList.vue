<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <h1 class="text-center text-h4 mb-6">タスク管理アプリ</h1>

        <!-- タスク追加フォーム -->
        <v-form @submit.prevent="addTask" class="mb-6">
          <v-row>
            <v-col cols="9">
              <v-text-field
                v-model="newTask.title"
                label="新しいタスクを入力..."
                variant="outlined"
                density="comfortable"
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-btn color="primary" block height="56" @click="addTask">
                追加
              </v-btn>
            </v-col>
          </v-row>
        </v-form>

        <!-- タスク一覧 -->
        <div v-if="loading" class="text-center my-5">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
          <div class="mt-2">読み込み中...</div>
        </div>
        <v-alert v-else-if="tasks.length === 0" type="info" class="my-5">
          タスクがありません。新しいタスクを追加してください。
        </v-alert>
        <v-list v-else class="bg-transparent">
          <v-list-item
            v-for="task in tasks"
            :key="task.id"
            :class="task.completed ? 'bg-grey-lighten-3' : ''"
            rounded="lg"
            class="mb-3"
          >
            <template v-slot:prepend>
              <v-checkbox
                v-model="task.completed"
                @change="toggleTask(task)"
                hide-details
                color="primary"
              ></v-checkbox>
            </template>
            <v-list-item-title
              :class="{
                'text-decoration-line-through': task.completed,
                'text-grey': task.completed,
              }"
            >
              {{ task.title }}
            </v-list-item-title>
            <template v-slot:append>
              <v-btn
                icon
                variant="text"
                color="primary"
                size="small"
                @click="editTask(task)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn
                icon
                variant="text"
                color="error"
                size="small"
                @click="deleteTask(task.id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-list-item>
        </v-list>

        <!-- タスク編集ダイアログ -->
        <v-dialog v-model="editMode" max-width="500px">
          <v-card v-if="editedTask">
            <v-card-title>タスクの編集</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="editedTask.title"
                label="タスク名"
                variant="outlined"
                class="mb-4"
              ></v-text-field>
              <v-textarea
                v-model="editedTask.description"
                label="詳細説明（任意）"
                variant="outlined"
                rows="4"
              ></v-textarea>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="error" variant="text" @click="cancelEdit">
                キャンセル
              </v-btn>
              <v-btn color="primary" variant="text" @click="updateTask">
                保存
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TaskService from "@/services/TaskService";

export default {
  name: "TaskList",
  data() {
    return {
      tasks: [],
      loading: true,
      newTask: {
        title: "",
        description: "",
        completed: false,
      },
      editMode: false,
      editedTask: null,
    };
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    // タスク一覧の取得
    fetchTasks() {
      this.loading = true;
      TaskService.getTasks()
        .then((response) => {
          this.tasks = response.data;
          this.loading = false;
        })
        .catch((error) => {
          console.error("タスクの取得中にエラーが発生しました:", error);
          this.loading = false;
        });
    },

    // 新しいタスクの追加
    addTask() {
      if (!this.newTask.title.trim()) return;

      TaskService.createTask(this.newTask)
        .then((response) => {
          this.tasks.unshift(response.data);
          this.newTask.title = "";
          this.newTask.description = "";
        })
        .catch((error) => {
          console.error("タスクの作成中にエラーが発生しました:", error);
        });
    },

    // タスクの完了状態の切り替え
    toggleTask(task) {
      const newStatus = task.completed;
      TaskService.toggleComplete(task.id, newStatus)
        .then(() => {
          // APIで更新が成功すれば、UIの状態は既に更新されている
        })
        .catch((error) => {
          // エラーの場合は元に戻す
          task.completed = !newStatus;
          console.error("タスクの更新中にエラーが発生しました:", error);
        });
    },

    // タスクの編集モード開始
    editTask(task) {
      this.editedTask = { ...task };
      this.editMode = true;
    },

    // タスクの更新
    updateTask() {
      // nullチェックを追加
      if (!this.editedTask) {
        console.error("編集中のタスクがnullです");
        this.editMode = false;
        return;
      }

      if (!this.editedTask.title || !this.editedTask.title.trim()) {
        return;
      }

      TaskService.updateTask(this.editedTask.id, this.editedTask)
        .then((response) => {
          const index = this.tasks.findIndex(
            (t) => t.id === this.editedTask.id
          );
          if (index !== -1) {
            this.tasks.splice(index, 1, response.data);
          }

          // 未使用の変数宣言を削除し、順序を維持
          this.editedTask = null;
          this.editMode = false;
        })
        .catch((error) => {
          console.error("タスクの更新中にエラーが発生しました:", error);
          this.editedTask = null;
          this.editMode = false;
        });
    },

    // 編集モードのキャンセル
    cancelEdit() {
      // 順序を変更
      this.editedTask = null;
      this.editMode = false;
    },

    // タスクの削除
    deleteTask(id) {
      if (!confirm("このタスクを削除しますか？")) return;

      TaskService.deleteTask(id)
        .then(() => {
          this.tasks = this.tasks.filter((task) => task.id !== id);
        })
        .catch((error) => {
          console.error("タスクの削除中にエラーが発生しました:", error);
        });
    },
  },
};
</script>
