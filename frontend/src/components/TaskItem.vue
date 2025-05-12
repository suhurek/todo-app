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
