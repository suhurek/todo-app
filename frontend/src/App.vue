<template>
  <div id="app">
    <TaskList />
  </div>
</template>

<script>
import TaskList from "@/components/TaskList.vue";

export default {
  name: "App",
  components: {
    TaskList,
  },
};
</script>

<style>
body {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
}

#app {
  margin-top: 30px;
}
</style>
