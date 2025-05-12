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
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" variant="text" @click="cancel"> キャンセル </v-btn>
        <v-btn color="primary" variant="text" @click="save"> 保存 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
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
    task(newTask) {
      if (newTask) {
        this.taskData = JSON.parse(JSON.stringify(newTask));
      } else {
        this.taskData = null;
      }
    },
    visible(newVal) {
      if (newVal && this.task) {
        this.taskData = JSON.parse(JSON.stringify(this.task));
      }
    },
  },
  methods: {
    save() {
      if (!this.taskData.title.trim()) return;
      this.$emit("save", this.taskData);
    },
    cancel() {
      this.$emit("cancel");
    },
  },
};
</script>
