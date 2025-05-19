<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2 class="text-center text-h4 mb-6">タスク統計</h2>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
        <div class="mt-2">統計情報を読み込み中...</div>
      </v-col>
    </v-row>

    <template v-else>
      <!-- 全体の進捗サマリー -->
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-subtitle-1">全体の進捗</v-card-title>
            <v-card-text class="text-center">
              <v-progress-circular
                :model-value="completionRate"
                :size="120"
                :width="15"
                :color="completionRateColor"
              >
                {{ completionRateFormatted }}
              </v-progress-circular>
              <div class="mt-2">
                {{ stats.completed_tasks }} / {{ stats.total_tasks }} タスク
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- カテゴリ分布 -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-subtitle-1">カテゴリ分布</v-card-title>
            <v-card-text>
              <div
                v-if="stats.category_distribution.length === 0"
                class="text-center"
              >
                カテゴリデータがありません
              </div>
              <v-list v-else density="compact">
                <v-list-item
                  v-for="item in stats.category_distribution"
                  :key="item.name"
                >
                  <template v-slot:prepend>
                    <div
                      class="color-dot mr-2"
                      :style="{ backgroundColor: item.color }"
                    ></div>
                  </template>
                  <v-list-item-title>{{ item.name }}</v-list-item-title>
                  <template v-slot:append>
                    <v-chip>{{ item.count }}</v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- 優先度分布 -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-subtitle-1">優先度分布</v-card-title>
            <v-card-text>
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="error">mdi-alert-circle</v-icon>
                  </template>
                  <v-list-item-title>高</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="error">{{
                      stats.priority_distribution.high || 0
                    }}</v-chip>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="warning">mdi-minus-circle</v-icon>
                  </template>
                  <v-list-item-title>中</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="warning">{{
                      stats.priority_distribution.medium || 0
                    }}</v-chip>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="success">mdi-chevron-down-circle</v-icon>
                  </template>
                  <v-list-item-title>低</v-list-item-title>
                  <template v-slot:append>
                    <v-chip color="success">{{
                      stats.priority_distribution.low || 0
                    }}</v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- 日次完了タスク数チャート -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-subtitle-1"
              >最近7日間の完了タスク数</v-card-title
            >
            <v-card-text style="height: 300px">
              <v-chart
                v-if="chartOption"
                class="chart"
                :option="chartOption"
                autoresize
              />
              <div v-else class="text-center py-6">
                データが不足しているためグラフを表示できません
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import TaskService from "@/services/TaskService";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart from "vue-echarts";

// EChartsコンポーネントを登録
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

export default {
  name: "TaskStatistics",
  components: {
    VChart,
  },
  data() {
    return {
      loading: true,
      stats: {
        total_tasks: 0,
        completed_tasks: 0,
        completion_rate: 0,
        category_distribution: [],
        priority_distribution: {},
        daily_completion: [],
      },
      chartOption: null,
    };
  },
  computed: {
    completionRate() {
      return this.stats.completion_rate * 100;
    },
    completionRateFormatted() {
      return `${Math.round(this.completionRate)}%`;
    },
    completionRateColor() {
      const rate = this.stats.completion_rate;
      if (rate >= 0.7) return "success";
      if (rate >= 0.4) return "warning";
      return "error";
    },
  },
  methods: {
    async fetchStatistics() {
      this.loading = true;
      try {
        const response = await TaskService.getTaskStatistics();
        this.stats = response.data;
        this.prepareChartData();
      } catch (error) {
        console.error("統計情報の取得中にエラーが発生しました:", error);
      } finally {
        this.loading = false;
      }
    },
    prepareChartData() {
      if (
        !this.stats.daily_completion ||
        this.stats.daily_completion.length === 0
      ) {
        this.chartOption = null;
        return;
      }

      // 日付と完了タスク数のデータを抽出
      const dates = this.stats.daily_completion.map((item) => item.day);
      const counts = this.stats.daily_completion.map((item) => item.count);

      this.chartOption = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: dates,
          axisLabel: {
            interval: 0,
          },
        },
        yAxis: {
          type: "value",
          minInterval: 1,
        },
        series: [
          {
            name: "完了したタスク",
            type: "bar",
            data: counts,
            itemStyle: {
              color: "#4CAF50",
            },
            label: {
              show: true,
              position: "top",
              formatter: "{c}",
            },
          },
        ],
      };
    },
  },
  created() {
    this.fetchStatistics();
  },
};
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
}

.color-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-block;
}
</style>
