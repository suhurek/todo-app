<template>
  <v-app :theme="theme">
    <v-app-bar app>
      <v-toolbar-title>タスク管理アプリ</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- タブナビゲーション -->
      <v-tabs v-model="activeTab">
        <v-tab value="tasks">タスク一覧</v-tab>
        <v-tab value="statistics">統計</v-tab>
      </v-tabs>

      <!-- ダークモード切り替えボタン -->
      <v-btn icon @click="toggleTheme">
        <v-icon>{{
          theme === "light" ? "mdi-weather-night" : "mdi-weather-sunny"
        }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <!-- タブの内容を表示 -->
        <div v-if="activeTab === 'tasks'">
          <task-list />
        </div>
        <div v-else-if="activeTab === 'statistics'">
          <task-statistics />
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TaskList from "@/components/TaskList.vue";
import TaskStatistics from "@/components/TaskStatistics.vue";

export default {
  name: "App",
  components: {
    TaskList,
    TaskStatistics,
  },
  data() {
    return {
      theme: localStorage.getItem("theme") || "light",
      activeTab: "tasks",
    };
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === "light" ? "dark" : "light";
      localStorage.setItem("theme", this.theme);
    },
  },
  created() {
    // システム設定からダークモード検出（オプション）
    if (!localStorage.getItem("theme")) {
      const prefersDark =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      this.theme = prefersDark ? "dark" : "light";
      localStorage.setItem("theme", this.theme);
    }
  },
};
</script>
