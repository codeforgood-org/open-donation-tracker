import axios from 'axios';
import type {
  User,
  Organization,
  Campaign,
  Donation,
  ImpactReport,
  LoginCredentials,
  RegisterData,
  AuthTokens,
  DonationStats,
  OrganizationStats,
  CampaignProgress,
} from '@/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const { data } = await api.post<AuthTokens>('/auth/login', credentials);
    return data;
  },

  register: async (userData: RegisterData): Promise<User> => {
    const { data } = await api.post<User>('/auth/register', userData);
    return data;
  },

  getCurrentUser: async (): Promise<User> => {
    const { data } = await api.get<User>('/auth/me');
    return data;
  },
};

// Organizations API
export const organizationsApi = {
  getAll: async (params?: { category?: string; verified_only?: boolean }) => {
    const { data } = await api.get<Organization[]>('/organizations', { params });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<Organization>(`/organizations/${id}`);
    return data;
  },

  getStats: async (id: number) => {
    const { data } = await api.get<OrganizationStats>(`/organizations/${id}/stats`);
    return data;
  },

  create: async (orgData: Partial<Organization>) => {
    const { data } = await api.post<Organization>('/organizations', orgData);
    return data;
  },

  update: async (id: number, orgData: Partial<Organization>) => {
    const { data } = await api.patch<Organization>(`/organizations/${id}`, orgData);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/organizations/${id}`);
  },
};

// Campaigns API
export const campaignsApi = {
  getAll: async (params?: { organization_id?: number; active_only?: boolean }) => {
    const { data } = await api.get<Campaign[]>('/campaigns', { params });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<Campaign>(`/campaigns/${id}`);
    return data;
  },

  getProgress: async (id: number) => {
    const { data } = await api.get<CampaignProgress>(`/campaigns/${id}/progress`);
    return data;
  },

  create: async (campaignData: Partial<Campaign>) => {
    const { data } = await api.post<Campaign>('/campaigns', campaignData);
    return data;
  },

  update: async (id: number, campaignData: Partial<Campaign>) => {
    const { data } = await api.patch<Campaign>(`/campaigns/${id}`, campaignData);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/campaigns/${id}`);
  },
};

// Donations API
export const donationsApi = {
  getAll: async (params?: { organization_id?: number; campaign_id?: number }) => {
    const { data } = await api.get<Donation[]>('/donations', { params });
    return data;
  },

  getAllPublic: async (params?: { organization_id?: number; campaign_id?: number }) => {
    const { data } = await api.get<Donation[]>('/donations/all', { params });
    return data;
  },

  getStats: async (organization_id?: number) => {
    const { data } = await api.get<DonationStats>('/donations/stats', {
      params: { organization_id },
    });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<Donation>(`/donations/${id}`);
    return data;
  },

  create: async (donationData: Partial<Donation>) => {
    const { data } = await api.post<Donation>('/donations', donationData);
    return data;
  },

  update: async (id: number, donationData: Partial<Donation>) => {
    const { data } = await api.patch<Donation>(`/donations/${id}`, donationData);
    return data;
  },
};

// Impact Reports API
export const impactReportsApi = {
  getAll: async (organization_id?: number) => {
    const { data } = await api.get<ImpactReport[]>('/impact-reports', {
      params: { organization_id },
    });
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<ImpactReport>(`/impact-reports/${id}`);
    return data;
  },

  create: async (reportData: Partial<ImpactReport>) => {
    const { data } = await api.post<ImpactReport>('/impact-reports', reportData);
    return data;
  },

  update: async (id: number, reportData: Partial<ImpactReport>) => {
    const { data } = await api.patch<ImpactReport>(`/impact-reports/${id}`, reportData);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/impact-reports/${id}`);
  },
};

export default api;
