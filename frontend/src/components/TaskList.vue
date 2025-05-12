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
          <task-item
            v-for="task in tasks"
            :key="task.id"
            :task="task"
            @toggle-complete="handleToggleComplete"
            @edit="editTask"
            @delete="deleteTask"
          ></task-item>
        </v-list>

        <!-- タスク編集ダイアログ -->
        <task-edit-dialog
          :task="editedTask"
          :visible="editMode"
          @update:visible="editMode = $event"
          @save="updateTask"
          @cancel="cancelEdit"
        ></task-edit-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TaskService from "@/services/TaskService";
import TaskItem from "@/components/TaskItem.vue";
import TaskEditDialog from "@/components/TaskEditDialog.vue";

export default {
  name: "TaskList",
  components: {
    TaskItem,
    TaskEditDialog,
  },
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
    handleToggleComplete(data) {
      TaskService.toggleComplete(data.id, data.completed)
        .then(() => {
          const task = this.tasks.find((t) => t.id === data.id);
          if (task) {
            task.completed = data.completed;
          }
        })
        .catch((error) => {
          console.error("タスクの更新中にエラーが発生しました:", error);
          // エラーの場合は元に戻す
          const task = this.tasks.find((t) => t.id === data.id);
          if (task) {
            task.completed = !data.completed;
          }
        });
    },

    // タスクの編集モード開始
    editTask(task) {
      this.editedTask = task;
      this.editMode = true;
    },

    // タスクの更新
    updateTask(updatedTask) {
      if (!updatedTask || !updatedTask.title.trim()) return;

      TaskService.updateTask(updatedTask.id, updatedTask)
        .then((response) => {
          const index = this.tasks.findIndex((t) => t.id === updatedTask.id);
          if (index !== -1) {
            this.tasks.splice(index, 1, response.data);
          }
          this.editMode = false;
          this.editedTask = null;
        })
        .catch((error) => {
          console.error("タスクの更新中にエラーが発生しました:", error);
        });
    },

    // 編集モードのキャンセル
    cancelEdit() {
      this.editMode = false;
      this.editedTask = null;
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
