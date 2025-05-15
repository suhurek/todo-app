import { createVuetify } from "vuetify";
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

// Vuetify
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        dark: false,
        colors: {
          primary: "#4CAF50",
          secondary: "#03A9F4",
          error: "#F44336",
          warning: "#FFC107",
          success: "#8BC34A",
          // 他のカラー設定はそのまま
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: "#81C784", // 明るい緑
          secondary: "#29B6F6", // 明るい青
          error: "#EF5350", // 明るい赤
          warning: "#FFD54F", // 明るい黄色
          success: "#AED581", // 明るい緑
          background: "#121212", // 暗い背景
          surface: "#1E1E1E", // 暗い表面
        },
      },
    },
  },
});
