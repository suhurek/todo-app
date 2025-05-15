<template>
  <v-app :theme="theme">
    <v-app-bar flat>
      <v-container>
        <v-row>
          <v-col cols="12" class="d-flex align-center">
            <v-spacer></v-spacer>
            <v-btn icon @click="toggleTheme">
              <v-icon>{{
                theme === "light" ? "mdi-weather-night" : "mdi-weather-sunny"
              }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>
    <v-main>
      <v-container>
        <TaskList />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TaskList from "@/components/TaskList.vue";

export default {
  name: "App",
  components: {
    TaskList,
  },
  data() {
    return {
      theme: localStorage.getItem("theme") || "light",
    };
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === "light" ? "dark" : "light";
      localStorage.setItem("theme", this.theme);
    },
  },
  created() {
    // システム設定からダークモード検出
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

<style>
/* 基本スタイルはVuetifyによって上書きされますが、カスタムスタイルは残せます */
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ダークモード固有のスタイル追加（必要な場合） */
.v-theme--dark #app {
  color: #f5f5f5;
}
</style>
