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
