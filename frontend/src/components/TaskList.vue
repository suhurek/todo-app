<template>
  <div class="task-list">
    <h1>タスク管理アプリ</h1>

    <!-- タスク追加フォーム -->
    <div class="task-form">
      <input
        v-model="newTask.title"
        placeholder="新しいタスクを入力..."
        @keyup.enter="addTask"
      />
      <button @click="addTask">追加</button>
    </div>

    <!-- タスク一覧 -->
    <div v-if="loading" class="loading">読み込み中...</div>
    <div v-else-if="tasks.length === 0" class="no-tasks">
      タスクがありません。新しいタスクを追加してください。
    </div>
    <ul v-else class="tasks">
      <li
        v-for="task in tasks"
        :key="task.id"
        :class="{ completed: task.completed }"
      >
        <div class="task-content">
          <input
            type="checkbox"
            :checked="task.completed"
            @change="toggleTask(task)"
          />
          <span class="task-title">{{ task.title }}</span>
        </div>
        <div class="task-actions">
          <button @click="editTask(task)" class="edit">編集</button>
          <button @click="deleteTask(task.id)" class="delete">削除</button>
        </div>
      </li>
    </ul>

    <!-- タスク編集モーダル -->
    <div v-if="editMode" class="modal">
      <div class="modal-content">
        <h2>タスクの編集</h2>
        <input v-model="editedTask.title" placeholder="タスク名" />
        <textarea
          v-model="editedTask.description"
          placeholder="詳細説明（任意）"
        ></textarea>
        <div class="modal-actions">
          <button @click="updateTask" class="save">保存</button>
          <button @click="cancelEdit" class="cancel">キャンセル</button>
        </div>
      </div>
    </div>
  </div>
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
      const newStatus = !task.completed;
      TaskService.toggleComplete(task.id, newStatus)
        .then(() => {
          task.completed = newStatus;
        })
        .catch((error) => {
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
      if (!this.editedTask.title.trim()) return;

      TaskService.updateTask(this.editedTask.id, this.editedTask)
        .then((response) => {
          const index = this.tasks.findIndex(
            (t) => t.id === this.editedTask.id
          );
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

<style scoped>
.task-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.task-form {
  display: flex;
  margin-bottom: 20px;
}

.task-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
}

.task-form button {
  padding: 10px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.tasks {
  list-style: none;
  padding: 0;
}

.tasks li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 10px;
  border-left: 4px solid #4caf50;
}

.tasks li.completed {
  border-left-color: #999;
  opacity: 0.7;
}

.tasks li.completed .task-title {
  text-decoration: line-through;
  color: #777;
}

.task-content {
  display: flex;
  align-items: center;
}

.task-title {
  margin-left: 10px;
}

.task-actions button {
  margin-left: 5px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-actions .edit {
  background-color: #2196f3;
  color: white;
}

.task-actions .delete {
  background-color: #f44336;
  color: white;
}

.loading,
.no-tasks {
  text-align: center;
  margin: 20px 0;
  color: #777;
}

/* モーダルスタイル */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  width: 80%;
  max-width: 500px;
}

.modal-content h2 {
  margin-top: 0;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-content textarea {
  min-height: 100px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.modal-actions button {
  margin-left: 10px;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions .save {
  background-color: #4caf50;
  color: white;
}

.modal-actions .cancel {
  background-color: #f44336;
  color: white;
}
</style>
