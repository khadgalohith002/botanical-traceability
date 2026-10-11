/**
 * PhytoTrace API Client Service
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const err = await response.json();
      errorDetail = err.detail || err.message || errorDetail;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/api/health`);
    return handleResponse(res);
  },

  async getLanguages() {
    const res = await fetch(`${API_BASE}/api/languages`);
    return handleResponse(res);
  },

  async getTranslations(lang = 'en') {
    const res = await fetch(`${API_BASE}/api/translations/${lang}`);
    return handleResponse(res);
  },

  async getCrops(lang = 'en') {
    const res = await fetch(`${API_BASE}/api/crops?lang=${lang}`);
    return handleResponse(res);
  },

  async getCategories(lang = 'en') {
    const res = await fetch(`${API_BASE}/api/categories?lang=${lang}`);
    return handleResponse(res);
  },

  async getBatches(params = {}) {
    const query = new URLSearchParams();
    if (params.crop_id) query.append('crop_id', params.crop_id);
    if (params.category) query.append('category', params.category);
    if (params.status) query.append('status', params.status);
    if (params.stage) query.append('stage', params.stage);
    if (params.search) query.append('search', params.search);
    if (params.sort_by) query.append('sort_by', params.sort_by);
    if (params.order) query.append('order', params.order);

    const res = await fetch(`${API_BASE}/api/batches?${query.toString()}`);
    return handleResponse(res);
  },

  async getBatch(batchId) {
    const res = await fetch(`${API_BASE}/api/batches/${batchId}`);
    return handleResponse(res);
  },

  async registerHarvest(data) {
    const res = await fetch(`${API_BASE}/api/harvest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(res);
  },

  async traceBatch(batchId) {
    const res = await fetch(`${API_BASE}/api/trace/${batchId}`);
    return handleResponse(res);
  },

  async getGraphData(highlightBatchId = null) {
    const query = highlightBatchId ? `?highlight_batch_id=${encodeURIComponent(highlightBatchId)}` : '';
    const res = await fetch(`${API_BASE}/api/graph/data${query}`);
    return handleResponse(res);
  },

  async getGraphMetrics() {
    const res = await fetch(`${API_BASE}/api/graph/metrics`);
    return handleResponse(res);
  },

  async getCypher() {
    const res = await fetch(`${API_BASE}/api/graph/cypher`);
    return handleResponse(res);
  },

  async getAnalyticsSummary() {
    const res = await fetch(`${API_BASE}/api/analytics/summary`);
    return handleResponse(res);
  },

  async getFarms() {
    const res = await fetch(`${API_BASE}/api/farms`);
    return handleResponse(res);
  },

  async getSuppliers() {
    const res = await fetch(`${API_BASE}/api/suppliers`);
    return handleResponse(res);
  },
};
