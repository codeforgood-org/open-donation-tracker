export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface Organization {
  id: number;
  name: string;
  description?: string;
  website?: string;
  email?: string;
  phone?: string;
  ein?: string;
  category?: string;
  logo_url?: string;
  is_verified: boolean;
  transparency_score: number;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface Campaign {
  id: number;
  name: string;
  description?: string;
  goal_amount: number;
  current_amount: number;
  currency: string;
  is_active: boolean;
  image_url?: string;
  start_date: string;
  end_date: string;
  organization_id: number;
  created_at: string;
  updated_at: string;
}

export interface Donation {
  id: number;
  amount: number;
  currency: string;
  status: DonationStatus;
  payment_method?: PaymentMethod;
  transaction_id?: string;
  notes?: string;
  is_anonymous: boolean;
  is_recurring: boolean;
  recurring_frequency?: string;
  donor_id: number;
  organization_id: number;
  campaign_id?: number;
  donation_date: string;
  created_at: string;
}

export interface ImpactReport {
  id: number;
  title: string;
  description?: string;
  period_start: string;
  period_end: string;
  metrics: Record<string, any>;
  report_url?: string;
  images: string[];
  organization_id: number;
  created_at: string;
  updated_at: string;
}

export enum DonationStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  REFUNDED = 'refunded',
  FAILED = 'failed',
}

export enum PaymentMethod {
  CREDIT_CARD = 'credit_card',
  DEBIT_CARD = 'debit_card',
  BANK_TRANSFER = 'bank_transfer',
  PAYPAL = 'paypal',
  CRYPTO = 'crypto',
  CASH = 'cash',
  CHECK = 'check',
}

export interface DonationStats {
  total_amount: number;
  donation_count: number;
  average_donation: number;
  largest_donation: number;
  by_status: Record<string, number>;
  by_payment_method: Record<string, number>;
}

export interface OrganizationStats {
  total_donations: number;
  donation_count: number;
  donor_count: number;
  active_campaigns: number;
  transparency_score: number;
}

export interface CampaignProgress {
  campaign_id: number;
  name: string;
  goal_amount: number;
  current_amount: number;
  percentage: number;
  donor_count: number;
  days_remaining: number;
  is_active: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  full_name: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
