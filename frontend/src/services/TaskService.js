import axios from "axios";

const API_URL = "http://localhost:8000/api/";

export default {
  // タスクの一覧を取得
  getTasks() {
    return axios.get(`${API_URL}tasks/`);
  },

  // 特定のタスクを取得
  getTask(id) {
    return axios.get(`${API_URL}tasks/${id}/`);
  },

  // 新しいタスクを作成
  createTask(task) {
    return axios.post(`${API_URL}tasks/`, task);
  },

  // タスクを更新
  updateTask(id, task) {
    return axios.put(`${API_URL}tasks/${id}/`, task);
  },

  // タスクを削除
  deleteTask(id) {
    return axios.delete(`${API_URL}tasks/${id}/`);
  },

  // タスクの完了状態を切り替え
  toggleComplete(id, status) {
    return axios.patch(`${API_URL}tasks/${id}/`, { completed: status });
  },

  // 繰り返しタスク用：タスクを完了にして次の繰り返しを生成
  completeRecurringTask(id, status) {
    return axios.patch(`${API_URL}tasks/${id}/toggle_complete/`, {
      completed: status,
    });
  },

  // タスクの並べ替え
  reorderTasks(taskOrders) {
    return axios.post(`${API_URL}tasks/reorder/`, { task_orders: taskOrders });
  },

  // タスク統計情報を取得
  getTaskStatistics() {
    return axios.get(`${API_URL}tasks/statistics/`);
  },
};
