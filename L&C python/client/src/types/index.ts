export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface NewsArticle {
  id: number;
  title: string;
  content: string;
  url: string;
  source: string;
  category: string;
  published_at: string;
  created_at: string;
}

export interface ExternalServer {
  id: number;
  name: string;
  api_key: string;
  base_url: string;
  is_active: boolean;
}

export interface NotificationPreference {
  id: number;
  user_id: number;
  email_notifications: boolean;
  categories: string[];
  frequency: 'daily' | 'weekly';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ApiError {
  detail: string;
  status_code: number;
} 