import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
              refresh_token: refreshToken,
            });

            const { access_token, refresh_token } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);

            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            localStorage.clear();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, formData);
    return response.data;
  }

  async register(data: any) {
    const response = await axios.post(`${API_BASE_URL}/api/v1/auth/register`, data);
    return response.data;
  }

  async logout() {
    return this.client.post('/auth/logout');
  }

  // Admin endpoints
  async getAdminDashboard() {
    const response = await this.client.get('/admin/dashboard');
    return response.data;
  }

  async getJobs(params?: any) {
    const response = await this.client.get('/admin/jobs', { params });
    return response.data;
  }

  async createJob(data: any) {
    const response = await this.client.post('/admin/jobs', data);
    return response.data;
  }

  async updateJob(jobId: string, data: any) {
    const response = await this.client.put(`/admin/jobs/${jobId}`, data);
    return response.data;
  }

  async assignJob(jobId: string, technicianId: string) {
    const response = await this.client.post(`/admin/jobs/${jobId}/assign`, {
      technician_id: technicianId,
    });
    return response.data;
  }

  // Technician endpoints
  async getTechnicianDashboard() {
    const response = await this.client.get('/technician/dashboard');
    return response.data;
  }

  async getTechnicianJobs(status?: string) {
    const response = await this.client.get('/technician/jobs', {
      params: status ? { status } : {},
    });
    return response.data;
  }

  async startJob(jobId: string) {
    const response = await this.client.post(`/technician/jobs/${jobId}/start`);
    return response.data;
  }

  async completeJob(jobId: string) {
    const response = await this.client.post(`/technician/jobs/${jobId}/complete`);
    return response.data;
  }

  // Customer endpoints
  async getCustomerDashboard() {
    const response = await this.client.get('/customer/dashboard');
    return response.data;
  }

  async getCustomerJobs() {
    const response = await this.client.get('/customer/jobs');
    return response.data;
  }

  async createJobRequest(data: any) {
    const response = await this.client.post('/customer/jobs', data);
    return response.data;
  }
}

export default new ApiService();
