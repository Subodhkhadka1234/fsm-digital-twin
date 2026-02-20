export interface User {
  id: string;
  email: string;
  role: string;
  organization_id?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: string;
  organization_id: string;
  customer_id: string;
  assigned_technician_id?: string;
  job_type: string;
  status: string;
  priority: string;
  address: string;
  scheduled_start?: string;
  scheduled_end?: string;
  actual_start?: string;
  actual_end?: string;
  predicted_duration_hours?: number;
  required_skills: string[];
  equipment_details: any;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_jobs: number;
  pending_jobs: number;
  in_progress_jobs: number;
  completed_jobs: number;
  active_technicians: number;
  sla_compliance: number;
  revenue: number;
}
