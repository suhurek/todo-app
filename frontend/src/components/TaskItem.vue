<template>
  <v-list-item
    :class="task.completed ? 'bg-grey-lighten-3' : ''"
    rounded="lg"
    class="mb-3"
  >
    <template v-slot:prepend>
      <v-checkbox
        v-model="localCompleted"
        @change="toggleComplete"
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

    <!-- カテゴリ表示を追加 -->
    <v-list-item-subtitle>
      <v-row no-gutters>
        <v-col cols="auto" v-if="task.category">
          <v-chip
            :color="task.category.color"
            size="small"
            label
            class="mt-1 mr-2"
          >
            {{ task.category.name }}
          </v-chip>
        </v-col>
        <v-col cols="auto">
          <v-chip
            :color="priorityColor"
            size="small"
            label
            class="mt-1"
            :prepend-icon="priorityIcon"
          >
            {{ priorityLabel }}
          </v-chip>
        </v-col>
        <v-col cols="12" class="mt-1" v-if="task.due_date">
          <v-chip
            size="small"
            prepend-icon="mdi-calendar"
            :color="isOverdue ? 'error' : 'info'"
            variant="outlined"
            class="mr-2"
          >
            {{ formattedDueDate }}
          </v-chip>

          <!-- 繰り返し表示 -->
          <v-chip
            v-if="task.repeat_type !== 'none'"
            size="small"
            prepend-icon="mdi-refresh"
            color="secondary"
            variant="outlined"
          >
            {{ repeatLabel }}
          </v-chip>
        </v-col>
      </v-row>
    </v-list-item-subtitle>

    <template v-slot:append>
      <v-btn
        icon
        variant="text"
        color="primary"
        size="small"
        @click="$emit('edit', task)"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        icon
        variant="text"
        color="error"
        size="small"
        @click="$emit('delete', task.id)"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>
  </v-list-item>
</template>

<script>
import { format, isPast, isToday } from "date-fns";
import { ja } from "date-fns/locale";

export default {
  name: "TaskItem",
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      localCompleted: this.task.completed,
    };
  },
  computed: {
    priorityColor() {
      switch (this.task.priority) {
        case "high":
          return "error";
        case "medium":
          return "warning";
        case "low":
          return "success";
        default:
          return "warning"; // デフォルトは medium
      }
    },
    priorityIcon() {
      switch (this.task.priority) {
        case "high":
          return "mdi-alert-circle";
        case "medium":
          return "mdi-minus-circle";
        case "low":
          return "mdi-chevron-down-circle";
        default:
          return "mdi-minus-circle"; // デフォルトは medium
      }
    },
    priorityLabel() {
      switch (this.task.priority) {
        case "high":
          return "高";
        case "medium":
          return "中";
        case "low":
          return "低";
        default:
          return "中"; // デフォルトは medium
      }
    },
    formattedDueDate() {
      if (!this.task.due_date) return "";
      try {
        return format(new Date(this.task.due_date), "yyyy/MM/dd(E)", {
          locale: ja,
        });
      } catch (e) {
        return "";
      }
    },
    isOverdue() {
      if (!this.task.due_date || this.task.completed) return false;
      const dueDate = new Date(this.task.due_date);
      return isPast(dueDate) && !isToday(dueDate);
    },
    repeatLabel() {
      switch (this.task.repeat_type) {
        case "daily":
          return "毎日";
        case "weekly":
          return "毎週";
        case "monthly":
          return "毎月";
        case "custom":
          return `${this.task.repeat_interval}日ごと`;
        default:
          return "";
      }
    },
  },
  watch: {
    "task.completed"(newVal) {
      this.localCompleted = newVal;
    },
  },
  methods: {
    toggleComplete() {
      this.$emit("toggle-complete", {
        id: this.task.id,
        completed: this.localCompleted,
      });
    },
  },
};
</script>
