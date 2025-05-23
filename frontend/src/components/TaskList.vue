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

        <!-- カテゴリ管理コンポーネントを追加 -->
        <category-manager class="mb-6"></category-manager>

        <!-- フィルターコントロール（新規追加） -->
        <v-card class="mb-6">
          <v-card-text>
            <v-row align="center">
              <v-col cols="12" sm="6">
                <span class="text-subtitle-1">フィルター:</span>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn-toggle
                  v-model="filter"
                  mandatory
                  color="primary"
                  variant="outlined"
                  rounded
                  density="comfortable"
                >
                  <v-btn value="all">すべて</v-btn>
                  <v-btn value="active">未完了</v-btn>
                  <v-btn value="completed">完了済み</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
            <v-row align="center" class="mt-3">
              <v-col cols="12" sm="6">
                <span class="text-subtitle-1">優先度:</span>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn-toggle
                  v-model="priorityFilter"
                  color="primary"
                  variant="outlined"
                  rounded
                  density="comfortable"
                  multiple
                >
                  <v-btn value="high">高</v-btn>
                  <v-btn value="medium">中</v-btn>
                  <v-btn value="low">低</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
            <v-row align="center" class="mt-3">
              <v-col cols="12" sm="6">
                <span class="text-subtitle-1">期日:</span>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn-toggle
                  v-model="dueDateFilter"
                  color="primary"
                  variant="outlined"
                  rounded
                  density="comfortable"
                >
                  <v-btn value="all">すべて</v-btn>
                  <v-btn value="today">今日</v-btn>
                  <v-btn value="upcoming">今後</v-btn>
                  <v-btn value="overdue">期限超過</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- タスク一覧 -->
        <div v-if="loading" class="text-center my-5">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
          <div class="mt-2">読み込み中...</div>
        </div>
        <v-alert
          v-else-if="filteredTasks.length === 0"
          type="info"
          class="my-5"
        >
          {{ filterEmptyMessage }}
        </v-alert>
        <v-list v-else class="bg-transparent">
          <draggable
            v-model="sortableTasks"
            item-key="id"
            ghost-class="ghost-task"
            handle=".drag-handle"
            :disabled="
              loading ||
              filter !== 'all' ||
              priorityFilter.length > 0 ||
              dueDateFilter !== 'all'
            "
            @end="onDragEnd"
          >
            <template #item="{ element }">
              <task-item
                :task="element"
                @toggle-complete="handleToggleComplete"
                @edit="editTask"
                @delete="deleteTask"
              >
                <template #prepend>
                  <v-icon
                    class="drag-handle mr-2"
                    size="small"
                    :color="
                      filter === 'all' &&
                      priorityFilter.length === 0 &&
                      dueDateFilter === 'all'
                        ? 'grey'
                        : 'grey-lighten-2'
                    "
                  >
                    mdi-drag
                  </v-icon>
                </template>
              </task-item>
            </template>
          </draggable>
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
import CategoryManager from "@/components/CategoryManager.vue";
import draggable from "vuedraggable";

export default {
  name: "TaskList",
  components: {
    TaskItem,
    TaskEditDialog,
    CategoryManager,
    draggable,
  },
  data() {
    return {
      tasks: [],
      loading: true,
      newTask: {
        title: "",
        description: "",
        completed: false,
        priority: "medium",
        repeat_type: "none",
        repeat_interval: 1,
      },
      editMode: false,
      editedTask: null,
      filter: "all", // フィルター状態
      priorityFilter: [],
      dueDateFilter: "all",
    };
  },
  computed: {
    // フィルター適用後のタスク一覧
    filteredTasks() {
      let result = [...this.tasks];

      // ステータスフィルター（完了/未完了）
      switch (this.filter) {
        case "active":
          result = result.filter((task) => !task.completed);
          break;
        case "completed":
          result = result.filter((task) => task.completed);
          break;
      }

      // 優先度フィルター
      if (this.priorityFilter.length > 0) {
        result = result.filter((task) =>
          this.priorityFilter.includes(task.priority)
        );
      }

      // 期日フィルター
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      switch (this.dueDateFilter) {
        case "today":
          result = result.filter((task) => {
            if (!task.due_date) return false;
            const dueDate = new Date(task.due_date);
            dueDate.setHours(0, 0, 0, 0);
            return dueDate.getTime() === today.getTime();
          });
          break;
        case "upcoming":
          result = result.filter((task) => {
            if (!task.due_date) return false;
            const dueDate = new Date(task.due_date);
            dueDate.setHours(0, 0, 0, 0);
            return dueDate > today;
          });
          break;
        case "overdue":
          result = result.filter((task) => {
            if (!task.due_date || task.completed) return false;
            const dueDate = new Date(task.due_date);
            dueDate.setHours(0, 0, 0, 0);
            return dueDate < today;
          });
          break;
      }

      return result;
    },
    // フィルター状態に応じた空メッセージ
    filterEmptyMessage() {
      switch (this.filter) {
        case "active":
          return "未完了のタスクがありません。";
        case "completed":
          return "完了済みのタスクがありません。";
        default:
          return "タスクがありません。新しいタスクを追加してください。";
      }
    },
    // ドラッグ&ドロップ用のソータブルタスク配列
    sortableTasks: {
      get() {
        return this.filteredTasks;
      },
      set() {},
    },
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

      // 最小の順序値を設定（新しいタスクを一番上に表示）
      const minOrder =
        this.tasks.length > 0
          ? Math.min(...this.tasks.map((t) => t.order)) - 1
          : 0;

      const taskWithOrder = {
        ...this.newTask,
        order: minOrder,
      };

      TaskService.createTask(taskWithOrder)
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
      // タスクを検索
      const task = this.tasks.find((t) => t.id === data.id);
      if (!task) return;

      // 繰り返しタスクかどうかを確認
      const isRecurring =
        task.repeat_type && task.repeat_type !== "none" && task.due_date;

      // 適切なメソッドを選択
      const serviceMethod = isRecurring
        ? TaskService.completeRecurringTask
        : TaskService.toggleComplete;

      // APIリクエスト実行
      serviceMethod(data.id, data.completed)
        .then((response) => {
          // タスクの完了状態を更新
          const task = this.tasks.find((t) => t.id === data.id);
          if (task) {
            task.completed = data.completed;
          }

          // 新しい繰り返しタスクが作成された場合、リストに追加
          if (response.data.next_task) {
            this.tasks.unshift(response.data.next_task);
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

    // ドラッグ&ドロップ完了時の処理
    onDragEnd() {
      // フィルターが適用されている場合は並べ替えをスキップ
      if (
        this.filter !== "all" ||
        this.priorityFilter.length > 0 ||
        this.dueDateFilter !== "all"
      ) {
        return;
      }

      // 新しい順序を計算
      const taskOrders = this.sortableTasks.map((task, index) => ({
        id: task.id,
        order: index,
      }));

      // バックエンドに順序更新を送信
      TaskService.reorderTasks(taskOrders)
        .then(() => {
          // 成功したら、メモリ内のtasks配列も更新
          const tasksMap = new Map();
          this.sortableTasks.forEach((task, index) => {
            tasksMap.set(task.id, { ...task, order: index });
          });

          this.tasks = this.tasks.map((task) =>
            tasksMap.has(task.id) ? tasksMap.get(task.id) : task
          );
        })
        .catch((error) => {
          console.error("タスクの並べ替え中にエラーが発生しました:", error);
        });
    },
  },
};
</script>
