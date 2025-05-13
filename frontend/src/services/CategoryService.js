import axios from "axios";

const API_URL = "http://localhost:8000/api/";

export default {
  // カテゴリ一覧の取得
  getCategories() {
    return axios.get(`${API_URL}categories/`);
  },

  // 特定のカテゴリを取得
  getCategory(id) {
    return axios.get(`${API_URL}categories/${id}/`);
  },

  // 新しいカテゴリの作成
  createCategory(category) {
    return axios.post(`${API_URL}categories/`, category);
  },

  // カテゴリの更新
  updateCategory(id, category) {
    return axios.put(`${API_URL}categories/${id}/`, category);
  },

  // カテゴリの削除
  deleteCategory(id) {
    return axios.delete(`${API_URL}categories/${id}/`);
  },
};
